from django.shortcuts import render, redirect
from DB.models import Department, Campus, Faculty

# Create your views here.
def home(request):
    return render(request, 'Overview.html')

def students(request):
    return render(request, 'Student.html')

def faculty(request):
    faculties = Faculty.objects.all()

    return render(request, 'Faculty.html', {'faculties': faculties})

def departments(request):
    departments = Department.objects.all()
    return render(request, 'Departments.html', {'departments': departments})

def campus(request):
    campuses = Campus.objects.all()
    return render(request, 'Campus.html', {'campuses': campuses})

def addstudent(request):
    return render(request, 'Add-Student.html')

def addfaculty(request):
    if request.method == 'POST':
        faculty = Faculty()
        faculty.faculty_id = request.POST.get('faculty_id')
        faculty.name = request.POST.get('name')
        faculty.dob = request.POST.get('dob')
        faculty.email = request.POST.get('email')
        faculty.mobile = request.POST.get('mobile')
        faculty.gender  = request.POST.get('gender')
        faculty.campus = Campus.objects.get(campus_name=request.POST.get('campus'))
        faculty.qualification = request.POST.get('qualification')
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

def edit_faculty(request, faculty_id):
    faculty = Faculty.objects.get(faculty_id=faculty_id)
    if request.method == 'POST':
        faculty.name = request.POST.get('name')
        faculty.dob = request.POST.get('dob')
        faculty.email = request.POST.get('email')
        faculty.mobile = request.POST.get('mobile')
        faculty.gender  = request.POST.get('gender')
        faculty.campus = Campus.objects.get(campus_name=request.POST.get('campus'))
        faculty.qualification = request.POST.get('qualification')
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