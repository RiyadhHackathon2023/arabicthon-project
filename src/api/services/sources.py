from typing import Union
from ...db.session import get_session
from ...db.models import SourceModel, SourceTypeEnum


async def get_source(source_id: str, source_type: SourceTypeEnum):
    # Search for source
    session = get_session()
    source_query = session.query(SourceModel)
    source: Union[SourceModel, None] = source_query.filter(SourceModel.source_id == source_id).first()
    if not source:
        return

    # swift = get_swift_connection()
    # cv_filename = cv.cv_filename
    # header, obj = swift.connection.get_object('cvs', cv_filename)
    # return header, obj

