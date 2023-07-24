#Our lab Backend server

## For the postgress database
export MODE='deployment'

## For running the app
export FLASK_APP=flasker:create_app
falsk init_db
flask add_members
flask run