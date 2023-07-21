import click
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash

from ..models.db import Base, engine
from ..models import User


@click.command('init_db')
@with_appcontext
def init_db_command():
    Base.metadata.create_all(engine)
    click.echo('Database is created')

@click.command('add_members')
@with_appcontext
def db_mock_command():
    user1_dict = {
        "user_name":"example",
        "password":generate_password_hash("123456"),
        "first_name":"example",
        "last_name":"example",
        "phone_number":"123456",
        "email":"example@example.com"
    }
    user2_dict = {
        "user_name":"admin",
        "password":generate_password_hash("123456"),
        "first_name":"admin",
        "last_name":"admin",
        "phone_number":"123456",
        "email":"admin@example.com"
    }
    if not User.get_member(user1_dict["user_name"]):
        user1 = User(**user1_dict)
        User.add_member(user1)
        click.echo("First member is added")

    if not User.get_member(user2_dict["user_name"]):
        user2 = User(**user2_dict)
        User.add_member(user2)
        click.echo("Second member is added")


def init_app(app):
#    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(db_mock_command)
