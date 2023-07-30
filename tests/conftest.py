import pytest
from ..config import Setting
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..database import Base,get_db
from ..fast4 import app
from fastapi.testclient import TestClient
from jose import JWTError, jwt
from datetime import datetime, timedelta
from .. import models

SQL_DB_URL = f"""{Setting.DB_HOSTNAME}://{Setting.DB_USERNAME}:{Setting
    .DB_PASSWORD}@{Setting.DB_URL}:{Setting.DB_PORT}/{Setting.DB_NAME}_test"""

engine = create_engine(SQL_DB_URL)
#Base.metadata.create_all(bind = engine)

testingsessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


#this is to make a clean table each time we test db
@pytest.fixture(scope = "session")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = testingsessionlocal()
    try:
        yield db
    finally:
        db.close()

#client = TestClient(app)

@pytest.fixture(scope = "session")
def client(session):
    def override_get_db():
        db = testingsessionlocal()
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)



@pytest.fixture(scope = "session")
def test_user(client, session):
    user_data = {
        "name" : "bff",
        "password" : "S1m|Ep@55w0Rd",
        "items" : ["nothing"]
    }
    res = client.post("/users", json=user_data)
    usr = session.query(models.ap).filter(models.ap.name == "bff").first()

    user_data['id'] = usr.id
    #print(usr.id)
    return user_data


def create_token (payload:dict):
    copy = payload.copy()

    expire = datetime.utcnow() + timedelta(minutes = Setting.ACCESS_TOKEN_EXPIRY_MINUTES)
    copy.update({"exp" : expire})

    encoded_jwt = jwt.encode(copy, Setting.SECRET, algorithm = Setting.ALGORITHM)

    return encoded_jwt

@pytest.fixture(scope = "session")
def token(test_user):
    T =create_token({"id": str(test_user['id'])})
    #payload = jwt.decode(T, Setting.SECRET, algorithms = [Setting.ALGORITHM])
    #print(payload.get('id'))
    return T

@pytest.fixture(scope = "session")
def authorized_user(token, client):
    client.headers = {
        **client.headers,
        "Authorization" : f"Bearer {token}"
    }
    return client


@pytest.fixture(scope = "session")
def create_posts(session, test_user):
    post_list=[{
    "title": "title1", "content": "content for t1", "user_id":test_user['id']
    },{
    "title": "title2", "content": "this must be different", "user_id":test_user['id']
    },{
    "title": "title3", "content": "just a content", "user_id":test_user['id']
    }]

    def post_models (post):
        return models.post(**post)

    posts = list(map(post_models, post_list))
    session.add_all(posts)
    session.commit()
    return session.query(models.post).all()


@pytest.fixture(scope = "session")
def post_id(session):
    return session.query(models.post).filter(models.post.title == "title1").first()
