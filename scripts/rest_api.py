import json
import requests
import os


# AUTH_ENDPOINT = "http://127.0.0.1:8000/api/auth/jwt/"

AUTH_ENDPOINT = "http://127.0.0.1:8000/api/auth/register/"
REFRESH_ENDPOINT = AUTH_ENDPOINT + "jwt/refresh/"
ENDPOINT = "http://127.0.0.1:8000/api/status/"

image_path = os.path.join(os.getcwd() , "iitb.jpeg")


data = {
#     # "username" : "ishan",
#     "username" : "ishan@gmail.com",
#
#     "password" : "codechef",
#     "password2" : "codechef"


    # To create new user

    "username" : "iitb",
    "email" : "iitb@gmail.com",
    "password" : "codechef",
    "password2" : "codechef"
}

headers = {
    "content-Type" : "application/json" ,
    # "Authorization" : "JWT " + 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImlzaGFuIiwiZXhwIjoxNTYwOTY5NjU2LCJlbWFpbCI6InNoYWhpc2hhbjcxMDk4QGdtYWlsLmNvbSIsIm9yaWdfaWF0IjoxNTYwOTY5MzU2fQ.dA3Wcc6bqTMqMEcuUiXsVqgP39_ziUqVlOdNsrSAIEg'
}

data = json.dumps(data)
r = requests.post(AUTH_ENDPOINT, data=data , headers=headers)
# print(r.json())

token = r.json()#['token']
print(token)
# print(token)
# print(token)

# refresh_data = {
#     'token' : token
# }
#
# new_response = requests.post(REFRESH_ENDPOINT , data = json.dumps(refresh_data) , headers=headers)
# new_token = new_response.json()#['token']
# print(new_token)


# for posting(creating) elements with content only (need json)

# headers = {
#     'content-type' : 'application/json',
#     'Authorization' : 'JWT ' + token,
# }
#
# post_data = json.dumps({"content":"new random!!!!!"})
# posted_response = requests.post(ENDPOINT , data=post_data , headers=headers)
# print(posted_response.text)

# for posting elements with images (doesn't need json)

# headers = {
#     # 'content-Type' : 'application/json',
#     "Authorization" : "JWT " + token,
# }
#
# with open(image_path,'rb') as image:
#     file_data = {
#         'image' : image
#     }
#
# post_data = {}
# posted_response = requests.post(ENDPOINT , data=post_data , headers=headers , files=file_data)
# print(posted_response.text)

# for updating elements
# headers = {
#     # 'content-type' : 'application/json',
#     'Authorization' : 'JWT ' + token,
# }
#
# data = {"content" : "updated 21 21 !!"}
# posted_response = requests.put(ENDPOINT + str(21) + "/" , data=data , headers=headers)
# print(posted_response.text)

# get_endpoint = ENDPOINT + str(21) + "/"
# post_data = json.dumps({'content':'new post random'})
#
# r = requests.get(get_endpoint)
# print(r.text)
#
# r2 = requests.get(ENDPOINT)
# print(r2.status_code)
#
#
# post_headers = {
#     'content-type' : 'application/json',
#
# }
# post_response = requests.post(ENDPOINT , data=post_data , headers=post_headers)
# print(post_response.text)


# def do_img(method='get', data={} ,is_json=True , img_path=None):
#     headers = {}
#     if is_json:
#         data = json.dumps(data)
#     if img_path is not None:
#         with open(image_path , 'rb') as image:
#             file_data = {'image' : image}
#             r = requests.request(method, ENDPOINT, data=data, files=file_data)
#     else:
#         r = requests.request(method , ENDPOINT, data=data , headers=headers)
#     print(r.text)
#     print(r.status_code)
#     return r
#
# # do_img(method='post', data={'user':1,'content':''},is_json=False , img_path=image_path)
#
# do_img()
#



# def do(method='get', data={} ,is_json=True): # no need of parameter 'pk'
#     headers = {}
#     if is_json:
#         headers['content-type'] = 'application/json'
#         data = json.dumps(data)
#     # r = requests.request(method , ENDPOINT + "?pk=" + str(pk) , data=data)
#
#     r = requests.request(method , ENDPOINT, data=data , headers=headers)
#     print(r.text)
#     print(r.status_code)
#     return r
#








# do(data={'pk':15}) # no method arg is passed so calling 'get'

# do(method='delete', data={'pk':10})

# do(method='put' , data={'pk':10 , 'user':1 , 'content':'updated 10'})

# do(method='post' , data={'user':1 , 'content':'created 13'})
