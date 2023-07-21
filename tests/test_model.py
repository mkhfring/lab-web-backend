from io import BytesIO

from sqlalchemy_media import StoreManager, File

from flasker.models import User, Post, Message


def test_user(dbsession):
    message1 = Message(title="example1", body="this is example")
    message2 = Message(
        title="example2",
        body="this is example2",
        reply_to=message1
    )
    user1 = User(
        user_name='Mohamad',
        password='123456',
        first_name="Mohamad",
        last_name="Khajezade",
        sent_messages=[message1]
    )
    user2 = User(
        user_name='example',
        password='123456',
        first_name="example",
        last_name="example",
        received_messages=[message2]
    )
    dbsession.add(user1)
    dbsession.add(user2)
    dbsession.flush()
    assert len(user1.sent_messages) > 0
    assert len(user2.received_messages) > 0
    assert user1.sent_messages[0].title == 'example1'
    assert user2.received_messages[0].title == 'example2'


def test_message_attachment(dbsession):
    message1 = Message(title="example1", body="this is example")
    sample_content = b'Simple text.'

    with StoreManager(dbsession):
        message1.attachment = BytesIO(sample_content)
        dbsession.add(message1)
        dbsession.flush()

