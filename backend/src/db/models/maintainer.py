from sqlalchemy import Column, String
from .base import base_provider

class MaintainerModel(base_provider.Base):
    __tablename__ = 'maintainers'

    maintainer_id = Column(
        String,
        primary_key=True,
    )

    name = Column(
        String(50)
    )

    email = Column(
        String(50),
        unique=True
    )
    password = Column(
        String
    )


    def tojson(self):
        return {
            'maintainer_id': self.maintainer_id,
            'name': self.name,
            'email': self.email,
        }