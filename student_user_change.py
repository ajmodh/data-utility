import student
import utility
import json
from random import randint

username = 'username'
password = 'password'
user_url = utility.base_url + '/api/v1/user'
login_data = utility.login(username, password)
header_all = utility.get_headers(login_data)
student_data = student.get_students(header_all)

def get_username(student):
    username = student['person']['first_name'].lower() + '_' + student['person']['last_name'].lower() + '_' + str(randint(1,99))
    user_of_id = utility.requests.get(user_url + '/?username=' + username, headers=header_all).json()
    # print (username, user_of_id)
    print(user_of_id['meta']['total_count'] > 0)
    if (user_of_id['meta']['total_count'] > 0):
        get_username(student)
    return username

for istudent in student_data:
    username = get_username(student=istudent)
    header_all['Content-Type'] = 'application/json'
    data = {
             "person": {
                 "resource_uri": istudent['person']['resource_uri'],
                "user": {
                    "resource_uri": istudent['person']['user']['resource_uri'],
                    "username": username
                }
             }
            }
    utility.requests.patch(utility.base_url + istudent['resource_uri'], data = json.dumps(data), headers=header_all)