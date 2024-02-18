from sqlalchemy import Column, String, ForeignKey
from .base import base_provider

class WorkerSourceModel(base_provider.Base):
    __tablename__ = 'workers_sources'

    worker_id = Column(
        String, 
        ForeignKey('workers.worker_id'),
        primary_key=True,
    )

    source_id = Column(
        String, 
        ForeignKey('sources.source_id'),
        primary_key=True,
    )


    def tojson(self):
        return {
            'worker_id': self.worker_id,
            'source_id': self.source_id,
        }