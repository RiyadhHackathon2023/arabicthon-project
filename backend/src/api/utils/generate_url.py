import subprocess
import os
import re

def generate_cv_url(
    cv_filename: str,
    expiration_time: int = 600
):
    
    pass
    # account_id = os.getenv('SWIFT_ACCOUNT_ID')
    # container = os.getenv('CVS_CONTAINER')
    # version = f"v{os.getenv('SWIFT_AUTH_VERSION')}"

    # key_cmd = [
    #     'swift',
    #     'post',
    #     '-m',
    #     '"Temp-URL-Key:secret"'
    # ]
    # swift_cli_command = [
    #     'swift',
    #     'tempurl',
    #     'get',
    #     f"2800",
    #     f'/{version}/{account_id}/{container}/{cv_filename}',
    #     'secret'
    # ]

    # print(" ".join(swift_cli_command))

    # try:
    #     subprocess.check_output(key_cmd)
    #     path = subprocess.check_output(swift_cli_command)
    #     url = os.getenv('SWIFT_ENDPOINT')+path.decode()
    #     url = re.sub('\n', '', url)
    #     print(url)
    #     return url
    # except Exception as e:
    #     print(e)
    #     return None