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
        self.asana_pj_gid = os.getenv("ASANA_PJ_ID")
        self.api_client = asana.ApiClient(self.configuration)

    def get_multiple_workspaces(self) -> dict:
        workspaces_api_instance = asana.WorkspacesApi(self.api_client)
        opts = {
            'limit': 50, # int | Results per page. The number of objects to return per page. The value must be between 1 and 100.
            'opt_fields': "email_domains,is_organization,name,offset,path,uri", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.
        }

        try:
            # Get multiple workspaces
            api_response = workspaces_api_instance.get_workspaces(opts)
            for data in api_response:
                pprint(data)
        except ApiException as e:
            print("Exception when calling WorkspacesApi->get_workspaces: %s\n" % e)

    def get_multiple_projects(self) -> dict:
        """
        https://developers.asana.com/reference/getprojects
        """

        projects_api_instance = asana.ProjectsApi(self.api_client)
        opts = {
            'limit': 50, # int | Results per page. The number of objects to return per page. The value must be between 1 and 100.
            'workspace': self.asana_ws_gid, # str | The workspace or organization to filter projects on.
            'archived': False # bool | Only return projects whose `archived` field takes on the value of this parameter.
            # 'opt_fields': "archived,color,completed,completed_at,completed_by,completed_by.name,created_at,created_from_template,created_from_template.name,current_status,current_status.author,current_status.author.name,current_status.color,current_status.created_at,current_status.created_by,current_status.created_by.name,current_status.html_text,current_status.modified_at,current_status.text,current_status.title,current_status_update,current_status_update.resource_subtype,current_status_update.title,custom_field_settings,custom_field_settings.custom_field,custom_field_settings.custom_field.asana_created_field,custom_field_settings.custom_field.created_by,custom_field_settings.custom_field.created_by.name,custom_field_settings.custom_field.currency_code,custom_field_settings.custom_field.custom_label,custom_field_settings.custom_field.custom_label_position,custom_field_settings.custom_field.date_value,custom_field_settings.custom_field.date_value.date,custom_field_settings.custom_field.date_value.date_time,custom_field_settings.custom_field.default_access_level,custom_field_settings.custom_field.description,custom_field_settings.custom_field.display_value,custom_field_settings.custom_field.enabled,custom_field_settings.custom_field.enum_options,custom_field_settings.custom_field.enum_options.color,custom_field_settings.custom_field.enum_options.enabled,custom_field_settings.custom_field.enum_options.name,custom_field_settings.custom_field.enum_value,custom_field_settings.custom_field.enum_value.color,custom_field_settings.custom_field.enum_value.enabled,custom_field_settings.custom_field.enum_value.name,custom_field_settings.custom_field.format,custom_field_settings.custom_field.has_notifications_enabled,custom_field_settings.custom_field.id_prefix,custom_field_settings.custom_field.is_formula_field,custom_field_settings.custom_field.is_global_to_workspace,custom_field_settings.custom_field.is_value_read_only,custom_field_settings.custom_field.multi_enum_values,custom_field_settings.custom_field.multi_enum_values.color,custom_field_settings.custom_field.multi_enum_values.enabled,custom_field_settings.custom_field.multi_enum_values.name,custom_field_settings.custom_field.name,custom_field_settings.custom_field.number_value,custom_field_settings.custom_field.people_value,custom_field_settings.custom_field.people_value.name,custom_field_settings.custom_field.precision,custom_field_settings.custom_field.privacy_setting,custom_field_settings.custom_field.representation_type,custom_field_settings.custom_field.resource_subtype,custom_field_settings.custom_field.text_value,custom_field_settings.custom_field.type,custom_field_settings.is_important,custom_field_settings.parent,custom_field_settings.parent.name,custom_field_settings.project,custom_field_settings.project.name,custom_fields,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.id_prefix,custom_fields.is_formula_field,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.representation_type,custom_fields.text_value,custom_fields.type,default_access_level,default_view,due_date,due_on,followers,followers.name,html_notes,icon,members,members.name,minimum_access_level_for_customization,minimum_access_level_for_sharing,modified_at,name,notes,offset,owner,path,permalink_url,privacy_setting,project_brief,public,start_on,team,team.name,uri,workspace,workspace.name", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.
        }

        try:
            # Get multiple projects
            api_response = projects_api_instance.get_projects(opts)
            for data in api_response:
                pprint(data)
        except ApiException as e:
            print("Exception when calling ProjectsApi->get_projects: %s\n" % e)

    def get_multiple_tasks(self) -> dict:
        """
        https://developers.asana.com/reference/gettasks
        """
        # create an instance of the API class
        tasks_api_instance = asana.TasksApi(self.api_client)
        opts = {
            'limit': 100, # int | Results per page. The number of objects to return per page. The value must be between 1 and 100.
            #'offset': "eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9", # str | Offset token. An offset to the next page returned by the API. A pagination request will return an offset token, which can be used as an input parameter to the next request. If an offset is not passed in, the API will return the first page of results. *Note: You can only pass in an offset that was returned to you via a previously paginated request.*
            'project': self.asana_pj_gid, # str | The project to filter tasks on.
            #'section': "321654", # str | The section to filter tasks on.
            #'workspace': "321654", # str | The workspace to filter tasks on. *Note: If you specify `workspace`, you must also specify the `assignee` to filter on.*
            #'completed_since': '2012-02-22T02:06:58.158Z', # datetime | Only return tasks that are either incomplete or that have been completed since this time.
            #'modified_since': '2012-02-22T02:06:58.158Z', # datetime | Only return tasks that have been modified since the given time.  *Note: A task is considered “modified” if any of its properties change, or associations between it and other objects are modified (e.g.  a task being added to a project). A task is not considered modified just because another object it is associated with (e.g. a subtask) is modified. Actions that count as modifying the task include assigning, renaming, completing, and adding stories.*
            'opt_fields': "actual_time_minutes,approval_status,assignee,assignee.name,assignee_section,assignee_section.name,assignee_status,completed,completed_at,completed_by,completed_by.name,created_at,created_by,custom_fields,custom_fields.asana_created_field,custom_fields.created_by,custom_fields.created_by.name,custom_fields.currency_code,custom_fields.custom_label,custom_fields.custom_label_position,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.default_access_level,custom_fields.description,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.format,custom_fields.has_notifications_enabled,custom_fields.id_prefix,custom_fields.is_formula_field,custom_fields.is_global_to_workspace,custom_fields.is_value_read_only,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.people_value,custom_fields.people_value.name,custom_fields.precision,custom_fields.privacy_setting,custom_fields.representation_type,custom_fields.resource_subtype,custom_fields.text_value,custom_fields.type,custom_type,custom_type.name,custom_type_status_option,custom_type_status_option.name,dependencies,dependents,due_at,due_on,external,external.data,followers,followers.name,hearted,hearts,hearts.user,hearts.user.name,html_notes,is_rendered_as_separator,liked,likes,likes.user,likes.user.name,memberships,memberships.project,memberships.project.name,memberships.section,memberships.section.name,modified_at,name,notes,num_hearts,num_likes,num_subtasks,offset,parent,parent.created_by,parent.name,parent.resource_subtype,path,permalink_url,projects,projects.name,resource_subtype,start_at,start_on,tags,tags.name,uri,workspace,workspace.name", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.
        }

        try:
            # Get multiple tasks
            api_response = tasks_api_instance.get_tasks(opts)
            for data in api_response:
                pprint(data)
        except ApiException as e:
            print("Exception when calling TasksApi->get_tasks: %s\n" % e)



"""
test code
"""
a = AsanaAPI()
a.get_multiple_workspaces()
a.get_multiple_projects()
a.get_multiple_tasks()
