## Docker installation
### Overview
The major tools involved in this project are; [djangorestframework](https://www.django-rest-framework.org/) (DRF) and [Django](https://www.djangoproject.com/) itself. And as such it follows the basic structure of a Django app.

The app uses Serializers from the DRF, streamlining the generation of JSON output from the Django models in the app.

In order to get it up and running quickly, you should have;
- You should have [docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/) installed. 
- Copy .env.example to .env and pass the necessary parameters. 

Modify the parameters in `services.db.environment` of the docker-compose.yml config file with the appropriate
- POSTGRES_DB
- POSTGRES_USER
- POSTGRES_PASSWORD

Having them match your database configurations in `.env`.

### Quickstart
- In your terminal, run (pass `-d` if you want to run the command in the background).<br/>
`$ docker-compose up`

Visit `BASE_URL/v1` (eg. http://0.0.0.0:8000/v1) in your browser to visit the root API. You should see by now the list of accessible endpoints.
Note:
If you already have PostgreSQL running on the default port of 5432 then 
you might want to stop it before you run this docker instance (`pg_ctlcuster` maybe ?)

