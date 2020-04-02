import packet
import os

# Collect input variables from workflow
API_key = os.getenv("INPUT_API_KEY")
host_name = os.getenv("INPUT_HOST_NAME")
project_name = os.getenv("INPUT_PROJECT_NAME")
plan = os.getenv("INPUT_PLAN")
facility = os.getenv("INPUT_FACILITY")
operating_system = os.getenv("INPUT_OPERATING_SYSTEM")
user_ssh_keys = os.getenv("INPUT_USER_SSH_KEYS") or []
project_ssh_keys = os.getenv("INPUT_PROJECT_SSH_KEYS") or []

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

# Create a device with desired parameters matching top-level vars

device = manager.create_device(project_id=project_id, hostname=host_name,
                               plan=plan,
                               facility=facility,
                               operating_system=operating_system,
                               user_ssh_keys=user_ssh_keys,
                               project_ssh_keys=project_ssh_keys)

# Set outputs for action
print(f"::set-output name=device_id::{device.id}")
print(f"::set-output name=ip_addresses::{device.ip_addresses}")

# Profit
