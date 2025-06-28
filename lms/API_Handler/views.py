from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import redirect
from DB.models import Student, Faculty, Department, Campus, Program
# lms/API_Handler/views.py

# Create your views here.
def view_student(request, regd_no):
    student = Student.objects.get(regd_no=regd_no)
    if not student:
        return redirect('students')
    return JsonResponse({
        'status': 'success',
        'pic_key': student.dp_key,
        'data':{
            'regd_no': student.regd_no,
            'name': student.name,
            'birthday': student.birthday,
            'email': student.email,
            'gender': student.gender,
            'batch': student.batch,
            'blood_group': student.blood_group,
            'city': student.city,
            'mobile': student.mobile,
            'country': student.country,
            'district': student.district_name,
            'state': student.state_name,
            'prev_degree1_gpa': student.prev_degree1_gpa,
            'prev_degree2_gpa': student.prev_degree2_gpa,
            'prev_degree1_name': student.prev_degree1_name,
            'prev_degree1_university': student.prev_degree1_university,
            'prev_degree2_name': student.prev_degree2_name,
            'prev_degree2_university': student.prev_degree2_university,
            'program': str(student.program) if student.program else None,
            'status': student.status
    }})

def view_faculty(request, faculty_id):
    faculty = Faculty.objects.get(faculty_id=faculty_id)
    if not faculty:
        return redirect('faculty')
    return JsonResponse({
        'status': 'success',
        'pic_key': faculty.dp_key,
        'data': {
            'id': faculty.faculty_id,
            'birthday': faculty.dob,
            'name': faculty.name,
            'gender': faculty.gender,
            'email': faculty.email,
            'campus': str(faculty.campus) if faculty.campus else None,
            'qualification': faculty.qualification,
            'mobile': faculty.mobile,
            'department': str(faculty.department) if faculty.department else None,
            'status': faculty.status
        }
    })

def view_department(request, dept_id):
    department = Department.objects.get(dept_id=dept_id)
    if not department:
        return redirect('departments')
    return JsonResponse({
        'status': 'success',
        'data': {
            'dept_id': department.dept_id,
            'name': department.dept_name,
            'hod': str(department.hod.name) if department.hod else None,
    }})

def view_campus(request, campus_id):
    campus = Campus.objects.get(campus_id=campus_id)
    if not campus:
        return redirect('campus')
    return JsonResponse({
        'status': 'success',
        'data': {
            'code': campus.code,
            'name': campus.name,
            'location': campus.location
    }})

def view_program(request, program_id):
    program = Program.objects.get(id=program_id)
    if not program:
        return redirect('programs')
    return JsonResponse({
        'status': 'success',
        'data': {
            'code': program.programme_code,
            'name': program.name,
            'department': str(program.department) if program.department else None,
            'duration': program.duration_years
    }})