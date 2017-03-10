from flask_restful import Api
from flask_celery import Celery

rest_api = Api()
celery = Celery()