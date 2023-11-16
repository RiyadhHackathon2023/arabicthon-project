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
        Enum(WorkerStatusEnum)
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

    def tojson(self):
        return {
            'worker_id': self.worker_id,
            'worker_name': self.worker_name,
            'worker_status': self.worker_status,
            'worker_description': self.worker_description,
            'start_date': self.start_date,
            'end_date': self.end_date,
        }