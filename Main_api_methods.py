import requests
import numpy as np
detection_url='http://127.0.0.1:9999'
verification_endpoint='/check_person_images'
db_url="http://127.0.0.1:5555"
Db_signup_endpoint='/Database/add_student_to_db'
Db_add_to_lec_endpoint='/Database/add_student_to_lec'
db_student_info_endpoint='/Database/get_students_info/'
attendance_endpoint='/get_attendance'
abs_increase='/Database/increment_absence_count'
add_instructor='/Database/add_instructor'
get_students_by_ids='/Database/get_student_names_and_absences'

def get_student_info_by_ids(lec_id,lst_ids):

    url = db_url+get_students_by_ids
    payload = {
        'student_ids': lst_ids,
        'lec_id': lec_id
    }
    # Send a POST request to the API endpoint
    response = requests.post(url, json=payload)

    response_json = response.json()

    # Extract status and message from the response
    status = response_json.get('status')
    if status==True:
        data=response_json.get('student_info')
    else:
        data=response_json.get('message')
    # Return status and message
    return status, data

def add_instructor_api(username, password, email=None,lectures=None):
    endpoint = f"{db_url}{add_instructor}"
    payload = {
        'username': username,
        'password': password,
        'lectures': lectures,
        'email':email
    }

    try:
        response = requests.post(endpoint, json=payload)
        response_data = response.json()
        if response.status_code == 400 and not response_data.get('success'):
            if "Instructor already exists" in response_data.get('message', ''):
                return 400, {'success': False, 'message': 'Instructor already exists.'}
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.status_code, response_data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None, {'success': False, 'message': 'Request failed.'}
def Images_verification(imgs):
    images_array = []
    for image in imgs:
        image = image.resize((image.width//2, image.height//2))
        image = np.array(image)
        images_array.append((image).tolist())
    json_data={'imgs':images_array}
    print('Request sent.')
    response = requests.post(detection_url + verification_endpoint, json=json_data)
    Data = response.json()
    print(Data['Status'])
    return Data['Status'],Data['Data']


def add_student_to_db(email, username, password, encodings,major):
    url = db_url+"/Database/add_student_to_db"
    data = {
        "email": email,
        "username": username,
        "password": password,
        "encodings": encodings,
        "major":major
    }

    # Send a POST request to the API endpoint
    response = requests.post(url, json=data)

    response_json = response.json()

    # Extract status and message from the response
    status = response_json.get('status')
    message = response_json.get('message')

    # Return status and message
    return status, message

def login_verif(username,password):
    url = db_url+"/Database/user_info"
    data = {
        "username": username,
        "password": password,
    }

    # Send a POST request to the API endpoint
    response = requests.post(url, json=data)

    response_json = response.json()

    # Extract status and message from the response
    status = response_json.get('status')
    if status==True:
        data=response_json.get('data')
    else:
        data=response_json.get('message')
    # Return status and message
    return status, data

def teacher_login_verif(username,password):
    login_url = db_url+"/Database/authenticate_instructor"
    data = {
        "username": username,
        "password": password,
    }

    # Send a POST request to the API endpoint
    response = requests.post(login_url, json=data)

    response_json = response.json()

    # Extract status and message from the response
    status = response_json.get('authenticated')
    if status==True:
        data=response_json.get('lecture_details')
    else:
        data=response_json.get('message')
    # Return status and message
    return status, data
def add_student_to_lec(student_id,lec_id):
    url = db_url+Db_add_to_lec_endpoint
    data = {
    "lec_id":lec_id,
    "student_id":student_id
    }

    # Send a POST request to the API endpoint
    response = requests.post(url, json=data)

    response_json = response.json()

    # Extract status and message from the response
    status = response_json.get('status')
    message = response_json.get('message')

    # Return status and message
    return status, message
def get_students_enc_ids(lec_id):
    url = db_url+db_student_info_endpoint+lec_id
    # Send a POST request to the API endpoint
    response = requests.get(url)
    response_json = response.json()
    # Extract status and message from the response
    ids = response_json.get('ids')
    encodings = response_json.get('Encodings')
    # Return status and message
    print(ids)
    print(len(encodings))
    return ids, encodings

def get_attendance(lec_id):
    json_data = {'lec_id': lec_id}
    print('Requset sent')
    response = requests.post(detection_url + "/get_attendance", json=json_data)
    Data = response.json()
    if 'ids' in Data:
        return True,[Data['ids'],Data['all_ids']]
    else:
        return False,Data["error"]
def increase_abs_count(abs_student_ids,lec_id):
    status=True
    for id in abs_student_ids:
        json_data = {'id': id,'lec_id':lec_id}
        response = requests.post(db_url + abs_increase, json=json_data)
        Data = response.json()
        if not Data['status']:
            status=False
    return status
if __name__=='__main__':
    print(get_attendance("123"))
