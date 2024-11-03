import asyncio
import traceback
from typing import Any, Coroutine, Union

from loguru import logger
from taskiq import (
    InMemoryBroker,
    TaskiqMessage,
    TaskiqMiddleware,
    TaskiqResult,
    TaskiqScheduler,
)

from taskiq.cli.scheduler.args import SchedulerArgs
from taskiq.cli.scheduler.run import run_scheduler as run_taskiq_scheduler
from taskiq.schedule_sources import LabelScheduleSource


class BrokerMiddleware(TaskiqMiddleware):
    def on_error(
        self,
        message: "TaskiqMessage",
        result: "TaskiqResult[Any]",
        exception: BaseException,
    ) -> "Union[None, Coroutine[Any, Any, None]]":
        tb_str = "".join(
            traceback.format_exception(
                type(exception), value=exception, tb=exception.__traceback__
            )
        )
        logger.error(tb_str)
        return None


broker = InMemoryBroker().with_middlewares(BrokerMiddleware())

scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)],
)

if __name__ == "__main__":
    asyncio.run(
        run_taskiq_scheduler(
            SchedulerArgs(
                scheduler="app.background:scheduler",
                modules=["app.tasks"],
                tasks_pattern=("./tasks/*task.py",),
                fs_discover=True,
            )
        )
    )
