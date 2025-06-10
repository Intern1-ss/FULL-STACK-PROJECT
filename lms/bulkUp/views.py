from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from DB.models import Department, Campus, Faculty, Program, Student
from .utils import generate_excel_template, read_excel_and_return_dataframe
import json
from xhtml2pdf import pisa
from datetime import date

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
        expected_columns = ['dept_id', 'dept_name']
        df = read_excel_and_return_dataframe(request.FILES['file'])
        if df is None:
            messages.error(request, "Failed to read the Excel file.")
            return redirect('bulkUp_home')
        if list(df.columns) != expected_columns:
            messages.error(request, "Uploaded file does not match the Department template columns.")
            return render(request, 'Error-Handler.html', {'errors': ["Template mismatch: expected columns are " + str(expected_columns)], 'count': 0, 'ecount': 1, 'role': 'department'})
        count = 0
        errors = []
        for idx, row in df.iterrows():
            try:
                if Department.objects.filter(dept_id=row['dept_id']).exists():
                    raise ValueError(f"Department with dept_id '{row['dept_id']}' already exists.")
                # No foreign key to check for Department
                Department.objects.update_or_create(
                    dept_id=row['dept_id'],
                    defaults={'dept_name': row['dept_name']}
                )
                count += 1
            except Exception as e:
                errors.append(f"Row {idx+2}: {str(e)}")
        if errors:
            messages.error(request, "Some rows could not be uploaded:\n" + "\n".join(errors))
            return render(request, 'Error-Handler.html', {'errors': errors, 'count': count, 'ecount': len(errors), 'role': 'department'})
        messages.success(request, "Department data uploaded successfully.")
        return render(request, 'Error-Handler.html', {'errors': errors, 'count': count, 'ecount': len(errors), 'role': 'department'})

# =======================
# CAMPUS TEMPLATE & UPLOAD
# =======================
def download_campus_template(request):
    columns = ['id', 'campus_name', 'location']
    return generate_excel_template(columns)

def upload_campus_excel(request):
    if request.method == 'POST':
        expected_columns = ['id', 'campus_name', 'location']
        df = read_excel_and_return_dataframe(request.FILES['file'])
        if df is None:
            messages.error(request, "Failed to read the Excel file.")
            return redirect('bulkUp_home')
        if list(df.columns) != expected_columns:
            messages.error(request, "Uploaded file does not match the Campus template columns.")
            return render(request, 'Error-Handler.html', {'errors': ["Template mismatch: expected columns are " + str(expected_columns)], 'count': 0, 'ecount': 1, 'role': 'campus'})
        count = 0
        errors = []
        for idx, row in df.iterrows():
            try:
                if Campus.objects.filter(id=row['id']).exists():
                    raise ValueError(f"Campus with id '{row['id']}' already exists.")
                # No foreign key to check for Campus
                Campus.objects.update_or_create(
                    id=row['id'],
                    defaults={
                        'campus_name': row['campus_name'],
                        'location': row['location']
                    }
                )
                count += 1
            except Exception as e:
                errors.append(f"Row {idx+2}: {str(e)}")
        if errors:
            messages.error(request, "Some rows could not be uploaded:\n" + "\n".join(errors))
            return render(request, 'Error-Handler.html', {'errors': errors, 'count': count, 'ecount': len(errors), 'role': 'campus'})
        messages.success(request, "Campus data uploaded successfully.")
        return render(request, 'Error-Handler.html', {'errors': errors, 'count': count, 'ecount': len(errors), 'role': 'campus'})

# =======================
# FACULTY TEMPLATE & UPLOAD
# =======================
def download_faculty_template(request):
    columns = ['faculty_id', 'dob', 'name', 'email', 'gender', 'mobile', 'campus_id', 'qualification', 'department_id', 'status']
    return generate_excel_template(columns)

@csrf_exempt
def upload_faculty_excel(request):
    if request.method == 'POST':
        expected_columns = ['faculty_id', 'dob', 'name', 'email', 'gender', 'mobile', 'campus_id', 'qualification', 'department_id', 'status']
        df = read_excel_and_return_dataframe(request.FILES['file'])
        if df is None:
            messages.error(request, "Failed to read the Excel file.")
            return redirect('bulkUp_home')
        if list(df.columns) != expected_columns:
            messages.error(request, "Uploaded file does not match the Faculty template columns.")
            return render(request, 'Error-Handler.html', {'errors': ["Template mismatch: expected columns are " + str(expected_columns)], 'count': 0, 'ecount': 1, 'role': 'faculty'})
        count = 0
        errors = []
        for idx, row in df.iterrows():
            try:
                if Faculty.objects.filter(faculty_id=row['faculty_id']).exists():
                    raise ValueError(f"Faculty with faculty_id '{row['faculty_id']}' already exists.")
                # Foreign key checks
                if not Campus.objects.filter(id=row['campus_id']).exists():
                    raise ValueError(f"Campus with id '{row['campus_id']}' not found.")
                if not Department.objects.filter(dept_id=row['department_id']).exists():
                    raise ValueError(f"Department with dept_id '{row['department_id']}' not found.")
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
                count += 1
            except Exception as e:
                errors.append(f"Row {idx+2}: {str(e)}")
        if errors:
            messages.error(request, "Some rows could not be uploaded:\n" + "\n".join(errors))
            return render(request, 'Error-Handler.html', {'errors': errors, 'count': count, 'ecount': len(errors), 'role': 'faculty'})
        messages.success(request, "Faculty data uploaded successfully.")
        return render(request, 'Error-Handler.html', {'errors': errors, 'count': count, 'ecount': len(errors), 'role': 'faculty'})

# =======================
# PROGRAM TEMPLATE & UPLOAD
# =======================
def download_program_template(request):
    columns = ['name', 'code', 'department_id', 'duration_years']
    return generate_excel_template(columns)

@csrf_exempt
def upload_program_excel(request):
    if request.method == 'POST':
        expected_columns = ['name', 'code', 'department_id', 'duration_years']
        df = read_excel_and_return_dataframe(request.FILES['file'])
        if df is None:
            messages.error(request, "Failed to read the Excel file.")
            return redirect('bulkUp_home')
        if list(df.columns) != expected_columns:
            messages.error(request, "Uploaded file does not match the Program template columns.")
            return render(request, 'Error-Handler.html', {'errors': ["Template mismatch: expected columns are " + str(expected_columns)], 'count': 0, 'ecount': 1, 'role': 'program'})
        count = 0
        errors = []
        for idx, row in df.iterrows():
            try:
                if Program.objects.filter(code=row['code']).exists():
                    raise ValueError(f"Program with code '{row['code']}' already exists.")
                # Foreign key check for department_id
                if not Department.objects.filter(dept_id=row['department_id']).exists():
                    raise ValueError(f"Department with dept_id '{row['department_id']}' not found.")
                Program.objects.update_or_create(
                    code=row['code'],
                    defaults={
                        'name': row['name'],
                        'department_id': row['department_id'],
                        'duration_years': row['duration_years']
                    }
                )
                count += 1
            except Exception as e:
                errors.append(f"Row {idx+2}: {str(e)}")
        if errors:
            messages.error(request, "Some rows could not be uploaded:\n" + "\n".join(errors))
            return render(request, 'Error-Handler.html', {'errors': errors, 'count': count, 'ecount': len(errors), 'role': 'program'})
        messages.success(request, "Program data uploaded successfully.")
        return render(request, 'Error-Handler.html', {'errors': errors, 'count': count, 'ecount': len(errors), 'role': 'program'})

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
        expected_columns = [
            'regd_no', 'name', 'email', 'mobile', 'state_name', 'district_name',
            'city', 'country', 'prev_degree1_name', 'prev_degree1_university', 'prev_degree1_gpa',
            'prev_degree2_name', 'prev_degree2_university', 'prev_degree2_gpa',
            'blood_group', 'birthday', 'program_code', 'batch', 'status'
        ]
        df = read_excel_and_return_dataframe(request.FILES['file'])
        if df is None:
            messages.error(request, "Failed to read the Excel file.")
            return redirect('bulkUp_home')
        if list(df.columns) != expected_columns:
            messages.error(request, "Uploaded file does not match the Student template columns.")
            return render(request, 'Error-Handler.html', {'errors': ["Template mismatch: expected columns are " + str(expected_columns)], 'count': 0, 'ecount': 1, 'role': 'student'})
        count = 0
        errors = []
        for idx, row in df.iterrows():
            try:
                # Validate program_code exists
                try:
                    program = Program.objects.get(code=row['program_code'])
                except Program.DoesNotExist:
                    raise ValueError(f"Program code '{row['program_code']}' not found.")
                # Add more foreign key checks here if needed
                if Student.objects.filter(regd_no=row['regd_no']).exists():
                    raise ValueError(f"Student with regd_no '{row['regd_no']}' already exists.")
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
                        'program_id': program.id,
                        'batch': row['batch'],
                        'status': row['status'],
                    }
                )
                count += 1
            except Exception as e:
                errors.append(f"Row {idx+2}: {str(e)}")  # +2 for Excel row number (header + 0-index)
        if errors:
            messages.error(request, "Some rows could not be uploaded:\n" + "\n".join(errors))
            return render(request, 'Error-Handler.html', {'errors': errors, 'count': count, 'ecount': len(errors), 'role': 'student'})
        messages.success(request, "Student data uploaded successfully.")
        return render(request, 'Error-Handler.html', {'errors': errors, 'count': count, 'ecount': len(errors), 'role': 'student'})
        return HttpResponse("Student data uploaded successfully.", status=200)
        return redirect('students')

@csrf_exempt
@require_POST
def generate_error_pdf(request):
    try:
        data = json.loads(request.body)
        errors = data.get('errors', [])
        count = data.get('count', 0)
        ecount = data.get('ecount', len(errors))
        role = data.get('role', 'student')
        html = render_to_string('Error-PDF.html', {
            'date': date.today().strftime('%Y-%m-%d'),
            'errors': errors,
            'count': count,
            'ecount': ecount,
            'role': role,
            'year': date.today().year,
        })
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="error_report.pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return JsonResponse({'error': 'PDF generation failed'}, status=500)
        return response
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

