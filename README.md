### Tech Stack

- Python 3.6
- Postgress 11
- AWS for media
### Installation and setup,

- Clone the repo and switch to master

- setup a local virtual environment and activate it

- install dependencies using `pip install -r requirements.txt`

- setup a postgres database

- Copy contents of the `.env_sample` file and switch the values to your environment specific credentials

- source your environment file into the shell

- Migrate database tables using `python manage.py migrate`

- Run te local server using `python manage.py runserver`


### Deployments

- This application can be deployed to any server that has python and postgres
