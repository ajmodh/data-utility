import utility
import string
staff_all_data = []


def staff_request(url, headers):
    staff_data = utility.requests.get(url, headers=headers).json()
    staff_all_data.extend(staff_data['objects'])

    if (staff_data['meta']['next'] != None):
        staff_request(utility.base_url + staff_data['meta']['next'], headers)
    return staff_all_data


def get_staff(headers):
    url_staff = utility.base_url + '/api/v1/staff'
    return staff_request(url_staff, headers)


def get_staff_detail(staff):
    return [{'name': staff['person']['first_name'] + ' ' + staff['person']['last_name'], \
             'username': staff['person']['user']['username']} \
            for staff in staff]


def main(username, password):
    login_data = utility.login(username, password)
    header_all = utility.get_headers(login_data)
    staff_data = get_staff(header_all)
    return get_staff_detail(staff_data)

users = main('username', 'password')

workbook = utility.xlsxwriter.Workbook('stafff_detail_with_username_sec.xlsx')
worksheet = workbook.add_worksheet()

# Add a bold format to use to highlight cells.
bold = workbook.add_format({'bold': 1})

# Write some data headers.
worksheet.write('A1', 'Name', bold)
worksheet.write('B1', 'Username', bold)

# Start from the first cell. Rows and columns are zero indexed.
row = 1
col = 0

# Iterate over the data and write it out row by row.
for item in users:
    worksheet.write(row, col, item['name'])
    worksheet.write(row, col + 1, item['username'])
    row += 1

workbook.close()

