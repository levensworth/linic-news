import logging
from dependency_injector import containers, providers

from src.platform_deps.slack_client import SlackClient
from src.config import Environment, settings
from src.cron.repository import CronRepository
from src.cron.service import CronService
from src.database import Database

from pathlib import Path
import ast

_LOGGER = logging.getLogger(__file__)


def find_files_with_inject_decorator(root_dir: Path | str) -> list[str]:
    """
    Searches for Python files using the `@inject` decorator and returns their module paths.

    Args:
        root_dir (str or Path): The root directory to search.

    Returns:
        list: A list of module paths where the `@inject` decorator is used.
    """
    root_path = Path(root_dir)
    module_paths: list[str] = []

    for file_path in root_path.rglob("*.py"):
        module_path = f"{root_path.name}." + file_path.relative_to(
            root_path
        ).with_suffix("").as_posix().replace("/", ".")
        with file_path.open("r", encoding="utf-8") as file:
            try:
                tree = ast.parse(file.read(), filename=str(file_path))
                for node in ast.walk(tree):
                    if (
                        isinstance(node, ast.FunctionDef)
                        or isinstance(node, ast.ClassDef)
                        or isinstance(node, ast.AsyncFunctionDef)
                    ):
                        for decorator in node.decorator_list:
                            if (
                                isinstance(decorator, ast.Name)
                                and decorator.id == "inject"
                            ):
                                module_paths.append(module_path)
                                break
            except SyntaxError as e:
                _LOGGER.error(f"Syntax error in {file_path}: {e}")

    return module_paths


WIRED_MODULES = find_files_with_inject_decorator(Path(__file__).parent)

_LOGGER.info(f"Found {len(WIRED_MODULES)} modules to inject: {WIRED_MODULES}")


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=WIRED_MODULES)

    app_logger: providers.Singleton[logging.Logger] = providers.Singleton(
        logging.Logger, name=settings.app_name
    )

    database: providers.Singleton[Database] = providers.Singleton(
        Database, db_url=settings.db_url, dev=settings.environment == Environment.DEV
    )

    slack_client = providers.Singleton(SlackClient, url=settings.slack_webhook_url)

    # event_bus: providers.Singleton[InMemoryEventBus] = providers.Singleton(
    #     InMemoryEventBus
    # )

    cron_repository = providers.Singleton(CronRepository, database, settings.db_schema)

    cron_service = providers.Factory(CronService, cron_repository)
