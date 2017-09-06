import utility
student_all_data = []


def student_request(url, headers):
    student_data = utility.requests.get(url, headers=headers).json()
    student_all_data.extend(student_data['objects'])

    if (student_data['meta']['next'] != None):
        student_request(utility.base_url + student_data['meta']['next'], headers)
    return student_all_data

def get_students(headers):
    url_student = utility.base_url + '/api/v1/student'
    return student_request(url_student, headers)

def get_students_detail(students):
    # return [{'name': student['person']['first_name'] + ' ' + student['person']['last_name'], 'parent_login': student['person']['father']['user']['username']} if student['person']['father'] else {'parent_login': '' }\
    #         for student in students]
    return [{'gr_no.': student['gr_number'], \
             'name': student['person']['first_name'] + ' ' + student['person']['last_name'], \
             'username': student['person']['user']['username'], \
             'parent_login': student['person']['first_name'].lower() + '-' + 'parent'} \
            for student in students]

def main(username, password):
    login_data = utility.login(username, password)
    header_all = utility.get_headers(login_data)
    student_data = get_students(header_all)
    return get_students_detail(student_data)

users = main('username', 'password')

# workbook = utility.xlsxwriter.Workbook('student_detail_with_username.xlsx')
workbook = utility.xlsxwriter.Workbook('poppp1.xlsx')
worksheet = workbook.add_worksheet()

# Add a bold format to use to highlight cells.
bold = workbook.add_format({'bold': 1})

# Write some data headers.
# worksheet.write('A1', 'GR. No.', bold)
worksheet.write('A1', 'Name', bold)
worksheet.write('B1', 'Username', bold)
worksheet.write('C1', 'Parent Login', bold)

# Start from the first cell. Rows and columns are zero indexed.
row = 1
col = 0

# Iterate over the data and write it out row by row.
for item in users:
    # worksheet.write(row, col, item['gr_no'])
    worksheet.write(row, col, item['name'])
    worksheet.write(row, col +1, item['username'])
    worksheet.write(row, col +2, item['parent_login'])
    row += 1

workbook.close()