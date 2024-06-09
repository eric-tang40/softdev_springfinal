# softdev_springfinal

Collaborators: Eric Tang, Tejas Siddaramaiah, Jason Lei, Aiden Tan

# Billboard

# Roles

# Description

# APIs

https://rapidapi.com/LDVIN/api/billboard-api
- Path: '/top-100'

https://rapidapi.com/Glavier/api/spotify23/
- Path: '/search'

# Launch Codes

## Install the Prerequisites

sudo apt update; sudo apt install build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev curl \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

curl https://pyenv.run | bash

export PATH="$HOME/.pyenv/bin:$PATH"
      eval "$(pyenv init --path)"
      eval "$(pyenv virtualenv-init -)"
    
pyenv install –list

pyenv update

pyenv install 3.11.5

pyenv local 3.11.5

python -m venv env_3.11.5

## Running Virtual Env

source env_3.11.5/bin/activate (Mac/Linux) or env_3.11.5\Scripts\activate (Windows)

pip install --upgrade pip-tools pip setuptools wheel
pip-compile --upgrade --generate-hashes --output-file requirements_env/main.txt requirements_env/main.in
pip-compile --upgrade --generate-hashes --output-file requirements_env/dev.txt requirements_env/dev.in

pip-sync requirements_env/main.txt requirements_env/dev.txt

## Run the Website

For the secrets.json, we have given a template that you must follow to be able to properly run the website. We have added an additional line for the api key to be given by the user with the project files.

## Database Code

IMPORTANT: You must comment out two lines of code before migrating the database models.

First, in billboard/billboard/settings.py, in the Installed Apps: 'django.contrib.admin'. We have left a comment denoting this.

Second, in billboard/billboard/urls.py, in the URL Patterns: path('admin/', admin.site.urls). We have also left a comment denoting this.

python manage.py makemigrations

python manage.py migrate

python manage.py runserver

Go to http://localhost:8000

IMPORTANT: You must uncomment out the two lines of code after migrating the database models.

## Vue.js Code

source env_3.11.5/bin/activate (Mac/Linux) or env_3.11.5\Scripts\activate (Windows) (Make sure your environment is active)

nodeenv --node=20.11.1 --prebuilt env_node_20.11.1

deactivate

source env_node_20.11.1/bin/activate

cd billboard_vue/

npm install

npm run dev