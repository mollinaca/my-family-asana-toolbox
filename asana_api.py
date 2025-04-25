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
        self.asana_pj_gid = os.getenv("ASANA_PJ_ID")
        self.asana_section_todo = os.getenv("ASANA_SECTION_TODO")
        self.asana_section_inprogress = os.getenv("ASANA_SECTION_INPROGRESS")
        self.asana_section_completed = os.getenv("ASANA_SECTION_COMPLETED")
        self.asana_section_archive2025 = os.getenv("ASANA_SECTION_ARCHIVED_2025")
        self.asana_tag_bot_checked = os.getenv("ASANA_TAG_BOT_CHECKED")
        self.api_client = asana.ApiClient(self.configuration)
        self.asana_opt_fields_full = "actual_time_minutes,approval_status,assignee,assignee.name,created_at,completed,completed_at,completed_by,completed_by.name,created_by,created_by.name,custom_field,custom_field.date_value,custom_field.date_value.date,custom_field.date_value.date_time,custom_field.display_value,custom_field.enabled,custom_field.enum_options,custom_field.enum_options.color,custom_field.enum_options.enabled,custom_field.enum_options.name,custom_field.enum_value,custom_field.enum_value.color,custom_field.enum_value.enabled,custom_field.enum_value.name,custom_field.id_prefix,custom_field.is_formula_field,custom_field.multi_enum_values,custom_field.multi_enum_values.color,custom_field.multi_enum_values.enabled,custom_field.multi_enum_values.name,custom_field.name,custom_field.number_value,custom_field.representation_type,custom_field.text_value,custom_field.type,dependency,dependency.created_by,dependency.name,dependency.resource_subtype,duplicate_of,duplicate_of.created_by,duplicate_of.name,duplicate_of.resource_subtype,duplicated_from,duplicated_from.created_by,duplicated_from.name,duplicated_from.resource_subtype,follower,follower.name,hearted,hearts,hearts.user,hearts.user.name,html_text,is_editable,is_edited,is_pinned,liked,likes,likes.user,likes.user.name,name,new_approval_status,new_date_value,new_dates,new_dates.due_at,new_dates.due_on,new_dates.start_on,new_enum_value,new_enum_value.color,new_enum_value.enabled,new_enum_value.name,new_multi_enum_values,new_multi_enum_values.color,new_multi_enum_values.enabled,new_multi_enum_values.name,new_name,new_number_value,new_people_value,new_people_value.name,new_resource_subtype,new_section,new_section.name,new_text_value,num_hearts,num_likes,offset,old_approval_status,old_date_value,old_dates,old_dates.due_at,old_dates.due_on,old_dates.start_on,old_enum_value,old_enum_value.color,old_enum_value.enabled,old_enum_value.name,old_multi_enum_values,old_multi_enum_values.color,old_multi_enum_values.enabled,old_multi_enum_values.name,old_name,old_number_value,old_people_value,old_people_value.name,old_resource_subtype,old_section,old_section.name,old_text_value,path,permalink_url,previews,previews.fallback,previews.footer,previews.header,previews.header_link,previews.html_text,previews.text,previews.title,previews.title_link,project,project.name,resource_subtype,source,sticker_name,story,story.created_at,story.created_by,story.created_by.name,story.resource_subtype,story.text,tags,tag.name,target,target.created_by,target.name,target.resource_subtype,task,task.created_by,task.name,task.resource_subtype,text,type,uri"

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
            'opt_fields': self.asana_opt_fields_full
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
        """
        https://developers.asana.com/reference/gettask
        """
        ret = {"ok": False}
        if task_gid is None:
            ret = {"ok": False, "response": "task_gid required"}
            return ret

        tasks_api_instance = asana.TasksApi(self.api_client)
        opts = {'opt_fields': self.asana_opt_fields_full}

        try:
            api_response = tasks_api_instance.get_task(task_gid, opts)
            ret = {"ok": True, "response": api_response}
        except ApiException as e:
            ret = {"ok": False, "response": str(e)}

        return ret

    def create_a_task(self, task_name:str = None, task_notes:str = None, tags:list = None, due_on:str = None) -> dict:
        """
        https://developers.asana.com/reference/createtask
        """
        ret = {"ok": False}
        if task_name is None or task_notes is None:
            ret = {"ok": False, "response": "task_name and task_notes required"}
            return ret

        tasks_api_instance = asana.TasksApi(self.api_client)
        body = {"data": {
                        "projects": self.asana_pj_gid,
                        "name": task_name, 
                        "notes": task_notes,
                        **({"tags": tags} if tags is not None else {}),
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

    def update_a_task(self, task_gid:str = None, task_name:str = None, task_notes:str = None, assignee_section:str = None) -> dict:
        """
        https://developers.asana.com/reference/updatetask
        """
        ret = {"ok": False}
        if task_gid is None:
            ret = {"ok": False, "response": "task_gid required"}
            return ret

        tasks_api_instance = asana.TasksApi(self.api_client)
        body = {"data": {
                        "projects": self.asana_pj_gid,
                        **({"name": task_name} if task_name is not None else {}),
                        **({"notes": task_notes} if task_notes is not None else {}),
                        **({"assignee_section": assignee_section} if assignee_section is not None else {})
                        }
                }
        opts = {"opt_fields": "name, notes, due_on, tags"}

        try:
            api_response = tasks_api_instance.update_task(body, task_gid, opts)
            ret = {"ok": True, "response": api_response}

        except ApiException as e:
            ret = {"ok": False, "response": str(e)}

        return ret

    def get_stories_from_a_task(self, task_gid:str = None, offset:str = None) -> dict:
        """
        https://developers.asana.com/reference/getstoriesfortask
        """
        stories_api_instance = asana.StoriesApi(self.api_client)
        opts = {
            'limit': 100,
            'opt_fields': self.asana_opt_fields_full,
            **({"offset": offset} if offset is not None else {}),
        }

        try:
            api_response = stories_api_instance.get_stories_for_task(task_gid, opts)
            ret = {"ok": True, "response": api_response}
        except ApiException as e:
            ret = {"ok": False, "response": str(e)}

        return ret

    def add_a_tag_to_a_task(self, task_gid:str = None, tag_gid:str = None) -> dict:
        """
        https://developers.asana.com/reference/addtagfortask
        """
        tasks_api_instance = asana.TasksApi(self.api_client)

        if tag_gid is None:
            body = {"data": {"tag": self.asana_tag_bot_checked}}
        else:
            body = {"data": {"tag": tag_gid}}

        try:
            api_response = tasks_api_instance.add_tag_for_task(body, task_gid)
            ret = {"ok": True, "response": api_response}
        except ApiException as e:
            ret = {"ok": False, "response": str(e)}

        return ret

    def add_a_task_to_section(self, task_gid:str = None, section_gid:str = None) -> dict:
        """
        https://developers.asana.com/reference/addtaskforsection
        """
        sections_api_instance = asana.SectionsApi(self.api_client)
        opts = {
            'body': {"data": {"task": task_gid}}
        }

        try:
            api_response = sections_api_instance.add_task_for_section(section_gid, opts)
            ret = {"ok": True, "response": api_response}
        except ApiException as e:
            ret = {"ok": False, "response": str(e)}

        return ret
