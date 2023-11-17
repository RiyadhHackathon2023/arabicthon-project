import enum
from sqlalchemy import Column, String, Enum, DateTime
from datetime import datetime
from .base import base_provider

class WorkerStatusEnum(enum.Enum):
    Running = "Running"
    Pending = "Pending"
    Completed = "Completed"
    Failed = "Failed"
    Canceled = "Canceled"

    def __str__(self):
        return str(self.value)


class WorkerModel(base_provider.Base):
    __tablename__ = 'workers'
    worker_id = Column(
        String(255),
        primary_key=True
    )

    worker_name = Column(
        String(255)
    )

    worker_status = Column(
        Enum(WorkerStatusEnum),
        default=WorkerStatusEnum.Pending
    )

    worker_description = Column(
        String(255)
    )

    start_date = Column(
        DateTime(),
        default=datetime.now()
    )

    end_date =Column(
        DateTime(),
    )

    domain = Column(
        String(255)
    )

    task = Column(
        String(255)
    )

    def tojson(self):
        return {
            'worker_id': self.worker_id,
            'worker_name': self.worker_name,
            'worker_status': str(self.worker_status),
            'worker_description': self.worker_description,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'domain': self.domain,
            'task': self.task,
        }