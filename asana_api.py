#!/usr/bin/env python3
import os
import asana
from asana.rest import ApiException
from pprint import pprint
from dotenv import load_dotenv
load_dotenv()

class AsanaAPI:

    def __init__(self):
        self.configuration = asana.Configuration()
        self.configuration.access_token = os.getenv("ASANA_TOKEN")
        self.asana_ws_gid = os.getenv("ASANA_WS_ID")
        self.asana_pj_gid = os.getenv("ASANA_PJ_ID") # hstn-famliy-project
        self.asana_section_todo = os.getenv("ASANA_SECTION_TODO")
        self.asana_section_inprogress = os.getenv("ASANA_SECTION_INPROGRESS")
        self.asana_section_completed = os.getenv("ASANA_SECTION_COMPLETED")
        self.asana_section_archive2025 = os.getenv("ASANA_SECTION_ARCHIVED_2025")
        self.api_client = asana.ApiClient(self.configuration)

    def get_multiple_workspaces(self) -> dict:
        """
        https://developers.asana.com/reference/getworkspaces
        """
        ret = {"ok": False}

        workspaces_api_instance = asana.WorkspacesApi(self.api_client)
        opts = {
            'limit': 1
        }

        try:
            # 一つ決め打ち
            api_response = workspaces_api_instance.get_workspaces(opts)
            for data in api_response:
                response = data

            ret = {"ok": True, "respones": response}

        except ApiException as e:
            ret = {"ok": False, "response": str(e)}

        return ret

    def get_multiple_projects(self) -> dict:
        """
        https://developers.asana.com/reference/getprojects
        """
        ret = {"ok": False}

        # 一つ決め打ち
        projects_api_instance = asana.ProjectsApi(self.api_client)
        opts = {
            'limit': 1,
            'workspace': self.asana_ws_gid
        }

        try:
            # Get multiple projects
            api_response = projects_api_instance.get_projects(opts)
            for data in api_response:
                response = data
            ret = {"ok": True, "respones": response}

        except ApiException as e:
            ret = {"ok": False, "response": str(e)}

        return ret

    def get_multiple_tasks(self, section:str = None, exclude_completed: bool = False, offset:str = None) -> dict:
        """
        https://developers.asana.com/reference/gettasks
        """
        ret = {"ok": False}

        tasks_api_instance = asana.TasksApi(self.api_client)
        opts = {
            'limit': 100,
            **({'project': self.asana_pj_gid} if section is None else {}),
            **({'section': section} if section is not None else {}),
            **({'completed_since': 'now'} if exclude_completed else {}),
            **({'offset': offset} if offset is not None else {}),
            'opt_fields': "approval_status,assignee.name,completed,completed_at,due_at,due_on,memberships.section.name,modified_at,name,notes,offset,parent,parent.created_by,parent.name,path,permalink_url,tags.name,uri"
            }

        print (opts)

        try:
            api_response = tasks_api_instance.get_tasks(opts)
            tasks = []
            for data in api_response:
                tasks.append(data)
            ret = {"ok": True, "response": tasks}

        except ApiException as e:
            ret = {"ok": False, "response": str(e)}

        return ret


"""
test code
"""
a = AsanaAPI()
#ret = a.get_multiple_workspaces()
#print (ret)

#ret = a.get_multiple_projects()
#print (ret)

ret = a.get_multiple_tasks(exclude_completed=True)
#print (ret)
for task in ret["response"]:
    print (task)
    print ()