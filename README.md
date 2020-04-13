# Origin Takehome

### Pre-Requisites
1. Python 3.8

### How to run locally
1. If you use a virtualenv, create it using python 3.8
2. Access your virtualenv
3. Install requirements `pip install -r requirements/requirements.txt`
4. Run `python app.py` and the server will be running at port 5000

### How to run on Docker with uWSGI and Nginx
1. Install Docker and docker-compose
2. Run `docker-compose up -d`
3. The server will be running at port 8080 with nginx as reverse proxy
4. This config is very similar to what we could use in production on Amazon ECS or Fargate, for example.

### How to run tests
1. Install testing requirements `pip install -r requirements/testing.txt`
2. Run `pytest` from the root folder of the project
3. If you want to see code coverage, you can run `pytest --cov=origin_test tests/`


### Project Structure
1. This project uses Flask-RestPlus in order to manage the APIs and facilitate their creation (Flask-Restplus is now being replaced by flask-restx);
2. Even though it is not being used in the project, I added sentry on the requirements, because it is really useful in production to trace bugs and exceptions;
3. It uses `uwsgi` on production. uWSGI is used when we have a NGINX (or any other reversed proxy) in front of in order for it to talk with our application;
4. The project also uses `pytest` for unit and integration tests;
5. The configs are loaded from the `config` folder, which is separated by environment (I usually have four environments: production, develop (or staging), development (localhost) and testing). The `default.py` file loads configs that are the same no matter what environment we are in. I usually use those files to load credentials from a vault (for example Amazon SSM) in order to avoid sensitive information on GitHub;
6. The project uses `Marshmallow` from serialization and deserialization of JSON objects in Python. All schemas are located in the `schemas` folder. I also created a new decorator called `check_body` in the `utils/validations` folder. It can be added before any route definition in order to validate the body before everything;
7. There is also a `responses.py` file, that I created to make it possible for us to create custom responses based on some http errors (for example, bad request);
8. There is a custom `api.py` within the `utils` folder. This custom api allows us to validate that all requests and responses has to be of type `application/json`, it also dumps all our responses that marshmallow deserialize.
9. Finally, there are two other folders: `apis` that stores all APIs and routes definitions, and `services` that acts as `controllers`.


### Endpoints
1. There is an endpoint `/health_check/`, that can be used by Kubernetes or Amazon ECS or Load Balancers in order to guarantee that the server is running;
2. The main endpoint is `/risk_profile/`, it receives the body as specified in the documentation and returns the risk profile for that profile.


### Important
1. All endpoints need the `/` in the end, otherwise the server will return `301 - Redirect`
