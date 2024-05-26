from celery import Celery
from kombu import Queue, Exchange


def make_celery(fapp):
    # Create Celery instance
    celery = Celery(
        fapp.import_name,
        broker=fapp.config['CELERY_BROKER_URL'],
        backend=fapp.config['RESULT_BACKEND'],
        broker_connection_retry_on_startup=True
    )

    # Define an exchange
    default_exchange = Exchange(name='celery', type='direct')

    celery.conf.task_queues = (
        Queue(name='email', exchange=default_exchange, routing_key='task.emails'),
        Queue(name='other_task', exchange=default_exchange, routing_key='task.other_tasks'),
    )
    celery.conf.task_routes = {
        'celery_tasks.send_email_task': {'queue': 'email'},
        'celery_tasks.other_task': {'queue': 'other_task'},
    }

    # Update Celery configs with Flask configs
    celery.conf.update(fapp.config)

    # Create ContextTask class
    class ContextTask(celery.Task):
        abstract = True

        def __call__(self, *args, **kwargs):
            with fapp.app_context():
                return super(ContextTask, self).__call__(*args, **kwargs)

    # Update Celery Task class with custom ContextTask
    celery.Task = ContextTask

    # Set the discovery of tasks to auto
    celery.autodiscover_tasks(['celery_tasks'], force=True)

    return celery
