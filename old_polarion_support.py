# importing libraries
from pylero.work_item import ContainersTools, InstalledTools

def check_ci(wi_type,name):
    """This function checks if the particular work item already exists in configuration management database
    input: work item type 
           name of the work item/ configuration item
    output: returns work item id if found else return none 
    """
    if wi_type == "container_tools":
        fields = ["work_item_id", "repository", "imageid", "tools"]
        query="type:containerstools"
        workitem_list = ContainersTools.query(query,fields)
        for w in workitem_list:
            if name == w.imageid:
                return w.work_item_id
    elif wi_type == "installed_tools":
        fields = ["work_item_id", "pkgname", "repo"]
        query="type:installedtools"
        workitem_list = InstalledTools.query(query,fields)
        for w in workitem_list:
            if name == w.toolname:
                return w.work_item_id
    else:
        print("'%s' is invalid. wi_type not created or not present in the system" % wi_type)
        return None

def create_containertools(repo,imageid,tools):
    check = check_ci("container_tools",imageid)
    if check:
        print("updating the esisting CI")
        id = check
        ci = ContainersTools(project_id="ISO26262RiskProject", work_item_id=id)
        ci.repository = repo
        ci.tools = tools
        ci.imageid = imageid
        ci.update()
    else:
        ci = ContainersTools.create("ISO26262RiskProject", imageid, "container tools CI", "open", source_repo_status = "pending")
        ci.repository = repo
        ci.tools = tools
        ci.imageid = imageid
        ci.update()

def create_installedtools(repo,pkgname):
    check = check_ci("installed_tools",pkgname)
    if check:
        print("updating the esisting CI")
        id = check
        ci = ContainersTools(project_id="ISO26262RiskProject", work_item_id=id)
        ci.pkgname = repo
        ci.repo = repo
        ci.update()
    else:
        ci = ContainersTools.create("ISO26262RiskProject", pkgname, "installed tools CI", "open", source_repo_status = "pending")
        ci.pkgname = repo
        ci.repo = repo
        ci.update()


