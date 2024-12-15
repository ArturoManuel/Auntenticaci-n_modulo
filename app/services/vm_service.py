# Datos hardcodeados por el momento


from app.celery_worker import celery
import time  # Simula el tiempo de creación de la VM
vms = [
    {"name": "VM1", "ip_worker": "192.168.1.101", "status": "running"},
    {"name": "VM2", "ip_worker": "192.168.1.102", "status": "stopped"}
]

def get_all_vms():
    return vms

# def create_vm(vm):
#     for existing_vm in vms:
#         if existing_vm["name"] == vm.name:
#             raise HTTPException(status_code=400, detail="VM already exists")
#     new_vm = {"name": vm.name, "ip_worker": vm.ip_worker, "status": vm.status}
#     vms.append(new_vm)
#     return {"message": "VM created", "vm": new_vm}



# Definir la tarea para crear la VM
@celery.task(name='app.services.vm_service.create_vm_task')
def create_vm_task(vm_data):
    # Simular la creación de la VM, por ejemplo, puedes hacer aquí la lógica que creará la VM en el worker.
    print(f"Creando VM en el worker {vm_data['ip_worker']} con el nombre {vm_data['name']}")
    time.sleep(5)  # Simula una tarea que tarda 5 segundos
    return {"message": f"VM {vm_data['name']} creada con éxito en {vm_data['ip_worker']}"}


def delete_vm(vm_name):
    global vms
    vms = [vm for vm in vms if vm["name"] != vm_name]
    return {"message": f"VM {vm_name} deleted"}

def update_vm(ip_worker, vm_name, vm):
    for existing_vm in vms:
        if existing_vm["name"] == vm_name and existing_vm["ip_worker"] == ip_worker:
            existing_vm["name"] = vm.name
            existing_vm["ip_worker"] = vm.ip_worker
            existing_vm["status"] = vm.status
            return {"message": f"VM {vm_name} updated"}
    raise HTTPException(status_code=404, detail="VM not found")
