import pytest
import warnings
from app.users.models import User
from app import database

warnings.filterwarnings("ignore", category=DeprecationWarning)

@pytest.fixture(scope='module')
def setup():
    # setting up test
    session = database.get_session()
    yield session
    # after test finish tearingdown
    queryset = User.objects.filter(email='bereded@gmail.com')
    if queryset.count() != 0:
        queryset.delete()
    session.shutdown()

def test_create_user(setup):
    #session = setup
    User.create_user(email ='bereded@gmail.com', password = 'bereded@vblp')

def test_duplicate_User(setup):
    with pytest.raises(Exception):
        User.create_user(email ='bereded@gmail.com', password = 'bereded@vblp')

def test_invalid_email(setup):
    with pytest.raises(Exception):
        User.create_user(email='bereded@gmail', password='bereded@vblp')

def test_valid_password(setup):
    queryset = User.objects.filter(email='bereded@gmail.com')
    assert queryset.count() == 1
    user_obj = queryset.first()
    assert user_obj.verify_password('bereded@vblp') == True
    assert user_obj.verify_password('bereded@vbl') == False
# def test_assert():
#     assert True is True

# def test_equal():
#     assert 1 == 1

# def test_invalid_assert():
#     with pytest.raises(AssertionError):
#         assert True is not True