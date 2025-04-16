#!/usr/bin/env python3
import sys
import os
import asana
from asana.rest import ApiException
from pprint import pprint
from dotenv import load_dotenv
load_dotenv()

if len(sys.argv) > 1:
    user_gid = sys.argc[1]
else:
    user_gid = "me"

configuration = asana.Configuration()
configuration.access_token = os.getenv('ASANA_TOKEN')
api_client = asana.ApiClient(configuration)

users_api_instance = asana.UsersApi(api_client)
opts = {
    'opt_fields': "email,name,photo,photo.image_1024x1024,photo.image_128x128,photo.image_21x21,photo.image_27x27,photo.image_36x36,photo.image_60x60,workspaces,workspaces.name", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.
}

try:
    api_response = users_api_instance.get_user(user_gid, opts)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UsersApi->get_user: %s\n" % e)
