import click
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash


from ..models.db import Base, engine
from ..models import User, NewsCard, NewsItems, Lab


supervisor_description = """
Dr. Fard is an Assistant Professor at the University of British Columbia (Okanagan Campus). Her research
interest lies at the intersection of Natural Language Processing and Software Engineering, more
specifically AI4SE. Dr. Fard and her team develop code intelligence models with a focus on low resource
languages and with less computational costs. Few shot learning, adapters, and (large) language models
are at the hearts of her works.\n
Dr. Fard teaches at the Master of Data Science Program, is a member of CITECH program and MMRI,
part of the Killam family of scholars, and an IEEE and ACM member. She is a strong advocate of Diversity
and Inclusion, specifically for underrepresented females in STEM.
"""

news1_body = """
Our emsejournal paper “Evaluating Pre-Trained Models for User Feedback Analysis in Software Engineering: A Study on Classification of App-Reviews” is online.
"""


news2_body = """
Our emsejournal paper “Evaluating Pre-Trained Models for User Feedback Analysis in Software Engineering: A Study on Classification of App-Reviews” is online.
"""

lab_summary = """
Focus of our lab is on developing new techniques to employ language models for code related tasks
"""


@click.command('init_db')
@with_appcontext
def init_db_command():
    Base.metadata.create_all(engine)
    click.echo('Database is created')

@click.command('add_members')
@with_appcontext
def db_mock_command():
    mohamad_dict = {
        "password":generate_password_hash("Mkh10594"),
        "first_name":"Mohamad",
        "last_name":"Khajezade",
        "role": "admin",
        "email":"khajezade.mohamad@gmail.com",
        "title": "PhD Candidate",
        "description":"sample desc.",
    }
    fard_dict = {
        "password":generate_password_hash("cqvDXAFShq8L"),
        "first_name":"Fatemeh",
        "last_name":"HendijaniFard",
        "role": "admin",
        "email":"fatemeh.fard@ubc.ca",
        "title": "Supervisor",
        "description":supervisor_description
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
        
    if len(NewsItems.get_news_list()) == 0:
        news1 = NewsItems(body=news1_body)
        news2 = NewsItems(body=news2_body)
        NewsItems.add_news(news1)
        click.echo("First news is added")
        NewsItems.add_news(news2)
        click.echo("Second news is added")
        
    if not NewsCard.get_news_fied():
        card = NewsCard(title='Lab News')
        NewsCard.add_card(card)
        click.echo("Card is added")
        
    if not Lab.get_lab():
        lab = Lab(title='About our Lab', summary=lab_summary)
        Lab.add_lab(lab)
        click.echo("Lab is added")
        

def init_app(app):
#    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(db_mock_command)
