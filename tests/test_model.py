from io import BytesIO

from sqlalchemy_media import StoreManager, File

from flasker.models import User, Post, Message


def test_user(dbsession):
    user1 = User(
        password='123456',
        first_name="Mohamad",
        last_name="Khajezade",
        title='PhD',
        description="A PhD Candidate"
    )
    user2 = User(
        password='123456',
        first_name="example",
        last_name="example",
        email="example@example.com",
        title="Masters",
        description="Example description"
    )
    
    sample_content = open('tests/p1.png', "rb").read()
    with StoreManager(dbsession):
        user1.avatar = BytesIO(sample_content)
        dbsession.add(user1)
        dbsession.flush()
        assert 1 == 1
        
    dbsession.add(user2)
    dbsession.flush()
    assert 1 == 1


def test_message_attachment(dbsession):
    message1 = Message(title="example1", body="this is example")
    sample_content = b'Simple text.'

    with StoreManager(dbsession):
        message1.attachment = BytesIO(sample_content)
        dbsession.add(message1)
        dbsession.flush()

