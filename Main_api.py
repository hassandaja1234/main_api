from flask import Flask, request, jsonify,send_file
from PIL import Image
from flask_cors import CORS
from Main_api_methods import get_student_info_by_ids,add_instructor_api,teacher_login_verif,get_attendance,increase_abs_count,add_student_to_lec,Images_verification,add_student_to_db,login_verif
from methods import convert_to_rgb,read_image_to_bytes
from io import BytesIO,StringIO
import csv
import tempfile

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
@app.route('/add_instructor', methods=['POST'])
def add_instructor_endpoint():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email=data.get('email')
    lectures = data.get('lectures')

    if not username or not password:
        return jsonify({'success': False, 'message': 'Username and password are required'}), 400

    status_code, response = add_instructor_api(username, password,email, lectures)

    if status_code is None:
        return jsonify(response), 500
    return jsonify(response), status_code
@app.route('/take_attendance', methods=['POST'])
def take_attendance():
    lec_id = request.form['lec_id']
    print(lec_id)
    status,data=get_attendance(lec_id)
    print(status)
    if not status:
        return jsonify({"status":status,"msg":"Error"})

    abs_student_ids = data[0]
    status = increase_abs_count(abs_student_ids, lec_id)
    student_info=get_student_info_by_ids(lec_id=lec_id,lst_ids=data[1])
    print(student_info[1])
    # Prepare CSV data
    csv_data = StringIO()
    csv_writer = csv.writer(csv_data)
    csv_writer.writerow(['Student ID', 'Student Username', 'Number of Absences'])

    for student_id, info in student_info[1].items():
        csv_writer.writerow([student_id, info['username'], info['total_absences']])

    csv_data.seek(0)  # Move to the beginning of the StringIO buffer
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
    temp_file.write(csv_data.getvalue().encode('utf-8'))
    temp_file.close()
    temp_file_path = temp_file.name

    # Send CSV file as a response
    return send_file(temp_file_path,
                     mimetype='text/csv',
                     as_attachment=True,
                     download_name='attendance_report.csv')


@app.route('/add_student_to_lec', methods=['POST'])
def add_to_lec():
    lec_dic={'algorithm':123,"Data structure":321}
    lecture_name = request.form.get('lecture_Name')
    student_id = request.form.get('student_id')
    lec_id=lec_dic[lecture_name]
    status,msg=add_student_to_lec(student_id=student_id,lec_id=lec_id)
    print(status)
    print(msg)
    return jsonify({'message': msg, "status": status})
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    status,data= login_verif(username,password)
    print(status)
    return jsonify({'data': data, "status": status})
@app.route('/teacher_login', methods=['POST'])
def teacher_login():
    username = request.form['username']
    password = request.form['password']
    status,data= teacher_login_verif(username,password)
    return jsonify({'data': data, "status": status})
@app.route('/submit_data', methods=['POST'])
def submit_data():
    # Retrieve image file
    profile_image1 = request.files['profileImage1']
    profile_image2 = request.files['profileImage2']
    profile_image3 = request.files['profileImage3']
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    major = request.form['major']
    # Read file content as bytes
    image_data1 = profile_image1.read()
    image_data2 = profile_image2.read()
    image_data3 = profile_image3.read()
    # Open the image using Pillow
    img1 = convert_to_rgb(Image.open(BytesIO(image_data1)))
    img2 = convert_to_rgb(Image.open(BytesIO(image_data2)))
    img3 = convert_to_rgb(Image.open(BytesIO(image_data3)))
    Status,Encodings=Images_verification([img1,img2,img3])
    if not Status:
        return jsonify({'message': "these images don't belong to the same person", "Status": False})
    db_req_status,msg=add_student_to_db(email=email,username=username,password=password,encodings=Encodings,major=major)
    print("DB stat",db_req_status)
    if not db_req_status:
        return jsonify(
            {'message': msg, "Status": db_req_status})
    return jsonify({'message': 'User has been added successfully,you will be directed to the login page.',"Status":db_req_status})





if __name__ == '__main__':
    app.run(debug=False,host="0.0.0.0")