from webapp.extensions import (
	celery,
	redis_store)
from webapp.models import Task
from subprocess import Popen, PIPE, CalledProcessError
import time, os

@celery.task()
def test(sec):
	sec = int(sec)
	time.sleep(sec)
	print(test.request)
	return "after {}s!".format(sec)

@celery.task(bind=True)
def test_callback(self, result):
	print("test!!!!!")

@celery.task()
def scan(args):
	time.sleep(10)
	#args: category, target, level, project_id
	return {'result':{'test1':1,'test2':2}}

@celery.task()
def save_result(result, task_id):
	task = Task.objects(id=task_id).first()
	task.result = result
	task.save(write_concern={"w":1, "j":True})

@celery.task()
def run_nmap(target, task_id, level):
	# make output dir
	if not os.path.exists('/tmp/nmap-output'):
		os.makedirs('/tmp/nmap-output')
	cmds = [
		# -sn:ping扫描,即主机发现
		# -n :不对IP进行域名反向解析
		# -P0:跳过主机存活检测直接扫端口
		# -PE:使用ICMP echo
		# is alive
		'nmap -v -sn -PE -n --min-hostgroup 1024 --min-parallelism 1024 {} -oX {}',
		# default common port
		'nmap -v --open --system-dns -P0 --script=banner,http-title --min-hostgroup 1024 --min-parallelism 1024 {} -oX {}',
		# all port
		'nmap -v -p 1-65535 --open --system-dns -P0 --script=banner,http-title --min-hostgroup 1024 --min-parallelism 1024 {} -oX {}',
	]
	path = '/tmp/nmap-output/{}.xml'.format(task_id)
	cmd = cmds[level].format(target, path)
	stdout = ''
	with Popen(cmd.split(' '), stdout=PIPE) as p:
		for line in p.stdout:
			stdout+=line.decode('utf-8')
			redis_store.hset('task_stdout', task_id, stdout)

	if p.returncode != 0:
		raise CalledProcessError(p.returncode, p.args)

	return {'path':path}