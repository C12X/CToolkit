from webapp.extensions import celery
import time

@celery.task()
def test():
	time.sleep(5)
	return "after 5s!"

@celery.task()
def scan_port():
	pass