from flask import Blueprint, request, jsonify
from models import db, Department, Doctor, Patient, Appointment
from datetime import datetime

new_routes = Blueprint('new_routes', __name__)


@new_routes.route('/departments', methods=['POST'])
def create_department():
    data = request.get_json()
    name = data.get('name')
    services_offered = data.get('services_offered')

    if not name:
        return jsonify({'error': 'Name is required'}), 400

    new_department = Department(name=name, services_offered=services_offered)

    try:
        db.session.add(new_department)
        db.session.commit()
        return jsonify({'message': 'Department created successfully', 'department_id': new_department.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.session.close()


# API endpoint to get departments with pagination, filtering, and searching
@new_routes.route('/departments', methods=['GET'])
def get_departments():
    # Pagination parameters
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    # Filtering parameters
    name_filter = request.args.get('name')
    services_offered_filter = request.args.get('services_offered')

    # Base query
    query = Department.query

    # Apply filters
    if name_filter:
        query = query.filter(Department.name.ilike(f'%{name_filter}%'))
    if services_offered_filter:
        query = query.filter(Department.services_offered.ilike(f'%{services_offered_filter}%'))

    # Pagination
    departments = query.paginate(page=page, per_page=per_page, error_out=False)

    # Convert pagination object to dictionary
    departments_data = {
        'departments': [{'id': department.id, 'name': department.name, 'services_offered': department.services_offered}
                        for department in departments.items],
        'total_departments': departments.total,
        'page': departments.page,
        'per_page': departments.per_page,
        'pages': departments.pages
    }

    return jsonify(departments_data)


# API endpoint to insert a doctor
@new_routes.route('/doctors', methods=['POST'])
def insert_doctor():
    data = request.get_json()
    name = data.get('name')
    specialization = data.get('specialization')
    department_id = data.get('department_id')
    contact_information = data.get('contact_information')
    day_of_week = data.get('day_of_week')
    start_time = data.get('start_time')
    end_time = data.get('end_time')

    if not all([name, specialization, department_id, contact_information, day_of_week, start_time, end_time]):
        return jsonify({'error': 'Missing required fields'}), 400

    new_doctor = Doctor(
        name=name,
        specialization=specialization,
        department_id=department_id,
        contact_information=contact_information,
        day_of_week=day_of_week,
        start_time=start_time,
        end_time=end_time
    )

    try:
        db.session.add(new_doctor)
        db.session.commit()
        return jsonify({'message': 'Doctor inserted successfully', 'doctor_id': new_doctor.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.session.close()


# API endpoint to get doctors with pagination and filtering
@new_routes.route('/doctors', methods=['GET'])
def get_doctors():
    # Pagination parameters
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    # Filtering parameters
    name_filter = request.args.get('name')
    specialization_filter = request.args.get('specialization')
    department_id_filter = request.args.get('department_id')
    day_of_week_filter = request.args.get('day_of_week')

    # Base query
    query = Doctor.query

    # Apply filters
    if name_filter:
        query = query.filter(Doctor.name.ilike(f'%{name_filter}%'))
    if specialization_filter:
        query = query.filter(Doctor.specialization.ilike(f'%{specialization_filter}%'))
    if department_id_filter:
        query = query.filter(Doctor.department_id == int(department_id_filter))
    if day_of_week_filter:
        query = query.filter(Doctor.day_of_week == int(day_of_week_filter))

    # Pagination
    doctors = query.paginate(page=page, per_page=per_page, error_out=False)

    # Convert pagination object to dictionary
    doctors_data = {
        'doctors': [{'id': doctor.id, 'name': doctor.name, 'specialization': doctor.specialization,
                     'department_id': doctor.department_id, 'contact_information': doctor.contact_information,
                     'day_of_week': doctor.day_of_week, 'start_time': str(doctor.start_time), 'end_time': str(doctor.end_time)}
                    for doctor in doctors.items],
        'total_doctors': doctors.total,
        'page': doctors.page,
        'per_page': doctors.per_page,
        'pages': doctors.pages
    }

    return jsonify(doctors_data)


# API endpoint to register a patient
@new_routes.route('/patients', methods=['POST'])
def register_patient():
    data = request.json
    name = data.get('name')
    age = data.get('age')
    gender = data.get('gender')
    contact_information = data.get('contact_information')
    medical_history = data.get('medical_history')
    allergies = data.get('allergies')

    # Validate input
    if not all([name, age, gender, contact_information, medical_history, allergies]):
        return jsonify({'error': 'Missing required fields'}), 400

    # Create a new patient instance
    new_patient = Patient(
        name=name,
        age=age,
        gender=gender,
        contact_information=contact_information,
        medical_history=medical_history,
        allergies=allergies
    )

    # Add the patient to the database session and commit changes
    try:
        db.session.add(new_patient)
        db.session.commit()
        return jsonify({'message': 'Patient registered successfully', 'patient_id': new_patient.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# API endpoint to get patients with pagination and filtering by name
@new_routes.route('/patients', methods=['GET'])
def get_patients():
    # Pagination parameters
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    # Filtering parameter
    name_filter = request.args.get('name')

    # Base query
    query = Patient.query

    # Apply name filter
    if name_filter:
        query = query.filter(Patient.name.ilike(f'%{name_filter}%'))

    # Pagination
    patients = query.paginate(page=page, per_page=per_page, error_out=False)

    # Convert pagination object to dictionary
    patients_data = {
        'patients': [{'id': patient.id, 'name': patient.name, 'age': patient.age,
                      'gender': patient.gender, 'contact_information': patient.contact_information,
                      'medical_history': patient.medical_history, 'allergies': patient.allergies}
                     for patient in patients.items],
        'total_patients': patients.total,
        'page': patients.page,
        'per_page': patients.per_page,
        'pages': patients.pages
    }

    return jsonify(patients_data)


# API endpoint to create an appointment
@new_routes.route('/create_appointment', methods=['POST'])
def create_appointment():
    data = request.json
    doctor_id = data.get('doctor_id')
    patient_id = data.get('patient_id')
    day_of_week = data.get('day_of_week')
    time = data.get('time')

    # Check if the doctor is available at the specified day and time
    doctor = Doctor.query.filter_by(id=doctor_id, day_of_week=day_of_week).first()
    if doctor:
        start_time = datetime.strptime(time, '%H:%M').time()
        if doctor.start_time <= start_time <= doctor.end_time:
            # Create the appointment
            new_appointment = Appointment(date=datetime.now(), doctor_id=doctor_id, patient_id=patient_id)
            db.session.add(new_appointment)
            db.session.commit()
            return jsonify({'message': 'Appointment scheduled successfully'}), 201
        else:
            return jsonify({'error': 'Doctor is not available at the specified time'}), 400
    else:
        return jsonify({'error': 'Doctor not found or does not work on the specified day'}), 404


@new_routes.route('/appointments', methods=['GET'])
def get_appointments():
    appointments = Appointment.query.all()

    appointment_list = []
    for appointment in appointments:
        appointment_list.append({
            'id': appointment.id,
            'date': appointment.date,
            'patient_id': appointment.patient_id,
            'doctor_id': appointment.doctor_id
        })

    return jsonify({'appointments': appointment_list})


@new_routes.route('/update_appointment/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        return jsonify({'error': 'Appointment not found'}), 404

    data = request.json
    if 'date' in data:
        appointment.date = data['date']
    if 'patient_id' in data:
        appointment.patient_id = data['patient_id']
    if 'doctor_id' in data:
        appointment.doctor_id = data['doctor_id']

    db.session.commit()

    return jsonify({'message': 'Appointment updated successfully'}), 200


@new_routes.route('/patient_history/<int:patient_id>', methods=['GET'])
def get_patient_history(patient_id):
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404

    appointments = Appointment.query.filter_by(patient_id=patient_id).all()

    history = {
        'patient_name': patient.name,
        'medical_history': patient.medical_history,
        'allergies': patient.allergies,
        'appointments': []
    }

    for appointment in appointments:
        doctor = Doctor.query.get(appointment.doctor_id)
        if doctor:
            department = Department.query.get(doctor.department_id)
            appointment_data = {
                'date': appointment.date,
                'doctor_name': doctor.name,
                'doctor_specialization': doctor.specialization,
                'department_name': department.name if department else None,
                'department_services_offered': department.services_offered if department else None
            }
            history['appointments'].append(appointment_data)

    return jsonify(history)


@new_routes.route('/doctor_patients/<int:doctor_id>', methods=['GET'])
def get_doctor_patients(doctor_id):
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return jsonify({'error': 'Doctor not found'}), 404

    patients = Patient.query.join(Appointment).filter(Appointment.doctor_id == doctor_id).all()

    doctor_patients = []
    for patient in patients:
        doctor_patients.append({
            'id': patient.id,
            'name': patient.name,
            'age': patient.age,
            'gender': patient.gender,
            'contact_information': patient.contact_information,
            'medical_history': patient.medical_history,
            'allergies': patient.allergies
        })

    return jsonify({'doctor_patients': doctor_patients})

