#!/usr/bin/env python3
import os
import asana
from asana.rest import ApiException
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

        try:
            api_response = tasks_api_instance.get_tasks(opts)
            tasks = []
            for data in api_response:
                tasks.append(data)
            ret = {"ok": True, "response": tasks}

        except ApiException as e:
            ret = {"ok": False, "response": str(e)}

        return ret

    def get_a_task(self, task_gid:str = None) -> dict:
        ret = {"ok": False}
        if task_gid is None:
            ret = {"ok": False, "response": "task_gid required"}
            return ret

        tasks_api_instance = asana.TasksApi(self.api_client)
        opts = {
            'opt_fields': "actual_time_minutes,approval_status,assignee,assignee.name,assignee_section,assignee_section.name,assignee_status,completed,completed_at,completed_by,completed_by.name,created_at,created_by,custom_fields,custom_fields.asana_created_field,custom_fields.created_by,custom_fields.created_by.name,custom_fields.currency_code,custom_fields.custom_label,custom_fields.custom_label_position,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.default_access_level,custom_fields.description,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.format,custom_fields.has_notifications_enabled,custom_fields.id_prefix,custom_fields.is_formula_field,custom_fields.is_global_to_workspace,custom_fields.is_value_read_only,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.people_value,custom_fields.people_value.name,custom_fields.precision,custom_fields.privacy_setting,custom_fields.representation_type,custom_fields.resource_subtype,custom_fields.text_value,custom_fields.type,custom_type,custom_type.name,custom_type_status_option,custom_type_status_option.name,dependencies,dependents,due_at,due_on,external,external.data,followers,followers.name,hearted,hearts,hearts.user,hearts.user.name,html_notes,is_rendered_as_separator,liked,likes,likes.user,likes.user.name,memberships,memberships.project,memberships.project.name,memberships.section,memberships.section.name,modified_at,name,notes,num_hearts,num_likes,num_subtasks,parent,parent.created_by,parent.name,parent.resource_subtype,permalink_url,projects,projects.name,resource_subtype,start_at,start_on,tags,tags.name,workspace,workspace.name", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.
        }

        try:
            api_response = tasks_api_instance.get_task(task_gid, opts)
            ret = {"ok": True, "response": api_response}
        except ApiException as e:
            ret = {"ok": False, "response": str(e)}

        return ret

    def create_a_task(self, task_name:str = None, task_notes:str = None, tags:str = None, due_on:str = None) -> dict:
        ret = {"ok": False}
        if task_name is None or task_notes is None:
            ret = {"ok": False, "response": "task_name and task_notes required"}
            return ret

        tasks_api_instance = asana.TasksApi(self.api_client)
        body = {"data": {
                        "projects": self.asana_pj_gid,
                        "name": task_name, 
                        "notes": task_notes,
                        **({"tags": [tags]} if tags is not None else {}),
                        **({"due_on": due_on} if due_on is not None else {}),
                        }
                }
        opts = {"opt_fields": "name, notes, due_on, tags"}

        try:
            api_response = tasks_api_instance.create_task(body, opts)
            ret = {"ok": True, "response": api_response}

        except ApiException as e:
            ret = {"ok": False, "response": str(e)}

        return ret
