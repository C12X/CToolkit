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

	CELERY_BROKER_URL = "redis://localhost:6379/0"
	CELERY_RESULT_BACKEND = "redis://"
	CELERYD_CONCURRENCY = 10

	REDIS_URL = "redis://localhost:6379/0"