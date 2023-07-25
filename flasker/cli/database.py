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
    mohamad_dict = {
        "password":generate_password_hash("cqvDXAFShq8L"),
        "first_name":"Mohamad",
        "last_name":"Khajezade",
        "email":"khajezade.mohamad@gmail.com",
        "title": "PhD Candidate",
        "description":"sample desc."
    }
    fard_dict = {
        "password":generate_password_hash("cqvDXAFShq8L"),
        "first_name":"Fatemeh",
        "last_name":"HendijaniFard",
        "email":"fatemeh.fard@ubc.ca",
        "title": "Supervisor",
        "description":"Sample desc."
    }
    if not User.get_member(mohamad_dict["email"]):
        user1 = User(**mohamad_dict)
        User.add_avatar(user1, 'mohamad.jpg')
        User.add_member(user1)
        click.echo("First member is added")

    if not User.get_member(fard_dict["email"]):
        user2 = User(**fard_dict)
        User.add_avatar(user2, 'supervisor.jpg')
        User.add_member(user2)
        click.echo("Second member is added")


def init_app(app):
#    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(db_mock_command)
