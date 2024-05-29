import requests
import urllib

oauthToken = ""
user_name = 'lakshmi@corp.kobai.io'

tenants_url = 'https://saturn1.azure.kobai.io/user-mgmt-svcs/auth/tenants?'
user_name_query_params={ 'userName' : user_name}
tenants_response = requests.get(tenants_url+urllib.parse.urlencode(user_name_query_params))
print(tenants_response.content)

tenant_id = "ba3dd6d5-8522-45a6-bfff-03e46f0c6fc5"
token_url = 'https://saturn1.azure.kobai.io/user-mgmt-svcs/auth/oauth/devicecode'
token_request_payload={
  "tenantId" : tenant_id,
  "oauthToken" : oauthToken,
  "userName" : user_name
}
token_response = requests.post(token_url, json=token_request_payload)
access_token = token_response.content.decode()
print(access_token)

profile_url = 'https://saturn1.azure.kobai.io/user-mgmt-svcs/user/profile'
profile_response = requests.get(profile_url, headers={'Authorization': 'Bearer '+access_token})
print(profile_response.content)
