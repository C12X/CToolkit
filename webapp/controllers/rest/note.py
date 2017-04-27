from flask_restful import Resource
from .parsers import note_get_parser
from .parsers import note_post_parser
from .parsers import note_put_parser
from webapp.models import Note
from flask import abort
import datetime

class NoteApi(Resource):
	def get(self, note_id=None):
		# args: code
		args = note_get_parser.parse_args()
		# get specific note content
		if note_id and args.code:
			return {'code': Note.objects(id=note_id).only('code').first().code}
		# want code without note_id
		if not note_id and args.code:
			return {'error':'illegal param'}
		# get children notes
		if note_id and not args.code:
			notes = Note.objects(parent=note_id).only('title','has_child','date_created').order_by('date_created').all()
		# get all notes without parent
		else:
			notes = Note.objects(parent=None).order_by('date_created').all()
		note_list = []
		for i in notes:
			note = {}
			note['note_id'] = str(i.id)
			note['title'] = i.title
			note['has_child'] = i.has_child
			note['children'] = []
			note['date_created'] = i.date_created.strftime('%Y-%m-%d %H:%M:%S')
			note_list.append(note)
		return note_list

	def post(self, note_id=None):
		#args: title
		args = note_post_parser.parse_args()

		#save in mongodb
		note = Note()
		note.title = args.title
		note.date_created = datetime.datetime.now()

		if note_id:
			#get parent
			parent = Note.objects(id=note_id).first()
			note.parent = parent
			#change parent note state
			parent.update(has_child=True)

		note.save(write_concern={"w":1, "j":True})

		return {'note_id': str(note.id)}

	def put(self, note_id=None):
		# note_id is required
		if not note_id:
			return {'error':'illegal param'}

		#args: code
		args = note_put_parser.parse_args()
		note = Note.objects(id=note_id).first()
		note.update(code=args.code)

		return {'status': 'save completed'}

	def delete(self, note_id=None):
		if not note_id:
			return {'error':'illegal param'}

		note = Note.objects(id=note_id).first()
		if not note:
			abort(404)

		#delete child note
		children = Note.objects(parent=note)
		children.delete()
		#check parent state
		parent = Note.objects(id=note_id)
		if not parent:
			parent.update(has_child=False)
		#finally delete specific note
		note.delete()
		return {'status': 'delete completed'}
