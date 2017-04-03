from flask_restful import Api
from flask_celery import Celery
from flask_redis import FlaskRedis


rest_api = Api()
celery = Celery()
redis_store = FlaskRedis()