from celery import Celery

# Configura Celery apuntando a Redis
celery = Celery(
    'modulo_slice_manager',
    broker='redis://192.168.200.200:6379/0',  
    backend='redis://192.168.200.200:6379/0'
)

celery.conf.task_routes = {
    'app.services.vm_service.create_vm_task': {'queue': 'vm_tasks'}
}


