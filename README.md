# Hospital-Management-System
Develop a RESTful API for a Hospital Management System using a suitable backend framework (Flask or Django) that allows users to manage patients, doctors, and departments efficiently.

# install project
git clone https://github.com/ravisvats/Hospital-Management-System.git
Create a virtual environment: virtualenv virt<br />
activate virtual environment: source virt/bin/activate<br />
install all packages: pip3 install requirements.text<br />
run flask app by: python app.py<br />

# Databases
now we have to create a database inside our mysql:<br />
create user: CREATE USER 'ravi'@'localhost' IDENTIFIED BY 'Ravi123!';<br />
create database hospital;<br />
GRANT ALL PRIVILEGES ON hospital.* TO 'ravi'@'localhost'; # user your user from local system or you can create user <br />
use hospital;<br />
CREATE TABLE department (     id INT AUTO_INCREMENT PRIMARY KEY,     name VARCHAR(100) NOT NULL,     services_offered TEXT );<br />
CREATE TABLE doctor (
    ->     id INT AUTO_INCREMENT PRIMARY KEY,
    ->     name VARCHAR(100) NOT NULL,
    ->     specialization VARCHAR(100) NOT NULL,
    ->     department_id INT NOT NULL,
    ->     contact_information VARCHAR(100) NOT NULL,
    ->     day_of_week INT NOT NULL,
    ->     start_time TIME NOT NULL,
    ->     end_time TIME NOT NULL,
    ->     FOREIGN KEY (department_id) REFERENCES department(id)
    -> );<br />
 CREATE TABLE patient (
    ->     id INT AUTO_INCREMENT PRIMARY KEY,
    ->     name VARCHAR(100) NOT NULL,
    ->     age INT NOT NULL,
    ->     gender VARCHAR(10) NOT NULL,
    ->     contact_information VARCHAR(100) NOT NULL,
    ->     medical_history TEXT NOT NULL,
    ->     allergies TEXT NOT NULL
    -> );<br />
CREATE TABLE appointment (
    ->     id INT AUTO_INCREMENT PRIMARY KEY,
    ->     date DATETIME NOT NULL,
    ->     patient_id INT NOT NULL,
    ->     doctor_id INT NOT NULL,
    ->     FOREIGN KEY (patient_id) REFERENCES patient(id),
    ->     FOREIGN KEY (doctor_id) REFERENCES doctor(id)
    -> );<br />

# Postman api's curl

# First create department of hospital
curl --location --request POST 'http://127.0.0.1:5000/departments' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Ortho",
    "services_offered":"bones"
}'

# Get all departments list filter search by per page, name and services_offered
curl --location --request GET 'http://127.0.0.1:5000/departments?per_page=10&name=ortho&services_offered=women'

# Create doctor on the portal
curl --location --request POST 'http://127.0.0.1:5000/doctors' \
--header 'Content-Type: application/json' \
--data-raw '{
  "name": "Dr. Arti",
  "specialization": "Gyno",
  "department_id": 2,
  "contact_information": "123-456-7890",
  "day_of_week": 2,
  "start_time": "08:00:00",
  "end_time": "17:00:00"
}
# Get all doctors filter and search by name, specialization and availability
'
curl --location --request GET 'http://127.0.0.1:5000/doctors?per_page=2&name=kab&specialization=gyn&department_id=1&day_of_week=2'

# Register patient
curl --location --request POST 'http://127.0.0.1:5000/patients' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "malkhan",
    "age":"54",
    "gender": "male",
    "contact_information": 1234567,
    "medical_history": "sugar",
    "allergies": "honey"
}'

# Get all patients filter by name
curl --location --request GET 'http://127.0.0.1:5000/patients?name=suraj'

# Create appointment of patient with doctor
curl --location --request POST 'http://127.0.0.1:5000/create_appointment' \
--header 'Content-Type: application/json' \
--data-raw '{
    "doctor_id": 2,
    "patient_id": 1,
    "day_of_week": 3, 
    "time": "09:00"
}'

# Get all appointments list
curl --location --request GET 'http://127.0.0.1:5000/appointments'

# Assign and Re-assign Patients to Doctors
curl --location --request PUT 'http://127.0.0.1:5000/update_appointment/1' \
--header 'Content-Type: application/json' \
--data-raw '{
    "patient_id": 2,
    "doctor_id":1
}'

# Appointment Records of patients
curl --location --request GET 'http://127.0.0.1:5000/patient_history/1'

# List of Patients Assigned to doctors
curl --location --request GET 'http://127.0.0.1:5000/doctor_patients/1'
