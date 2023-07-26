from passlib.context import CryptContext

pwd_content = CryptContext(schemes=["bcrypt"], deprecated= 'auto')

def hashPwd(password):

    hashed = pwd_content.hash(password)
    return hashed

def verifyPwd(password, hashed):
    return pwd_content.verify(password, hashed)


from datetime import datetime, timezone

def transform_to_utc_datetime(dt: datetime) -> datetime:
    return dt.astimezone(tz=timezone.utc)
