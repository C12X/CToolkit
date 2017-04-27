from webapp.extensions import (
	celery,
	redis_store)
from webapp.models import Task
from subprocess import Popen, PIPE, CalledProcessError
import time, json

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
	cmds = [
		# -sn:ping扫描,即主机发现
		# -n :不对IP进行域名反向解析
		# -Pn:不检测主机存活
		# -PE:使用ICMP echo
		# is alive
		'sudo nmap {} -v -sn -PE -n -oX {} --min-hostgroup 1024 --min-parallelism 1024',
		# default common port
		'sudo nmap {} -v --open --system-dns -Pn --script=banner,http-title -oX {} --min-hostgroup 1024 --min-parallelism 1024',
		# all port
		'sudo nmap {} -v -p 1-65535 --open --system-dns -Pn --script=banner,http-title -oX {} --min-hostgroup 1024 --min-parallelism 1024',
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