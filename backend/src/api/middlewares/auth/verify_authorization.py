from . import FastAPIUser
import jwt
import os
from dotenv import load_dotenv
from starlette.requests import Request
from starlette.authentication import AuthenticationError
from starlette.responses import JSONResponse
load_dotenv()


def verify_authorization_handler(
    header: str,
):
    # Split auth header
    try:
        auth_header = header['Authorization']
        print("Hello")
        [_, auth_token] = auth_header.split(' ')
        print(auth_token)
        decoded_token = jwt.decode(
            jwt=auth_token,
            key=os.getenv('JWT_SECRET', 'secret'),
            algorithms=['HS256']
        )
        print(decoded_token)
        scopes = [decoded_token['role']]
        print(scopes)
        user = FastAPIUser(
            user_id=decoded_token['user_id'],
            role=decoded_token['role']
        )
        return scopes, user

    except Exception as e:
        print(e)
        anonymous_user = FastAPIUser(
            user_id=None,
            role='anonymous'
        )
        return [], anonymous_user
    

def auth_error_handler(
    request: Request,
    error: AuthenticationError
): 
    return JSONResponse(
        content={
            'status': 'error',
            'data': None,
            'message': error
        },
        status_code=403
    )