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

	CELERY_BROKER_URL = "redis://localhost:6379/1"
	CELERY_RESULT_BACKEND = "redis://"
	CELERYD_CONCURRENCY = 10

	REDIS_URL = "redis://localhost:6379/0"

	HEADER_SETTINGS={
		'user-agent':{
			'chrome': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
			'android': "android"
		}
		
	}
	UPLOAD_PATH = 'upload'