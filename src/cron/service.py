import datetime
import typing
import uuid
from src.cron.repository import CronRepository, CronTask


class CronService:
    def __init__(self, repository: CronRepository) -> None:
        self.repository = repository

    async def add_task(
        self, task: str, payload: dict[str, typing.Any], expected_by: datetime.datetime
    ) -> CronTask:
        return await self.repository.create_task(
            task_id=task, payload=payload, expected_by=expected_by
        )

    async def get_next_available_tasks(self) -> list[CronTask]:
        return await self.repository.get_by_run_date(
            run_date=datetime.datetime.now(datetime.timezone.utc),
            status=CronTask.TaskStatusEnum.CREATED,
        )

    async def update_task_status(
        self, task_id: uuid.UUID, status: CronTask.TaskStatusEnum
    ) -> None:
        await self.repository.update_status(task_id=task_id, status=status)
