import functools

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import pytest
from sqlalchemy_media import StoreManager, FileSystemStore

from flasker.models.db import  Base
from flasker import create_app


base_url = 'http://localhost:5000/assets'
TEMP_PATH = '/tmp/sqlalchemy-media'


@pytest.fixture(scope='session')
def engine():

    return create_engine('sqlite:///:memory:')


@pytest.yield_fixture(scope='session')
def tables(engine):
    StoreManager.register(
        'fs',
        functools.partial(FileSystemStore, TEMP_PATH, base_url),
        default=True
    )
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.yield_fixture
def dbsession(engine, tables):
    """Returns an sqlalchemy session, and after the test tears down everything properly."""
    connection = engine.connect()
    # begin the nested transaction
    transaction = connection.begin()
    # use the connection with the already started transaction
    session = Session(bind=connection)

    yield session

    session.close()
    # roll back the broader transaction
    transaction.rollback()
    # put back the connection to the connection pool
    connection.close()

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    flask_app.config['TESTING'] = True

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!
#    shutil.rmtree(TEST_DATA_DIRECTORY)
    ctx.pop()

