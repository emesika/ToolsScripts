import importlib
from pylero.work_item import ContainersTools, InstalledTools

# Create a dictionary of work item types and their corresponding classes
WORK_ITEM_CLASSES = {
    "container_tools": ContainersTools,
    "installed_tools": InstalledTools,
    # Add more work item classes as needed
}

"""
# Get the list of work item types from the Polarion configuration
config = Configuration()
work_item_types = config.get_valid_field_values("workitem-type")

# Create a list to store the work item classes
work_item_classes = []

# Import the work item modules and retrieve the classes dynamically
for work_item_type in work_item_types:
    module_name = work_item_type.lower()  # Assuming module names are lowercase
    try:
        module = importlib.import_module(module_name)
        work_item_class = getattr(module, work_item_type)
        work_item_classes.append(work_item_class)
    except (ImportError, AttributeError):
        print(f"Failed to import {work_item_type} module or retrieve class.")

# Create the WORK_ITEM_CLASSES dictionary dynamically
WORK_ITEM_CLASSES = {cls.__name__.lower(): cls for cls in work_item_classes}
"""

def check_ci(wi_type, **kwargs):
    try:
        workitem_class = globals()[wi_type.capitalize()]
        fields = workitem_class.get_field_names()
        workitem_list = workitem_class.query(f"type:{wi_type}", fields)
        for w in workitem_list:
            if "title" in kwargs and kwargs["title"] == getattr(w, "title"):
                return w.work_item_id
    except KeyError:
        print("'%s' is invalid. wi_type not created or not present in the system" % wi_type)
    return None

def create_workitem(wi_type, **kwargs):
    try:
        workitem_class = WORK_ITEM_CLASSES[wi_type]
        workitem = workitem_class.create(**kwargs)
        workitem.update()
        print("Created/updated the work item:", workitem.work_item_id)
    except KeyError:
        print("'%s' is invalid. wi_type not created or not present in the system" % wi_type)

def create_workitem_generic(wi_type, **kwargs):
    check = check_ci(wi_type, kwargs.get("title"))
    if check:
        print("Updating the existing CI")
        workitem_class = WORK_ITEM_CLASSES[wi_type]
        workitem = workitem_class(project_id="ISO26262RiskProject", work_item_id=check)
    else:
        workitem_class = WORK_ITEM_CLASSES[wi_type]
        workitem = workitem_class(**kwargs)
    create_workitem(wi_type, workitem=workitem)

"""
Examples:

    create_workitem_generic("container_tools", title=repo+imageid repo=repo, imageid=image, tools=tools)
    create_workitem_generic("installed_tools", title=repo+package repo=repo, pkgname=package)

"""
