import bcrypt

def hashpwd(password):
    salt = bcrypt.gensalt()
    password = password.encode()
    hashed_password = bcrypt.hashpw(password, salt)
    return hashed_password.decode()