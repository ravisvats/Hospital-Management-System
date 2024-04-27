from flask import Blueprint, request, jsonify
from models import db, Department, Doctor

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
