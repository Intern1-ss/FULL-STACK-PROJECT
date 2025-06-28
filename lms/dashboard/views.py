from django.shortcuts import render, redirect , get_object_or_404
from django.http import JsonResponse
from DB.models import Department, Campus, Faculty, Student, Program , Course   
from mediahandler import utils as mh
from django.contrib import messages
from collections import defaultdict

import requests

# Create your views here.
def home(request):
    context = {
        'student_count': Student.objects.count(),
        'faculty_count': Faculty.objects.count(),
        'department_count': Department.objects.count(),
        'campus_count': Campus.objects.count(),
        'program_count': Program.objects.count(),
        'courses_count':Course.objects.count(),
    }
    return render(request, 'Overview.html', context)

def students(request):
    return render(request, 'Student.html', {'students': Student.objects.all()})

def faculty(request):
    faculties = Faculty.objects.all()

    return render(request, 'Faculty.html', {'faculties': faculties})

def programs(request):
    return render(request, 'Programs.html', {'programs': Program.objects.all()})
    
#this is the old one for course
# def courses_page(request):
#     programs = Program.objects.all()
#     return render(request, 'Courses.html', {'programs': programs})


def courses_page(request):
    programs = Program.objects.all()
    if request.method == 'POST':
        programme_code = request.POST.get('programme_code')
        batch = request.POST.get('batch')
        return redirect('add_course', programme_code=programme_code, batch=batch)
    return render(request, 'Courses.html', {'programs': programs})

# def view_courses(request, programme_code, batch):
#     program = Program.objects.filter(programme_code=programme_code, batch=batch).first()
#     if not program:
#         return HttpResponse("Program not found", status=404)

#     # courses = Course.objects.filter(programme_code=programme_code, batch=batch)
#     courses = Course.objects.filter(programme_code=programme_code, batch=batch).order_by('semester', 'sequence')
#     return render(request, 'view_courses.html', {
#         'program': program,
#         'courses': courses
#     })


def view_courses(request, programme_code, batch):
    program = Program.objects.filter(programme_code=programme_code, batch=batch).first()
    if not program:
        return HttpResponse("Program not found", status=404)

    courses = Course.objects.filter(programme_code=programme_code, batch=batch).order_by('semester', 'sequence')

    # Group courses by semester
    semester_wise_courses = defaultdict(list)
    for course in courses:
        semester_wise_courses[course.semester].append(course)

    return render(request, 'view_courses.html', {
        'program': program,
        'semester_wise_courses': dict(semester_wise_courses)
    })



# def edit_courses(request, program_id):
#     program = get_object_or_404(Program, id=program_id)

#     if request.method == 'POST':
#         # Clear existing papers for the program
#         program.papers.all().delete()

#         # Get data from form
#         # paper_code = request.POST.getlist('paper_code')
#         # paper_title = request.POST.getlist('paper_title')
#         # credits = request.POST.getlist('credit')
#         # cie_maxs = request.POST.getlist('cie_max')
#         # ese_maxs = request.POST.getlist('ese_max')
#         # cie_weights = request.POST.getlist('cie_weight')
#         # ese_weights = request.POST.getlist('ese_weight')
#         paper_codes = request.POST.getlist('paper_code')
#         paper_titles = request.POST.getlist('paper_title')
#         credits = request.POST.getlist('credit')
#         cie_maxs = request.POST.getlist('cie_max')
#         ese_maxs = request.POST.getlist('ese_max')
#         cie_weights = request.POST.getlist('cie_weight')
#         ese_weights = request.POST.getlist('ese_weight')


#         for i in range(len(paper_codes)):
#             if paper_codes[i] and paper_titles[i]:
#                 Paper.objects.create(
#                     paper_code=paper_codes[i],
#                     paper_title=paper_titles[i],
#                     credit=int(credits[i]),
#                     cie_max=int(cie_maxs[i]),
#                     ese_max=int(ese_maxs[i]),
#                     cie_weight=int(cie_weights[i]),
#                     ese_weight=int(ese_weights[i]),
#                     primary_department=program.department,
#                     program=program
#                 )

#         return redirect('courses')  # or your program list page

#     return render(request, 'Edit-Courses.html', {'program': program})


# def edit_courses(request, program_id):
#     program = get_object_or_404(Program, id=program_id)

#     if request.method == 'POST':
#         # Clear existing papers for the program
#         program.papers.all().delete()

#         # Get form data
#         paper_codes = request.POST.getlist('paper_code')
#         paper_titles = request.POST.getlist('paper_title')
#         credits = request.POST.getlist('credit')
#         cie_maxs = request.POST.getlist('cie_max')
#         ese_maxs = request.POST.getlist('ese_max')
#         cie_weights = request.POST.getlist('cie_weight')
#         ese_weights = request.POST.getlist('ese_weight')

#         for i, code in enumerate(paper_codes):
#             title = paper_titles[i]
#             credit = credits[i]
#             cie_max = cie_maxs[i]
#             ese_max = ese_maxs[i]
#             cie_weight = cie_weights[i]
#             ese_weight = ese_weights[i]

#             # Validate required fields
#             if code.strip() and title.strip():
#                 try:
#                     Paper.objects.create(
#                         paper_code=code.strip(),
#                         paper_title=title.strip(),
#                         credit=int(credit),
#                         cie_max=int(cie_max),
#                         ese_max=int(ese_max),
#                         cie_weight=int(cie_weight),
#                         ese_weight=int(ese_weight),
#                         primary_department=program.department,
#                         program=program
#                     )
#                 except Exception as e:
#                     print(f"Error saving paper at index {i}: {e}")
#                     continue  # Optionally log or skip invalid rows

#         return redirect('courses')

#     return render(request, 'Edit-Courses.html', {'program': program})



def edit_courses(request, program_id):
    program = get_object_or_404(Program, id=program_id)

    if request.method == 'POST':
        # Get data from form
        paper_codes = request.POST.getlist('paper_code')
        paper_titles = request.POST.getlist('paper_title')
        credits = request.POST.getlist('credit')
        cie_maxs = request.POST.getlist('cie_max')
        ese_maxs = request.POST.getlist('ese_max')
        cie_weights = request.POST.getlist('cie_weight')
        ese_weights = request.POST.getlist('ese_weight')

        for i, paper_code in enumerate(paper_codes):
            # Only save non-empty entries
            if paper_code and paper_titles[i]:
                Paper.objects.create(
                    paper_code=paper_code,
                    paper_title=paper_titles[i],
                    credit=int(credits[i]) if credits[i] else 0,
                    cie_max=int(cie_maxs[i]) if cie_maxs[i] else 0,
                    ese_max=int(ese_maxs[i]) if ese_maxs[i] else 0,
                    cie_weight=int(cie_weights[i]) if cie_weights[i] else 0,
                    ese_weight=int(ese_weights[i]) if ese_weights[i] else 0,
                    primary_department=program.department,
                    program=program
                )

        return redirect('courses')  # Redirect to the course list page

    return render(request, 'Edit-Courses.html', {'program': program})

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

def uploadcourse(request):
    return render(request, 'Upload-Courses.html')

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
            student.program = Program.objects.get(programme_code=request.POST.get('program'))
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
        
        # Required fields
        program. programme_code = request.POST.get('code')  # programme_code
        program.batch = request.POST.get('batch')
        program.programme_short_name = request.POST.get('short_name')  # programme_short_name
        program. programme_full_name = request.POST.get('full_name')    # programme_full_name
        # total_semesters 
        total_sem = request.POST.get('total_semesters')
        if total_sem and total_sem.isdigit():
            program.total_semesters = int(total_sem)

        # Optional or validated fields
        dept_id = request.POST.get('department')
        if dept_id:
            program.department = Department.objects.get(dept_id=dept_id)
        else:
            program.department = None

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

# def edit_program(request, program_id):
#     program = Program.objects.get(id=program_id)
#     if request.method == 'POST':
#         program.name = request.POST.get('name')
#         program.code = request.POST.get('code')
#         program.duration_years = request.POST.get('duration_years')
#         # Ensure that the department exists before assigning
#         if not request.POST.get('department'):
#             program.department = None
#         else:
#             program.department = Department.objects.get(dept_id=request.POST.get('department'))
#         program.save()
#         return redirect('programs')
    
#     departments = Department.objects.all()
#     return render(request, 'Edit-Programs.html', {'program': program, 'departments': departments})

def edit_program(request, program_id):
    program = Program.objects.get(id=program_id)

    if request.method == 'POST':
        program.programme_code = request.POST.get('code')
        program.programme_short_name = request.POST.get('short_name')
        program.programme_full_name = request.POST.get('full_name')
        program.batch = request.POST.get('batch')
        total_sem = request.POST.get('total_semesters')
        if total_sem and total_sem.isdigit():
            program.total_semesters = int(total_sem)
        dept_id = request.POST.get('department')
        if dept_id:
            try:
                program.department = Department.objects.get(dept_id=dept_id)
            except Department.DoesNotExist:
                program.department = None
        else:
            program.department = None

        program.save()
        return redirect('programs')

    departments = Department.objects.all()
    return render(request, 'Edit-Programs.html', {
        'program': program,
        'departments': departments
    })


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



#for adding the details in course according to batch
from DB.models import Course
# def add_course(request, programme_code, batch):
#     if request.method == 'POST':
#         paper_code = request.POST.get('paper_code')

#         if Course.objects.filter(programme_code=programme_code, batch=batch, paper_code=paper_code).exists():
#             # messages.error(request, "This course already exists for the selected program and batch.")
#             return redirect(request.path)

#         Course.objects.create(
#             programme_code=programme_code,
#             batch=batch,
#             # semester=request.POST.get('semester'),
#             paper_code=paper_code,
#             sequence=request.POST.get('sequence'),
#             paper_title=request.POST.get('paper_title'),
#             category=request.POST.get('category'),
#             credits=request.POST.get('credits'),
#             cie_max=request.POST.get('cie_max'),
#             cie_max_atp=request.POST.get('cie_max_atp') or None,
#             cie_max_psn=request.POST.get('cie_max_psn') or None,
#             cie_max_brn=request.POST.get('cie_max_brn') or None,
#             cie_max_ndg=request.POST.get('cie_max_ndg') or None,
#             ese_max=request.POST.get('ese_max'),
#             ese_max_atp=request.POST.get('ese_max_atp') or None,
#             ese_max_psn=request.POST.get('ese_max_psn') or None,
#             ese_max_brn=request.POST.get('ese_max_brn') or None,
#             ese_max_ndg=request.POST.get('ese_max_ndg') or None,
#             cie_wtg=request.POST.get('cie_wtg'),
#             ese_wtg=request.POST.get('ese_wtg')
#         )
#         messages.success(request, f"Course {paper_code} added successfully.")
#         return redirect('select_program')

#     return render(request, 'Add_Course.html', {
#         'programme_code': programme_code,
#         'batch': batch
#     })



# def add_course(request, programme_code, batch):
#     if request.method == 'POST':
#         paper_codes = request.POST.getlist('paper_code')
#         paper_titles = request.POST.getlist('paper_title')
#         sequences = request.POST.getlist('sequence')
#         categories = request.POST.getlist('category')
#         credits = request.POST.getlist('credits')
#         cie_max = request.POST.getlist('cie_max')
#         cie_max_atp = request.POST.getlist('cie_max_atp')
#         cie_max_psn = request.POST.getlist('cie_max_psn')
#         cie_max_brn = request.POST.getlist('cie_max_brn')
#         cie_max_ndg = request.POST.getlist('cie_max_ndg')
#         ese_max = request.POST.getlist('ese_max')
#         ese_max_atp = request.POST.getlist('ese_max_atp')
#         ese_max_psn = request.POST.getlist('ese_max_psn')
#         ese_max_brn = request.POST.getlist('ese_max_brn')
#         ese_max_ndg = request.POST.getlist('ese_max_ndg')
#         cie_wtg = request.POST.getlist('cie_wtg')
#         ese_wtg = request.POST.getlist('ese_wtg')

#         added_count = 0

#         for i in range(len(paper_codes)):
#             if not paper_codes[i]:
#                 continue  # Skip empty rows

#             if Course.objects.filter(programme_code=programme_code, batch=batch, paper_code=paper_codes[i]).exists():
#                 continue  # Skip duplicates

#             Course.objects.create(
#                 programme_code=programme_code,
#                 batch=batch,
#                 paper_code=paper_codes[i],
#                 paper_title=paper_titles[i],
#                 sequence=sequences[i] or 0,
#                 category=categories[i],
#                 credits=credits[i] or 0,
#                 cie_max=cie_max[i] or 0,
#                 cie_max_atp=cie_max_atp[i] or None,
#                 cie_max_psn=cie_max_psn[i] or None,
#                 cie_max_brn=cie_max_brn[i] or None,
#                 cie_max_ndg=cie_max_ndg[i] or None,
#                 ese_max=ese_max[i] or 0,
#                 ese_max_atp=ese_max_atp[i] or None,
#                 ese_max_psn=ese_max_psn[i] or None,
#                 ese_max_brn=ese_max_brn[i] or None,
#                 ese_max_ndg=ese_max_ndg[i] or None,
#                 cie_wtg=cie_wtg[i] or 0,
#                 ese_wtg=ese_wtg[i] or 0,
#             )
#             added_count += 1

#         if added_count > 0:
#              messages.success(request, "")
#         else:
#             messages.warning(request, "No new courses were added. They may already exist or be empty.")

#         return redirect('courses')

#     return render(request, 'Add_Course.html', {
#         'programme_code': programme_code,
#         'batch': batch
#     })


from django.http import HttpResponse
def add_course(request, programme_code, batch):
    program = get_object_or_404(Program, programme_code=programme_code, batch=batch)
    semesters = list(range(1, 9))
    category_choices = [choice[0] for choice in Course.CATEGORY_CHOICES]

    if request.method == 'POST':
        # Handle delete action
        if 'delete_row' in request.POST:
            course_id = request.POST['delete_row']
            try:
                Course.objects.get(id=course_id).delete()
                messages.success(request, "Course deleted successfully.")
            except Course.DoesNotExist:
                messages.error(request, "Course not found to delete.")
        else:
            # Get all POST field lists
            semester_list = request.POST.getlist('semester')
            paper_code_list = request.POST.getlist('paper_code')
            existing_paper_code_list = request.POST.getlist('existing_paper_code')
            paper_title_list = request.POST.getlist('paper_title')
            sequence_list = request.POST.getlist('sequence')
            category_list = request.POST.getlist('category')
            credits_list = request.POST.getlist('credits')
            cie_max_list = request.POST.getlist('cie_max')
            cie_max_atp_list = request.POST.getlist('cie_max_atp')
            cie_max_psn_list = request.POST.getlist('cie_max_psn')
            cie_max_brn_list = request.POST.getlist('cie_max_brn')
            cie_max_ndg_list = request.POST.getlist('cie_max_ndg')
            ese_max_list = request.POST.getlist('ese_max')
            ese_max_atp_list = request.POST.getlist('ese_max_atp')
            ese_max_psn_list = request.POST.getlist('ese_max_psn')
            ese_max_brn_list = request.POST.getlist('ese_max_brn')
            ese_max_ndg_list = request.POST.getlist('ese_max_ndg')
            cie_wtg_list = request.POST.getlist('cie_wtg')
            ese_wtg_list = request.POST.getlist('ese_wtg')

            for i in range(len(paper_code_list)):
                paper_code = paper_code_list[i].strip()
                existing_code = existing_paper_code_list[i].strip() if i < len(existing_paper_code_list) else ""

                # Skip incomplete new rows
                if not paper_code or not paper_title_list[i].strip():
                    continue

                course_data = {
                    'programme_code': programme_code,
                    'batch': batch,
                    'paper_code': paper_code,
                    'paper_title': paper_title_list[i].strip(),
                    'semester': semester_list[i],
                    'sequence': sequence_list[i] or 0,
                    'category': category_list[i],
                    'credits': credits_list[i] or 0,
                    'cie_max': cie_max_list[i] or 0,
                    'cie_max_atp': cie_max_atp_list[i] or 0,
                    'cie_max_psn': cie_max_psn_list[i] or 0,
                    'cie_max_brn': cie_max_brn_list[i] or 0,
                    'cie_max_ndg': cie_max_ndg_list[i] or 0,
                    'ese_max': ese_max_list[i] or 0,
                    'ese_max_atp': ese_max_atp_list[i] or 0,
                    'ese_max_psn': ese_max_psn_list[i] or 0,
                    'ese_max_brn': ese_max_brn_list[i] or 0,
                    'ese_max_ndg': ese_max_ndg_list[i] or 0,
                    'cie_wtg': cie_wtg_list[i] or 0,
                    'ese_wtg': ese_wtg_list[i] or 0,
                }

                if existing_code:
                    # Update only if values changed
                    try:
                        course = Course.objects.get(programme_code=programme_code, batch=batch, paper_code=existing_code)
                        changed = False
                        for field, val in course_data.items():
                            current_val = getattr(course, field)
                            new_val = type(current_val)(val)
                            if current_val != new_val:
                                setattr(course, field, new_val)
                                changed = True
                        if changed:
                            course.save()
                    except Course.DoesNotExist:
                        continue
                else:
                    # New course (if all required fields filled)
                    if all(course_data.values()):
                        Course.objects.create(**course_data)

            messages.success(request, "Courses updated successfully.")

    courses = Course.objects.filter(programme_code=programme_code, batch=batch).order_by('semester', 'sequence')
    return render(request, 'Add_Course.html', {
        'program': program,
        'batch': batch,
        'courses': courses,
        'semesters': semesters,
        'category_choices': category_choices,
    })




#for course pdf download
from django.template.loader import get_template

from xhtml2pdf import pisa


def download_course_pdf(request, programme_code, batch):
    program = Program.objects.filter(programme_code=programme_code, batch=batch).first()
    if not program:
        return HttpResponse("Program not found", status=404)

    # Get all courses ordered by semester
    courses = Course.objects.filter(programme_code=programme_code, batch=batch).order_by('semester', 'sequence')

    # Organize courses semester-wise
    semester_data = {}
    for course in courses:
        semester_data.setdefault(course.semester, []).append(course)

    # Render to PDF
    template_path = 'pdf_course_template.html'
    context = {
        'program': program,
        'semester_data': semester_data,
    }
    response = HttpResponse(content_type='application/pdf')
    filename = f"{program.programme_full_name.replace(' ', '_')}_Batch_{batch}_Syllabus.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse("Error generating PDF", status=500)

    return response
