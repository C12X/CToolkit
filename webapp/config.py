class Config(object):
	pass

class ProdConfig(Config):
	pass

class DevConfig(Config):
	DEBUG = True
	SECRET_KEY = 'test'

	SQLALCHEMY_TRACK_MODIFICATIONS = True

	MONGODB_SETTINGS = {
		'db': 'test',
		'host': 'test',
		'port': 27017
	}

	CELERY_BROKER_URL = "amqp://guest:guest@localhost:5672//"
	CELERY_RESULT_BACKEND = "amqp://guest:guest@localhost:5672//"
	CELERYD_CONCURRENCY = 10