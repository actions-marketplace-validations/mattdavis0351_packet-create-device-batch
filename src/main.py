import packet
import os

# Collect input variables from workflow
API_key = os.getenv("INPUT_API_KEY") or "No key supplied"
host_name = os.getenv("INPUT_HOST_NAME")
project_name = os.getenv("INPUT_PROJECT_NAME") or "default"
plan = os.getenv("INPUT_PLAN") or "default"
facility = os.getenv("INPUT_FACILITY") or "default"
operating_system = os.getenv("INPUT_OPERATING_SYSTEM") or "default"
user_ssh_keys = os.getenv("INPUT_USER_SSH_KEYS") or []
project_ssh_keys = os.getenv("INPUT_PROJECT_SSH_KEYS") or []
batch_quantity = os.getenv("INPUT_QUANTITY") or 1
spot_instance = os.getenv("INPUT_SPOT_INSTANCE") or False
spot_price_max = os.getenv("INPUT_SPOT_PRICE_MAX") or 1


# Check if required inputs have been received
if API_key == "No key supplied":
    raise ValueError(
        f"Cannot supply empty API key. Current key is: %s" % API_key)

if project_name == "default":
    raise ValueError("Must supply an existing project ID for this device")

if plan == "default":
    raise ValueError("Must specify a server type as value for PLAN")

if facility == "default":
    raise ValueError("Must specify a geographical location for FACILITY")

if operating_system == "default":
    raise ValueError("Must specify an operating system for this device")

if user_ssh_keys == "default" and project_ssh_keys == "default":
    raise ValueError(
        "Must supply at least one user ssh key, or at least one project ssh key")


# Store project_id for later API call
project_id = ""

# Create Packet.com API client
manager = packet.Manager(auth_token=API_key)

# Check for valid project name
projects = manager.list_projects()

for p in projects:
    if p.name == project_name:
        project_id = p.id
    else:
        raise ValueError(
            "Supplied project name does not match any valid projects for this API key")

# Parse hostnames
name_arr = host_name.split(',')
hostnames = []
for name in name_arr:
    hostnames.append(name.strip().replace(' ', '-'))

# Create a device batch with desired parameters matching top-level vars
params = [
    {
        "hostnames": hostnames,
        "facility": facility,
        "plan": plan,
        "operating_system": operating_system,
        "quantity": batch_quantity,
        "user_ssh_keys": user_ssh_keys,
        "project_ssh_keys": project_ssh_keys,
        "spot_instance": spot_instance,
        "spot_price_max": spot_price_max
    }
]
batch = manager.create_batch(project_id=project_id, params=params)

# Profit
