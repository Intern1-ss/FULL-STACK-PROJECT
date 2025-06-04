from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from DB.models import Department, Campus, Faculty, Program, Student
from .utils import generate_excel_template, read_excel_and_return_dataframe

# Create your views here.
def home(request):
    if request.method == "POST":
        return JsonResponse({"api": "bulkUp", "status": "ok"})
    return HttpResponse("This is bulkUp app home page. Use POST method to access the API.", status=200)

# =======================
# DEPARTMENT TEMPLATE & UPLOAD
# =======================
def download_department_template(request):
    columns = ['dept_id', 'dept_name']
    return generate_excel_template(columns)

@csrf_exempt
def upload_department_excel(request):
    if request.method == 'POST':
        df = read_excel_and_return_dataframe(request.FILES['file'])
        if df is None:
            messages.error(request, "Failed to read the Excel file.")
            return redirect('bulkUp_home')
        for _, row in df.iterrows():
            Department.objects.update_or_create(
                dept_id=row['dept_id'],
                defaults={'dept_name': row['dept_name']}
            )
        messages.success(request, "Department data uploaded successfully.")
        return redirect('departments')

# =======================
# CAMPUS TEMPLATE & UPLOAD
# =======================
def download_campus_template(request):
    columns = ['id', 'campus_name', 'location']
    return generate_excel_template(columns)

def upload_campus_excel(request):
    if request.method == 'POST':
        df = read_excel_and_return_dataframe(request.FILES['file'])
        print(df)
        if df is None:
            messages.error(request, "Failed to read the Excel file.")
            return redirect('bulkUp_home')
        for _, row in df.iterrows():
            Campus.objects.update_or_create(
                id=row['id'],
                defaults={
                    'campus_name': row['campus_name'],
                    'location': row['location']
                }
            )
        messages.success(request, "Campus data uploaded successfully.")
        return redirect('campus')

# =======================
# FACULTY TEMPLATE & UPLOAD
# =======================
def download_faculty_template(request):
    columns = ['faculty_id', 'dob', 'name', 'email', 'gender', 'mobile', 'campus_id', 'qualification', 'department_id', 'status']
    return generate_excel_template(columns)

@csrf_exempt
def upload_faculty_excel(request):
    if request.method == 'POST':
        df = read_excel_and_return_dataframe(request.FILES['file'])
        if df is None:
            messages.error(request, "Failed to read the Excel file.")
            return redirect('bulkUp_home')
        for _, row in df.iterrows():
            Faculty.objects.update_or_create(
                faculty_id=row['faculty_id'],
                defaults={
                    'dob': row['dob'],
                    'name': row['name'],
                    'email': row['email'],
                    'gender': row['gender'],
                    'mobile': row['mobile'],
                    'campus_id': row['campus_id'],
                    'qualification': row['qualification'],
                    'department_id': row['department_id'],
                    'status': row['status'],
                }
            )
        messages.success(request, "Faculty data uploaded successfully.")
        return redirect('faculty')

# =======================
# PROGRAM TEMPLATE & UPLOAD
# =======================
def download_program_template(request):
    columns = ['name', 'code', 'department_id', 'duration_years']
    return generate_excel_template(columns)

@csrf_exempt
def upload_program_excel(request):
    if request.method == 'POST':
        df = read_excel_and_return_dataframe(request.FILES['file'])
        if df is None:
            messages.error(request, "Failed to read the Excel file.")
            return redirect('bulkUp_home')
        for _, row in df.iterrows():
            Program.objects.update_or_create(
                code=row['code'],
                defaults={
                    'name': row['name'],
                    'department_id': row['department_id'],
                    'duration_years': row['duration_years']
                }
            )
        messages.success(request, "Program data uploaded successfully.")
        return redirect('programs')

# =======================
# STUDENT TEMPLATE & UPLOAD
# =======================
def download_student_template(request):
    columns = [
        'regd_no', 'name', 'email', 'mobile', 'state_name', 'district_name',
        'city', 'country', 'prev_degree1_name', 'prev_degree1_university', 'prev_degree1_gpa',
        'prev_degree2_name', 'prev_degree2_university', 'prev_degree2_gpa',
        'blood_group', 'birthday', 'program_code', 'batch', 'status'
    ]
    return generate_excel_template(columns)

@csrf_exempt
def upload_student_excel(request):
    if request.method == 'POST':
        df = read_excel_and_return_dataframe(request.FILES['file'])
        if df is None:
            messages.error(request, "Failed to read the Excel file.")
            return redirect('bulkUp_home')
        for _, row in df.iterrows():
            a = Program.objects.get(code=row['program_code']).id  # Ensure program exists
            Student.objects.update_or_create(
                regd_no=row['regd_no'],
                defaults={
                    'name': row['name'],
                    'email': row['email'],
                    'mobile': row['mobile'],
                    'state_name': row['state_name'],
                    'district_name': row['district_name'],
                    'city': row['city'],
                    'country': row['country'],
                    'prev_degree1_name': row['prev_degree1_name'],
                    'prev_degree1_university': row['prev_degree1_university'],
                    'prev_degree1_gpa': row['prev_degree1_gpa'],
                    'prev_degree2_name': row['prev_degree2_name'],
                    'prev_degree2_university': row['prev_degree2_university'],
                    'prev_degree2_gpa': row['prev_degree2_gpa'],
                    'blood_group': row['blood_group'],
                    'birthday': row['birthday'],
                    'program_id': a,
                    'batch': row['batch'],
                    'status': row['status'],
                }
            )
        messages.success(request, "Student data uploaded successfully.")
        return redirect('students')
