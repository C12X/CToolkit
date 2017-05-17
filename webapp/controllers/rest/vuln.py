from flask import current_app
from flask_restful import Resource
# from .parsers import vuln_get_parser
from .parsers import vuln_post_parser
from .parsers import vuln_put_parser
from .parsers import vuln_delete_parser
from webapp.models import Vuln
from werkzeug.datastructures import FileStorage
import datetime
import requests
import json

class VulnApi(Resource):
	def get(self, title=None):
		if not title:
			vulns = Vuln.objects.order_by('date_created').all()
			vuln_list = []
			for i in vulns:
				vuln = {}
				# vuln['vuln_id'] = str(i.id)
				vuln['title'] = i.title
				vuln_list.append(vuln)
			return vuln_list
		else:
			vuln = Vuln.objects(title=title).first()
			if vuln:
				return {'title':vuln.title, 'exps':vuln.exploits}
			else:
				return {}

	def post(self, title=None):
		if not title:
			args = vuln_post_parser.parse_args()
			vuln = Vuln()
			vuln.title = args.title
			vuln.date_created = datetime.datetime.now()
			vuln.save(write_concern={"w":1, "j":True})
			return {'title': vuln.title}
		else:
			return {'error':'illegal param'}

	def put(self, title=None):
		if not title:
			return {'error':'illegal param'}

		# args: method,target,payload,cookie,useragent,proxy,exp_title,exp_index
		args = vuln_put_parser.parse_args()
		vuln = Vuln.objects(title=title).first()

		# create or update exploits
		if args.save:
			# create
			exp = {
				'exp_title': args.exp_title,
				'method': args.method,
				'target': args.target,
				'payload': args.payload,
				'cookie': args.cookie,
				'user_agent': args.user_agent,
				'content_type':args.content_type,
				'proxy': args.proxy,
			}
			if args.exp_index == -1:
				vuln.exploits.append(exp)
			# update
			else:
				vuln.exploits[args.exp_index] = exp
			vuln.save(write_concern={"w":1, "j":True})
			return exp

		# test payload without saving
		else:
			# headers
			headers = {
				'user-agent':args.user_agent.replace('\n','') if args.user_agent else current_app.config['HEADER_SETTINGS']['user-agent']['chrome'],
				'cookie':args.cookie.replace('\n',''),
				'Content-Type':args.content_type.replace('\n','') if args.content_type else 'application/x-www-form-urlencoded'
			}
			# proxy
			proxies = {
				'http':'http://'+args.proxy,
				'https':'https://'+args.proxy
			} if args.proxy else {}
			# start request
			try:
				# get
				if args.method == 'get':
					# print(args.target)
					r = requests.get(
						args.target,
						headers=headers,
						params=args.payload.replace('\n','').strip().encode('utf-8'),
						proxies=proxies,
						allow_redirects=False,
						stream=True)
				# post
				if args.method == 'post':
					r = requests.post(
						args.target,
						headers=headers,
						data=args.payload.replace('\n','').strip().encode('utf-8'),
						proxies=proxies,
						allow_redirects=False,
						stream=True)
				# file
				if args.method == 'file':
					files = json.loads(args.payload)
					data = []
					for name in files:
						# post file object
						if files[name].get('filename'):
							with open('upload/tmp','w') as f:
								f.write(files[name].get('content'))
							# format: (name, file-content, content-type)
							data.append((name,(files[name].get('filename'),open('upload/tmp'),files[name].get('content_type'))))

						# just post data instead of file object
						else:
							data.append(name,files[name].get('content'))
					# print(headers)
					r = requests.post(
						args.target,
						files=data,
						proxies=proxies,
						headers=headers,
						allow_redirects=False,
						stream=True)
			except BaseException as e:
				return {'content':'request error: '+str(e)}
			# read content from stream
			content = b''
			try:
				for block in r.iter_content(1024):
					if not block:
						break
					content += block
			except BaseException as e:
				print('got error when reading stream from response: '+str(e))
				# thought get error, content was saved
				pass
			# encoding
			encoding = r.encoding if r.encoding else 'utf-8'
			encoding = 'utf-8' if 'ISO' in encoding else encoding
			content = content.replace(b'\x00',''.encode(encoding))
			# encoding bytes content to string
			try:
				content = content.decode(encoding)
			except BaseException as e:
				print('got error when encoding bytes: '+str(e))
				# may not utf-8 and gb2312
				try:				
					content = content.decode('gbk')
				except BaseException as e:
					print('not gbk: '+str(e))
					# cannot encode correctly
					content = str(content)
			rheaders = ''
			for i in r.headers:
				rheaders += i+': '+r.headers[i]+'\n'
			# content = rheaders+'\n\n'+r.text

			content = rheaders+'\n\n'+str(content)

			return {'content':content, 'headers':headers}


	def delete(self, title=None):
		if not title:
			return {'error':'illegal param'}
		else:
			args = vuln_delete_parser.parse_args()
			vuln = Vuln.objects(title=title).first()
			if vuln.exploits.pop(args.exp_index):
				vuln.save(write_concern={"w":1, "j":True})
				return {'exp_index': args.exp_index}
			else:
				return {'error': 'unknow index or list'}

# s2-016/17 http://www.cnblogs.com/jusker/p/4136406.html
# s2-032 http://www.cnblogs.com/nayu/p/5441757.html