import enum
from sqlalchemy import Integer, Column, String, Enum
from .base import base_provider

class SourceTypeEnum(enum.Enum):
    File = "File"
    Url = "Url"

class SourceModel(base_provider.Base):
    __tablename__ = 'sources'

    source_id = Column(
        Integer,
        primary_key=True
    )

    source_name = Column(
        String(255)
    )

    source_type = Column(
        Enum(SourceTypeEnum)
    )


    def tojson(self):
        return {
            'source_id': self.source_id,
            'source_name': self.source_name,
            'source_type': self.source_type,
        }