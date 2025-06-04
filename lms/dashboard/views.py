from django.shortcuts import render, redirect
from django.http import JsonResponse
from DB.models import Department, Campus, Faculty, Student, Program
from mediahandler import utils as mh
import requests

# Create your views here.
def home(request):
    context = {
        'student_count': Student.objects.count(),
        'faculty_count': Faculty.objects.count(),
        'department_count': Department.objects.count(),
        'campus_count': Campus.objects.count(),
        'program_count': Program.objects.count(),
    }
    return render(request, 'Overview.html', context)

def students(request):
    return render(request, 'Student.html', {'students': Student.objects.all()})

def faculty(request):
    faculties = Faculty.objects.all()

    return render(request, 'Faculty.html', {'faculties': faculties})

def programs(request):
    return render(request, 'Programs.html', {'programs': Program.objects.all()})

def uploadfaculty(request):
    return render(request, 'Upload-Faculty.html')

def uploaddepartment(request):
    return render(request, 'Upload-Department.html')

def uploadcampus(request):
    return render(request, 'Upload-Campus.html')

def uploadstudent(request):
    return render(request, 'Upload-Student.html')

def uploadprogram(request):
    return render(request, 'Upload-Program.html')

def departments(request):
    departments = Department.objects.all()
    return render(request, 'Departments.html', {'departments': departments})

def campus(request):
    campuses = Campus.objects.all()
    return render(request, 'Campus.html', {'campuses': campuses})

def addstudent(request):
    if request.method == 'POST':
        student = Student()
        student.regd_no = request.POST.get('regNum')
        print(request)
        # Ensure the form uses enctype="multipart/form-data" and input name="dp_pic"
        if request.FILES.get('dp_pic'):
            # Upload to mediahandler API
            uploaded = mh.handle_image_upload(request.FILES.get('dp_pic'), f"{student.regd_no}-profile-pic")
            student.dp_key = uploaded.key
        else:
            print("No file uploaded or file is empty.")
            student.dp_key = None
        student.name = request.POST.get('name')
        student.birthday = request.POST.get('dob')
        student.email = request.POST.get('email')
        student.batch = request.POST.get('batch')
        student.gender = request.POST.get('gender')
        student.blood_group = request.POST.get('blood_group')
        student.city = request.POST.get('city')
        student.mobile = request.POST.get('mobile')
        student.country = request.POST.get('country')
        student.district_name = request.POST.get('district_name')
        student.state_name  = request.POST.get('state_name')
        if request.POST.get('prev_degree1_gpa'):
            try:
                student.prev_degree1_gpa = float(request.POST.get('prev_degree1_gpa'))  
            except ValueError: 
                student.prev_degree1_gpa = None
        if request.POST.get('prev_degree2_gpa'):
            try:
                student.prev_degree2_gpa = float(request.POST.get('prev_degree2_gpa'))  
            except ValueError: 
                student.prev_degree2_gpa = None
        student.prev_degree1_name = request.POST.get('prev_degree1_name')
        student.prev_degree1_university = request.POST.get('prev_degree1_university')
        student.prev_degree2_name = request.POST.get('prev_degree2_name')
        student.prev_degree2_university = request.POST.get('prev_degree2_university')
        if not request.POST.get('program'):
            student.program = None
        else:
            # Ensure that the program exists before assigning
            student.program = Program.objects.get(code=request.POST.get('program'))
        student.status = request.POST.get('status')
        student.save()
        return redirect('students')

    return render(request, 'Add-Student.html', {'programs': Program.objects.all()})

def addfaculty(request):
    if request.method == 'POST':
        faculty = Faculty()
        faculty.faculty_id = request.POST.get('faculty_id')
        # Ensure the form uses enctype="multipart/form-data" and input name="dp_pic"
        if request.FILES.get('dp_pic'):
            # Upload to mediahandler API
            uploaded = mh.handle_image_upload(request.FILES.get('dp_pic'), f"{faculty.faculty_id}-profile-pic")
            faculty.dp_key = uploaded.key
        else:
            print("No file uploaded or file is empty.")
            faculty.dp_key = None
        faculty.name = request.POST.get('name')
        faculty.dob = request.POST.get('dob')
        faculty.email = request.POST.get('email')
        faculty.mobile = request.POST.get('mobile')
        faculty.gender  = request.POST.get('gender')
        # Ensure that the campus and department exist before assigning
        if not request.POST.get('campus'):
            faculty.campus = None
        else:
            faculty.campus = Campus.objects.get(campus_name=request.POST.get('campus'))
        faculty.qualification = request.POST.get('qualification')
        # Ensure that the department exists before assigning
        if not request.POST.get('department'):
            faculty.department = None
        else:
            # Ensure that the department exists before assigning
            faculty.department = Department.objects.get(dept_id=request.POST.get('department'))
        faculty.status = request.POST.get('status')
        faculty.save()
        return redirect('faculty')
    return render(request, 'Add-Faculty.html', {'departments': Department.objects.all(), 'campuses': Campus.objects.all()})

def adddepartment(request):
    if request.method == 'POST':
        department = Department()
        department.dept_id = request.POST.get('dept_id')
        department.dept_name = request.POST.get('dept_name')
        if not request.POST.get('hod'):
            department.hod = None
        else:
            # Ensure that the HOD is a valid faculty member
            department.hod = Faculty.objects.get(faculty_id=request.POST.get('hod'))
        department.save()
        return redirect('departments')
    return render(request, 'Add-Departments.html', {'faculties': Faculty.objects.all(), 'campuses': Campus.objects.all()})

def addcampus(request):
    if request.method == 'POST':
        campus = Campus()
        campus.id = request.POST.get('id')
        campus.campus_name = request.POST.get('name')
        campus.location = request.POST.get('loc')
        campus.save()
        return redirect('campus')
    return render(request, 'Add-Campus.html')

def addprogram(request):
    if request.method == 'POST':
        program = Program()
        program.name = request.POST.get('name')
        program.code = request.POST.get('code')
        program.duration_years = request.POST.get('duration_years')
        # Ensure that the department exists before assigning
        if not request.POST.get('department'):
            program.department = None
        else:
            program.department = Department.objects.get(dept_id=request.POST.get('department'))
        program.save()
        return redirect('programs')
    return render(request, 'Add-Programs.html', {'departments': Department.objects.all()})

def edit_student(request, regd_no):
    student = Student.objects.get(regd_no=regd_no)
    if request.method == 'POST':
        student.name = request.POST.get('name')
        print(request)
        # Ensure the form uses enctype="multipart/form-data" and input name="dp_pic"
        if request.FILES.get('dp_pic'):
            # Upload to mediahandler API
            if student.dp_key:
                # If the student already has a profile picture, delete the old one
                mh.delete_image( f"{student.regd_no}-profile-pic")
            uploaded = mh.handle_image_upload(request.FILES.get('dp_pic'), f"{student.regd_no}-profile-pic")
            student.dp_key = uploaded.key
        else:
            print("No file uploaded or file is empty.")
        student.birthday = request.POST.get('dob')
        student.email = request.POST.get('email')
        student.gender = request.POST.get('gender')
        student.batch = request.POST.get('batch')
        student.mobile = request.POST.get('mobile')
        student.blood_group = request.POST.get('blood_group')
        student.city = request.POST.get('city')
        student.country = request.POST.get('country')
        student.district_name = request.POST.get('district_name')
        student.state_name  = request.POST.get('state_name')
        if request.POST.get('prev_degree1_gpa'):
            try:
                student.prev_degree1_gpa = float(request.POST.get('prev_degree1_gpa'))  
            except ValueError: 
                student.prev_degree1_gpa = None
        if request.POST.get('prev_degree2_gpa'):
            try:
                student.prev_degree2_gpa = float(request.POST.get('prev_degree2_gpa'))  
            except ValueError: 
                student.prev_degree2_gpa = None
        student.prev_degree1_name = request.POST.get('prev_degree1_name')
        student.prev_degree1_university = request.POST.get('prev_degree1_university')
        student.prev_degree2_name = request.POST.get('prev_degree2_name')
        student.prev_degree2_university = request.POST.get('prev_degree2_university')
        if not request.POST.get('program'):
            student.program = None
        else:
            # Ensure that the program exists before assigning
            student.program = Program.objects.get(code=request.POST.get('program'))
        student.status = request.POST.get('status')
        student.save()
        return redirect('students')

    return render(request, 'Edit-Student.html', {'student': student, 'programs': Program.objects.all()})

def edit_faculty(request, faculty_id):
    faculty = Faculty.objects.get(faculty_id=faculty_id)
    if request.method == 'POST':
        faculty.name = request.POST.get('name')
        # Ensure the form uses enctype="multipart/form-data" and input name="dp_pic"
        if request.FILES.get('dp_pic'):
            # Upload to mediahandler API
            if faculty.dp_key:
                # If the student already has a profile picture, delete the old one
                mh.delete_image( f"{faculty.faculty_id}-profile-pic")
            uploaded = mh.handle_image_upload(request.FILES.get('dp_pic'), f"{faculty.faculty_id}-profile-pic")
            faculty.dp_key = uploaded.key
        else:
            print("No file uploaded or file is empty.")
        faculty.dob = request.POST.get('dob')
        faculty.email = request.POST.get('email')
        faculty.mobile = request.POST.get('mobile')
        faculty.gender  = request.POST.get('gender')
        # Ensure that the campus and department exist before assigning
        if not request.POST.get('campus'):
            faculty.campus = None
        else:
            faculty.campus = Campus.objects.get(campus_name=request.POST.get('campus'))
        faculty.qualification = request.POST.get('qualification')
        # Ensure that the department exists before assigning
        if not request.POST.get('department'):
            faculty.department = None
        else:
            # Ensure that the department exists before assigning
            faculty.department = Department.objects.get(dept_id=request.POST.get('department'))
        faculty.status = request.POST.get('status')
        faculty.save()
        return redirect('faculty')
    
    departments = Department.objects.all()
    return render(request, 'Edit-Faculty.html', {'faculty': faculty, 'departments': departments, 'campuses': Campus.objects.all()})

def edit_department(request, dept_id):
    department = Department.objects.get(dept_id=dept_id)
    if request.method == 'POST':
        department.dept_name = request.POST.get('dept_name')
        if not request.POST.get('hod'):
            department.hod = None
        else:
            # Ensure that the HOD is a valid faculty member
            department.hod = Faculty.objects.get(faculty_id=request.POST.get('hod'))
        department.save()
        return redirect('departments')
    
    faculties = Faculty.objects.all()
    return render(request, 'Edit-Departments.html', {'department': department, 'faculties': faculties})

def edit_campus(request, campus_id):
    campus = Campus.objects.get(id=campus_id)
    if request.method == 'POST':
        campus.campus_name = request.POST.get('name')
        campus.location = request.POST.get('loc')
        campus.save()
        return redirect('campus')
    return render(request, 'Edit-Campus.html', {'campus': campus})

def edit_program(request, program_id):
    program = Program.objects.get(id=program_id)
    if request.method == 'POST':
        program.name = request.POST.get('name')
        program.code = request.POST.get('code')
        program.duration_years = request.POST.get('duration_years')
        # Ensure that the department exists before assigning
        if not request.POST.get('department'):
            program.department = None
        else:
            program.department = Department.objects.get(dept_id=request.POST.get('department'))
        program.save()
        return redirect('programs')
    
    departments = Department.objects.all()
    return render(request, 'Edit-Programs.html', {'program': program, 'departments': departments})

def delete_student(request, regd_no):
    student = Student.objects.get(regd_no=regd_no)
    if not student:
        return redirect('students')
    student.delete()
    return redirect('students')

def delete_faculty(request, faculty_id):
    faculty = Faculty.objects.get(faculty_id=faculty_id)
    if not faculty:
        return redirect('faculty')
    faculty.delete()
    return redirect('faculty')

def delete_department(request, dept_id):
    department = Department.objects.get(dept_id=dept_id)
    if not department:
        return redirect('departments')
    department.delete()
    return redirect('departments')

def delete_campus(request, campus_id):
    campus = Campus.objects.get(id=campus_id)
    if not campus:
        return redirect('campus')
    campus.delete()
    return redirect('campus')

def delete_program(request, program_id):
    program = Program.objects.get(id=program_id)
    if not program:
        return redirect('programs')
    program.delete()
    return redirect('programs')

