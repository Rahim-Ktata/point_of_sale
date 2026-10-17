from fastapi.testclient import TestClient
import pytest
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from app import models, schemas
from app.database import Base
from app.dependencies import get_session
from app.utils.Oauth2 import get_current_active_emp
from ..config import settings

from app.main import app



engine = create_engine(
    settings.TEST_DB_URL,
    # connect_args={"check_same_thread": False},
    # poolClass = StaticPool,   # use static pool for in memory db
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)






# @pytest.fixture(scope="function")
# def db_session():
#     """ create a new database session for each test function"""
#     Base.metadata.create_all(bind = engine) # create tables
#     # all our models inherits from Base
#     # so the data base session will be created with this
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#         Base.metadata.drop_all(bind = engine) # drop tables after test


# @pytest.fixture()
# def test_db():
#     Base.metadata.create_all(bind=engine)
#     yield
#     Base.metadata.drop_all(bind=engine)


# @pytest.fixture(scope="function")
# def test_employee(db_session):

#     def override_get_db():
#         yield db_session

#     app.dependency_overrides[get_session] = override_get_db
#     # telling the back to use the test db instead of the real one

#     with TestClient(app) as client:
#         yield client
#     app.dependency_overrides.clear()







def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

async def override_Oauth_dependency():
    return 1

@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    app.dependency_overrides[get_session] = override_get_db
    app.dependency_overrides[get_current_active_emp] = override_Oauth_dependency
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind = engine) # drop tables after test
        app.dependency_overrides.clear()





def get_emp_account_activation_token(test_db):
    return test_db.query(models.AccountActivation).filter(models.AccountActivation.employee_id==1).first().token

def get_emp_reset_password_token(test_db):
    return test_db.query(models.ResetPassword).filter(models.ResetPassword.employee_id==1).first().token