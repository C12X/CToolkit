from flask_mongoengine import MongoEngine
mongo = MongoEngine()

class PortInfo(mongo.DynamicDocument):
	date_created = mongo.DateTimeField(required=True)

class DirInfo(mongo.Document):
	date_created = mongo.DateTimeField(required=True)

class Project(mongo.Document):
	project_name = mongo.StringField(required=True)
	date_created = mongo.DateTimeField(required=True)
	port_info = mongo.ReferenceField(PortInfo)

class Task(mongo.Document):
	task_id = mongo.StringField(required=True)
	category = mongo.StringField(required=True)
	target = mongo.StringField(required=True)
	date_created = mongo.DateTimeField(required=True)
	status = mongo.StringField(required=True)
	project = mongo.ReferenceField(Project,required=True)