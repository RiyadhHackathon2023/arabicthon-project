from typing import Union, List
from ...db.session import get_session
from ...db.models import SourceModel, SourceTypeEnum
from .responses.service_response import ServiceResponse
from ...storage_manager import get_swift_connection
import uuid


async def stream_source_file(source_id: str):
    # Search for source
    session = get_session()
    source_query = session.query(SourceModel)
    source: Union[SourceModel, None] = source_query.filter(
        SourceModel.source_id == source_id).first()
    if not source:
        return ServiceResponse(response_status='error',
                               data=None,
                               message='Source not found',
                               http_code=404)
    f_name = source.source_name
    f_path = f'{f_name}_{source_id}'
    swift = get_swift_connection()
    try:
        header, obj = swift.connection.get_object('documents', f_path)
        return ServiceResponse(response_status='success',
                               data=(header, obj),
                               message='',
                               http_code=200)
    except:
        return ServiceResponse(response_status='error',
                               data=None,
                               message='Could not fetch data',
                               http_code=500)
    finally:
        session.close()
        swift.connection.close()


async def get_source(source_id: str):
    # Search for source
    session = get_session()
    source_query = session.query(SourceModel)
    source: Union[SourceModel, None] = source_query.filter(
        SourceModel.source_id == source_id).first()
    if not source:
        session.close()

        return ServiceResponse(response_status='error',
                               data=None,
                               message='Source not found',
                               http_code=404)
    session.close()

    return ServiceResponse(response_status='error',
                           data=source.tojson(),
                           message='Source found',
                           http_code=200)


async def del_source(source_id: str):
    # Search for source
    session = get_session()
    source_query = session.query(SourceModel)
    source: Union[SourceModel, None] = source_query.filter(
        SourceModel.source_id == source_id).first()
    if not source:
        session.close()

        return ServiceResponse(response_status='error',
                               data=None,
                               message='Source not found',
                               http_code=404)
    try:
        session.delete(source)
        session.commit()
        return ServiceResponse(response_status='success',
                           data=None,
                           message=f'Source {source_id} deleted',
                           http_code=200)
    except:
        return ServiceResponse(response_status='error',
                           data=None,
                           message='Server error',
                           http_code=500)

    finally:
        session.close()

    


async def get_sources_by_type(source_type: SourceTypeEnum):
    # Search for source
    session = get_session()
    source_query = session.query(SourceModel)
    sources: List[SourceModel] = source_query.filter(
        SourceModel.source_type == source_type).all()
    session.close()

    return ServiceResponse(response_status='success',
                           data=[source.tojson() for source in sources],
                           message='Source list',
                           http_code=200)


async def get_sources():
    # Search for source
    session = get_session()
    source_query = session.query(SourceModel)
    sources: List[SourceModel] = source_query.order_by(
        SourceModel.created_at.desc()).all()
    session.close()

    return ServiceResponse(response_status='success',
                           data=[source.tojson() for source in sources],
                           message='Sources list',
                           http_code=200)


async def add_file_source(source_name: str, source_description: str,
                          source_type: SourceTypeEnum, source_domain: str,
                          source_file_content: Union[bytes, str]):
    # Search for source
    session = get_session()
    swift = get_swift_connection()
    file_id = uuid.uuid4().hex
    path = f'{source_name}_{file_id}'
    source = SourceModel(source_id=file_id,
                         source_name=source_name,
                         source_description=source_description,
                         source_type=source_type,
                         source_domain=source_domain,
                         source_file=path)
    try:
        session.begin()

        session.add(source)
        await swift.put(obj=path, contents=source_file_content)
        session.commit()
        return ServiceResponse(response_status='success',
                               data=source.tojson(),
                               message='Upload success',
                               http_code=500)
    except Exception as e:
        session.rollback()
        print(e)
        return ServiceResponse(response_status='error',
                               data=None,
                               message='Upload error',
                               http_code=500)
    finally:
        session.close()


async def add_non_file_source(
    source_name: str,
    source_description: str,
    source_type: SourceTypeEnum,
    source_url: str,
    source_domain: str,
):
    # Search for source
    session = get_session()
    source = SourceModel(source_id=uuid.uuid4().hex,
                         source_name=source_name,
                         source_description=source_description,
                         source_type=source_type,
                         source_url=source_url,
                         source_domain=source_domain)
    session.add(source)
    try:
        session.commit()
        return ServiceResponse(response_status='success',
                               data=source.tojson(),
                               http_code=201,
                               message='Source added')
    except Exception as e:
        print(e)
        return ServiceResponse(response_status='error',
                               data=None,
                               http_code=500,
                               message='Source added')
    finally:
        session.close()
    # source_query = session.query(SourceModel)
    # source: Union[SourceModel, None] = source_query.filter(SourceModel.source_id == source_id).first()
    # if not source:
    # return

    # swift = get_swift_connection()
    # cv_filename = cv.cv_filename
    # header, obj = swift.connection.get_object('cvs', cv_filename)
    # return header, obj