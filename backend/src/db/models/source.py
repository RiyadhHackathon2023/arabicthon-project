import enum
from sqlalchemy import Integer, Column, String, Enum, DateTime
from .base import base_provider
from datetime import datetime


class SourceTypeEnum(enum.Enum):
    File = "File"
    Url = "Url"
    Wikipedia = "Wikipedia"

    def __str__(self):
        return str(self.value)


class SourceModel(base_provider.Base):
    __tablename__ = 'sources'

    source_id = Column(String(), primary_key=True)

    source_name = Column(String(255))

    source_description = Column(String(), default="")

    source_type = Column(Enum(SourceTypeEnum))

    source_url = Column(String())

    source_domain = Column(String(), default="")

    source_file = Column(String(), nullable=True)

    created_at = Column(DateTime(), default=datetime.utcnow())

    def tojson(self):
        return {
            'source_id': self.source_id,
            'source_name': self.source_name,
            'source_description': self.source_description,
            'source_type': str(self.source_type),
            'source_url': self.source_url,
            'source_domain': self.source_domain,
            'source_file': self.source_file,
            'created_at': self.created_at.isoformat(),
        }