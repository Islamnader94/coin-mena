from coinMena.celery import app as celery_app

@celery_app.task
def query_every_five_mins():
    pass