import datetime
import enum
import typing
import uuid
import pydantic

from toradh import Option, Optional

from src.database import Database

from psycopg.sql import SQL, Identifier, Placeholder
from psycopg.types.json import Jsonb


class CronTask(pydantic.BaseModel):
    class TaskStatusEnum(str, enum.Enum):
        CREATED = "CREATED"
        PROCESSING = "PROCESSING"
        ERROR = "ERROR"
        DONE = "DONE"

    id: uuid.UUID
    created_on: datetime.datetime
    updated_on: datetime.datetime
    expected_by: datetime.datetime
    task_id: str  # this should be the name of the function (AKA task) to invoke with the payload as argument
    payload: dict[str, typing.Any]
    status: TaskStatusEnum


class CronRepository:
    TABLE_NAME = "cron_task"

    def __init__(self, db: Database, schema: str) -> None:
        self.__db = db
        self.__db_schema = schema
        self._fields = CronTask.model_fields

    async def create_task(
        self,
        task_id: str,
        payload: dict[str, typing.Any],
        expected_by: datetime.datetime,
    ) -> CronTask:
        task = CronTask(
            id=uuid.uuid4(),
            created_on=datetime.datetime.now(datetime.timezone.utc),
            updated_on=datetime.datetime.now(datetime.timezone.utc),
            expected_by=expected_by,
            task_id=task_id,
            payload=payload,
            status=CronTask.TaskStatusEnum.CREATED,
        )

        async with self.__db.aget_session(dict[str, uuid.UUID]) as session:
            content_id_dict = await (
                await session.execute(
                    SQL(
                        "INSERT INTO {0} ({1}) VALUES ({2}) RETURNING id AS id",
                    ).format(
                        Identifier(self.__db_schema, self.TABLE_NAME),
                        SQL(" ,").join(
                            [Identifier(col) for col in self._fields.keys()]
                        ),
                        SQL(", ").join(
                            [Placeholder() for _ in range(len(self._fields))]
                        ),
                    ),
                    tuple(
                        [
                            self._map_field_to_column_value(getattr(task, attr))
                            for attr in self._fields
                        ]
                    ),
                )
            ).fetchone()
            await session.commit()
            assert content_id_dict
            content_id = content_id_dict["id"]

            persisted_entity = await self.get_by_id(content_id)

            return typing.cast(CronTask, persisted_entity.unwrap())

    async def get_by_id(self, id: uuid.UUID) -> Optional[CronTask]:
        async with self.__db.aget_session(CronTask) as session:
            result = await (
                await session.execute(
                    SQL("SELECT {0} FROM {1} as entity WHERE  entity.id = {2}").format(
                        SQL(" ,").join(
                            [Identifier(col) for col in self._fields.keys()]
                        ),
                        Identifier(self.__db_schema, self.TABLE_NAME),
                        Placeholder(),
                    ),
                    (id,),
                )
            ).fetchone()
        return Option.of(result)

    async def get_by_run_date(
        self, run_date: datetime.datetime, status: CronTask.TaskStatusEnum | None
    ) -> list[CronTask]:
        async with self.__db.aget_session(CronTask) as session:
            result = await (
                await session.execute(
                    SQL(
                        """
                        SELECT {0} 
                        FROM {1} as entity 
                        WHERE  entity.expected_by <= {2}
                        AND {3}
                        """
                    ).format(
                        SQL(" ,").join(
                            [Identifier(col) for col in self._fields.keys()]
                        ),
                        Identifier(self.__db_schema, self.TABLE_NAME),
                        Placeholder(),
                        SQL("entity.status = %s") if status is not None else SQL("1=1"),
                    ),
                    (run_date, status) if status is not None else (run_date,),
                )
            ).fetchall()
        return result

    async def update_status(
        self, task_id: uuid.UUID, status: CronTask.TaskStatusEnum
    ) -> None:
        async with self.__db.aget_session(None) as session:
            await session.execute(
                SQL(""" 
                    UPDATE {0}
                    SET {1}
                    WHERE id = %s
                    """).format(
                    Identifier(self.__db_schema, self.TABLE_NAME),
                    SQL(", ").join(
                        [
                            SQL("{0} = {1}").format(Identifier(col), Placeholder())
                            for col in ["status", "updated_on"]
                        ]
                    ),
                ),
                tuple([status, datetime.datetime.now(datetime.timezone.utc), task_id]),
            )
            await session.commit()

    def _map_field_to_column_value(self, field: typing.Any) -> typing.Any:
        match field:
            case dict():
                return Jsonb(self._serialize_value(field))
            case list():
                return Jsonb(self._serialize_value(field))
            case _ if isinstance(field, pydantic.BaseModel):
                return Jsonb(self._serialize_value(field))
            case _:
                return field

    def _serialize_value(self, value: typing.Any) -> typing.Any:
        """prepare values for JSON serialization. Specifically design to deal
        with recursive structures

        Args:
            value (typing.Any): object to serialize

        Returns:
            typing.Any: JSON serialization
        """
        match value:
            case dict():
                return {k: self._serialize_value(v) for k, v in value.items()}
            case list():
                return [self._serialize_value(v) for v in value]
            case set():
                return set([self._serialize_value(v) for v in value])
            case _ if isinstance(value, pydantic.BaseModel):
                return value.model_dump()
            case _:
                return value
