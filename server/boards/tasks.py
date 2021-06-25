from celery import shared_task


@shared_task
def check():
	print("working!!!")