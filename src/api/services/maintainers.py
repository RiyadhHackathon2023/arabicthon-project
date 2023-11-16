from typing import Union, List
import jwt
from datetime import datetime, timedelta
from psycopg2.errors import UniqueViolation
from .utils.auth import hashpwd
import bcrypt
import os
from dotenv import load_dotenv
from ..requests.maintainer import CreateMaintainerRequest, UpdateMaintainerRequest
from ..requests.source import LoginRequest
from ...db.models import MaintainerModel
from ...db.session import get_session
from .responses.service_response import ServiceResponse
import uuid
load_dotenv()

async def login_maintainer(req: LoginRequest):
    session = get_session()

    maintainer_query = session.query(MaintainerModel)
    maintainer: Union[MaintainerModel, None] = maintainer_query.filter(MaintainerModel.email == req.email).first()
    if maintainer:
        # Found
        # Check passowrd
        password = req.password.encode()
        print(password, maintainer.password.encode())
        print(f"CANDIDATE HASHED PASSWORD: {maintainer.password.encode()}")
        correct_pw = bcrypt.checkpw(password, maintainer.password.encode())
        if correct_pw:
            jwt_payload = {
                'maintainer_id': maintainer.maintainer_id,
                'role': 'maintainer',
                'exp': datetime.utcnow() + timedelta(days=1) # token expires in 1 day
            }
            token = jwt.encode(jwt_payload, os.getenv('JWT_SECRET', 'secret'), algorithm="HS256")

            session.close()
            return ServiceResponse(
                response_status='success',
                data={
                    'token': token.decode(),
                    'maintainer_id': maintainer.maintainer_id
                },
                message='Maintainer login success',
                http_code=200,
            )
        session.close()
        return ServiceResponse(
                response_status='error',
                data=None,
                message='Incorrect credentials',
                http_code=400,
            )
        
    else:
        session.close()
        return ServiceResponse(
                response_status='error',
                data=None,
                message='Maintainer not found',
                http_code=404,
            )


async def create_maintainer(maintainer: CreateMaintainerRequest):
    # Find maintainer by email
    if await get_maintainer_by_email(maintainer.email) != None:
        return ServiceResponse(
            response_status='error',
            data=None,
            message='Maintainer alread exists',
            http_code=400
        )
    session = get_session()
    salt = bcrypt.gensalt()
    password = maintainer.password.encode()
    hashed_password = bcrypt.hashpw(password, salt)
    db_maintainer = MaintainerModel(
        maintainer_id=uuid.uuid4().hex,
        name = maintainer.name,
        email=maintainer.email,
        password=hashed_password.decode()
    )

    try:
        session.add(db_maintainer)
        session.commit()
    except UniqueViolation as e:
        session.close()
        return ServiceResponse(
            response_status='error',
            data=None,
            message='Maintainer alread exists',
            http_code=400
        )
    except Exception as e:
        session.close()

        return ServiceResponse(
            response_status='error',
            data=None,
            message='Internal error',
            http_code=500
        )

    candidate_json = db_maintainer.tojson()
    session.close()
    return ServiceResponse(
            response_status='success',
            data=candidate_json,
            message='Maintainer created',
            http_code=201
        )

async def get_maintainer(maintainer_id: str):
    """
        Fetch maintainer from database and serialize it as a reponse
    """
    print(maintainer_id)
    session = get_session()
    maintainer_query = session.query(MaintainerModel)
    maintainer: Union[MaintainerModel, None] = maintainer_query.filter(MaintainerModel.maintainer_id == maintainer_id).first()
    session.close()
    if maintainer:
        return ServiceResponse(
            data=maintainer.tojson(),
            http_code=200,
            message='Maintainers',
            response_status='success',
        )
    else:
        return ServiceResponse(
            data=None,
            http_code=400,
            message='No maintainer found',
            response_status='error',
        )

async def get_maintainers():
    """
        Fetch maintainesr from database and serialize it as a reponse
    """
    session = get_session()
    maintainer_query = session.query(MaintainerModel)
    maintainers_db: Union[List(MaintainerModel), None] = maintainer_query.all()
    session.close()

    return ServiceResponse(
        data=[maintainer_db.tojson() for maintainer_db in maintainers_db],
        http_code=200,
        message='Maintainers list',
        response_status='success',
    )

    
async def get_maintainer_by_email(email: str):
    """
        Fetch maintainer from database and serialize it as a reponse
    """
    session = get_session()
    maintainer_query = session.query(MaintainerModel)
    maintainer: Union[MaintainerModel, None] = maintainer_query.filter(MaintainerModel.email == email).first()
    session.close()
    if maintainer:
        return maintainer.tojson()
    else:
        return None

async def update_maintainer(maintainer_id: str, updated_maintainer: UpdateMaintainerRequest):
    """
        Update maintainer
    """
    session = get_session()
    maintainer_query = session.query(MaintainerModel)
    maintainer: Union[MaintainerModel, None] = maintainer_query.filter(MaintainerModel.maintainer_id == maintainer_id).first()
    
    print(maintainer)
    if maintainer:
        # Update fields
        # session.add(candidate)
        maintainer.name = updated_maintainer.name if updated_maintainer.name is not None else maintainer.name
        maintainer.family_name = updated_maintainer.family_name if updated_maintainer.family_name is not None else maintainer.family_name
        maintainer.password = hashpwd(updated_maintainer.password) if updated_maintainer.password is not None else maintainer.password
        maintainer.phone_number = updated_maintainer.phone_number if updated_maintainer.phone_number is not None else maintainer.phone_number
        
        session.commit()
        return maintainer.tojson()
    else:
        session.close()
        return None
    
async def delete_maintainer(maintainer_id: str):
    session = get_session()
    maintainer_query = session.query(MaintainerModel)
    maintainer: Union[MaintainerModel, None] = maintainer_query.filter(MaintainerModel.maintainer_id == maintainer_id).first()
    if maintainer:
        session.delete(maintainer)
        session.commit()
        return True
    else:
        session.close()
        return False
    
