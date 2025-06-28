from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from DB.models import Department, Campus, Faculty, Program, Student, Course
from .utils import generate_excel_template_student, read_excel_and_return_dataframe,safe_decimal,generate_excel_template,generate_excel_template_faculty,generate_excel_template_department,generate_excel_template_program, generate_excel_template_course
import json
from xhtml2pdf import pisa
from datetime import date
import pandas as pd

# Create your views here.
def home(request):
    if request.method == "POST":
        return JsonResponse({"api": "bulkUp", "status": "ok"})
    return HttpResponse("This is bulkUp app home page. Use POST method to access the API.", status=200)

# =======================
# DEPARTMENT TEMPLATE & UPLOAD
# =======================
def download_department_template(request):
    columns = ['dept_id', 'dept_name', 'hod_name']  # Now includes HOD name
    return generate_excel_template_department(columns)


@csrf_exempt
def upload_department_excel(request):
    if request.method == 'POST':
        expected_columns = ['dept_id', 'dept_name', 'hod_name']
        df = read_excel_and_return_dataframe(request.FILES['file'])

        if df is None:
            messages.error(request, "Failed to read the Excel file.")
            return redirect('bulkUp_home')

        if list(df.columns) != expected_columns:
            messages.error(request, "Uploaded file does not match the Department template columns.")
            return render(request, 'Error-Handler.html', {
                'errors': ["Template mismatch: expected columns are " + str(expected_columns)],
                'count': 0,
                'ecount': 1,
                'role': 'department'
            })

        count = 0
        errors = []

        for idx, row in df.iterrows():
            try:
                dept_id = str(row['dept_id']).strip()
                dept_name = str(row['dept_name']).strip()
                hod_name = str(row['hod_name']).strip()

                if Department.objects.filter(dept_id=dept_id).exists():
                    raise ValueError(f"Department with dept_id '{dept_id}' already exists.")

                # Get Faculty instance by name (assuming names are unique)
                faculty_hod = None
                if hod_name:
                    try:
                        faculty_hod = Faculty.objects.get(name=hod_name)
                    except Faculty.DoesNotExist:
                        raise ValueError(f"HOD with name '{hod_name}' not found.")
                    except Faculty.MultipleObjectsReturned:
                        raise ValueError(f"Multiple faculty entries found with name '{hod_name}'. Use unique names.")

                Department.objects.update_or_create(
                    dept_id=dept_id,
                    defaults={
                        'dept_name': dept_name,
                        'hod': faculty_hod
                    }
                )
                count += 1

            except Exception as e:
                errors.append(f"Row {idx + 2}: {str(e)}")  # Row +2 due to 0-index + header

        if errors:
            messages.error(request, "Some rows could not be uploaded:\n" + "\n".join(errors))
            return render(request, 'Error-Handler.html', {
                'errors': errors,
                'count': count,
                'ecount': len(errors),
                'role': 'department'
            })

        messages.success(request, "Department data uploaded successfully.")
        return render(request, 'Error-Handler.html', {
            'errors': [],
            'count': count,
            'ecount': 0,
            'role': 'department'
        })


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
    columns = ['faculty_id', 'dob', 'name', 'email', 'gender', 'mobile', 'campus_id', 'qualification', 'department_name', 'status']
    return generate_excel_template_faculty(columns)



@csrf_exempt
def upload_faculty_excel(request):
    if request.method == 'POST':
        expected_columns = [
            'faculty_id', 'dob', 'name', 'email', 'gender', 'mobile',
            'campus_id', 'qualification', 'department_name', 'status'
        ]

        df = read_excel_and_return_dataframe(request.FILES['file'])

        if df is None:
            messages.error(request, "Failed to read the Excel file.")
            return redirect('bulkUp_home')

        if list(df.columns) != expected_columns:
            messages.error(request, "Uploaded file does not match the Faculty template columns.")
            return render(request, 'Error-Handler.html', {
                'errors': ["Template mismatch: expected columns are " + str(expected_columns)],
                'count': 0,
                'ecount': 1,
                'role': 'faculty'
            })

        count = 0
        errors = []

        for idx, row in df.iterrows():
            try:
                faculty_id = str(row['faculty_id']).strip()
                department_name = str(row['department_name']).strip()
                campus_id = str(row['campus_id']).strip()

                if Faculty.objects.filter(faculty_id=faculty_id).exists():
                    raise ValueError(f"Faculty with faculty_id '{faculty_id}' already exists.")

                try:
                    campus = Campus.objects.get(id=campus_id)
                except Campus.DoesNotExist:
                    raise ValueError(f"Campus with id '{campus_id}' not found.")

                try:
                    department = Department.objects.get(dept_name__iexact=department_name)
                except Department.DoesNotExist:
                    raise ValueError(f"Department with name '{department_name}' not found.")

                Faculty.objects.update_or_create(
                    faculty_id=faculty_id,
                    defaults={
                        'dob': row['dob'],
                        'name': str(row['name']).strip(),
                        'email': str(row['email']).strip(),
                        'gender': str(row['gender']).strip(),
                        'mobile': str(row['mobile']).strip(),
                        'campus': campus,
                        'qualification': str(row['qualification']).strip(),
                        'department': department,
                        'status': str(row['status']).strip(),
                    }
                )
                count += 1

            except Exception as e:
                errors.append(f"Row {idx + 2}: {str(e)}")

        if errors:
            messages.error(request, "Some rows could not be uploaded:\n" + "\n".join(errors))
            return render(request, 'Error-Handler.html', {
                'errors': errors,
                'count': count,
                'ecount': len(errors),
                'role': 'faculty'
            })

        messages.success(request, "Faculty data uploaded successfully.")
        return render(request, 'Error-Handler.html', {
            'errors': [],
            'count': count,
            'ecount': 0,
            'role': 'faculty'
        })

# =======================
# PROGRAM TEMPLATE & UPLOAD
# =======================
def download_program_template(request):
    columns = ['name', 'code', 'department_name', 'duration_years']
    return generate_excel_template_program(columns)

@csrf_exempt
def upload_program_excel(request):
    if request.method == 'POST':
        expected_columns = ['name', 'code', 'department_name', 'duration_years']
        df = read_excel_and_return_dataframe(request.FILES['file'])

        if df is None:
            messages.error(request, "Failed to read the Excel file.")
            return redirect('bulkUp_home')

        if list(df.columns) != expected_columns:
            messages.error(request, "Uploaded file does not match the Program template columns.")
            return render(request, 'Error-Handler.html', {
                'errors': [f"Template mismatch: expected columns are {expected_columns}"],
                'count': 0, 'ecount': 1, 'role': 'program'
            })

        count = 0
        errors = []

        for idx, row in df.iterrows():
            try:
                if Program.objects.filter(code=row['code']).exists():
                    raise ValueError(f"Program with code '{row['code']}' already exists.")

                # Find department by name
                dept_name = str(row['department_name']).strip()
                try:
                    department = Department.objects.get(dept_name=dept_name)
                except Department.DoesNotExist:
                    raise ValueError(f"Department with name '{dept_name}' not found.")
                except Department.MultipleObjectsReturned:
                    raise ValueError(f"Multiple departments found with name '{dept_name}'.")

                # Create or update Program
                Program.objects.update_or_create(
                    code=row['code'],
                    defaults={
                        'name': row['name'],
                        'department': department,
                        'duration_years': row['duration_years']
                    }
                )
                count += 1

            except Exception as e:
                errors.append(f"Row {idx + 2}: {str(e)}")  # Excel row index

        if errors:
            messages.error(request, "Some rows could not be uploaded.")
            return render(request, 'Error-Handler.html', {
                'errors': errors,
                'count': count,
                'ecount': len(errors),
                'role': 'program'
            })

        messages.success(request, "Program data uploaded successfully.")
        return render(request, 'Error-Handler.html', {
            'errors': [],
            'count': count,
            'ecount': 0,
            'role': 'program'
        })

# =======================
# STUDENT TEMPLATE & UPLOAD
# =======================
def download_student_template(request):
    columns = [
        'regd_no', 'name', 'email','gender', 'mobile', 'state_name', 'district_name',
        'city', 'country', 'prev_degree1_name', 'prev_degree1_university', 'prev_degree1_gpa',
        'prev_degree2_name', 'prev_degree2_university', 'prev_degree2_gpa',
        'blood_group', 'birthday', 'program_code', 'batch', 'status'
    ]
    return generate_excel_template_student(columns)





def clean_optional(value):
    return value if pd.notna(value) else None

@csrf_exempt
def upload_student_excel(request):
    if request.method == 'POST':
        expected_columns = [
            'regd_no', 'name', 'email','gender', 'mobile', 'state_name', 'district_name',
            'city', 'country', 'prev_degree1_name', 'prev_degree1_university', 'prev_degree1_gpa',
            'prev_degree2_name', 'prev_degree2_university', 'prev_degree2_gpa',
            'blood_group', 'birthday', 'program_code', 'batch', 'status'
        ]

        print("Received file:", request.FILES.get('file'))

        df = read_excel_and_return_dataframe(request.FILES['file'])
        if df is None:
            messages.error(request, "Failed to read the Excel file.")
            return redirect('bulkUp_home')

        if list(df.columns) != expected_columns:
            messages.error(request, "Uploaded file does not match the Student template columns.")
            return render(request, 'Error-Handler.html', {
                'errors': ["Template mismatch: expected columns are " + str(expected_columns)],
                'count': 0, 'ecount': 1, 'role': 'student'
            })

        count = 0
        errors = []

        for idx, row in df.iterrows():
            try:
                # Validate program_code exists
                try:
                    program = Program.objects.get(programme_code=row['program_code'])
                except Program.DoesNotExist:
                    raise ValueError(f"Program code '{row['program_code']}' not found.")

                if Student.objects.filter(regd_no=row['regd_no']).exists():
                    raise ValueError(f"Student with regd_no '{row['regd_no']}' already exists.")

                Student.objects.update_or_create(
                    regd_no=row['regd_no'],
                    defaults={
                        'name': row['name'],
                        'email': row['email'],
                        'gender': row['gender'],
                        'mobile': row['mobile'],
                        'state_name': row['state_name'],
                        'district_name': row['district_name'],
                        'city': row['city'],
                        'country': row['country'],
                        'prev_degree1_name': clean_optional(row['prev_degree1_name']),
                        'prev_degree1_university': clean_optional(row['prev_degree1_university']),
                        'prev_degree1_gpa': safe_decimal(row['prev_degree1_gpa']),
                        'prev_degree2_name': clean_optional(row['prev_degree2_name']),
                        'prev_degree2_university': clean_optional(row['prev_degree2_university']),
                        'prev_degree2_gpa': safe_decimal(row['prev_degree2_gpa']),
                        'blood_group': row['blood_group'],
                        'birthday': row['birthday'],
                        'program_id': program.id,
                        'batch': row['batch'],
                        'status': row['status'],
                    }
                )
                count += 1
            except Exception as e:
                errors.append(f"Row {idx + 2}: {str(e)}")  # +2 for Excel row number (header + 0-index)

        if errors:
            messages.error(request, "Some rows could not be uploaded:\n" + "\n".join(errors))
            return render(request, 'Error-Handler.html', {
                'errors': errors, 'count': count, 'ecount': len(errors), 'role': 'student'
            })

        messages.success(request, "Student data uploaded successfully.")
        return render(request, 'Error-Handler.html', {
            'errors': errors, 'count': count, 'ecount': len(errors), 'role': 'student'
        })
    



#=======================
# COURSE TEMPLATE & UPLOAD
#=======================
def download_course_template(request):
    columns = [
        'programme_code', 'batch', 'paper_code', 'paper_title', 'semester',
        'sequence', 'category', 'credits', 'cie_max', 'cie_max_atp',
        'cie_max_psn', 'cie_max_brn', 'cie_max_ndg', 'ese_max',
        'ese_max_atp', 'ese_max_psn', 'ese_max_brn', 'ese_max_ndg',
        'cie_wtg', 'ese_wtg'
    ]
    return generate_excel_template_course(columns)

@csrf_exempt
def upload_course_excel(request):
    if request.method == 'POST':
        expected_columns = [
            'programme_code', 'batch', 'paper_code', 'paper_title', 'semester',
            'sequence', 'category', 'credits', 'cie_max', 'cie_max_atp',
            'cie_max_psn', 'cie_max_brn', 'cie_max_ndg', 'ese_max',
            'ese_max_atp', 'ese_max_psn', 'ese_max_brn', 'ese_max_ndg',
            'cie_wtg', 'ese_wtg'
        ]

        df = read_excel_and_return_dataframe(request.FILES['file'])
        if df is None:
            messages.error(request, "Failed to read the Excel file.")
            return redirect('bulkUp_home')

        if list(df.columns) != expected_columns:
            messages.error(request, "Uploaded file does not match the Course template columns.")
            return render(request, 'Error-Handler.html', {
                'errors': ["Template mismatch: expected columns are " + str(expected_columns)],
                'count': 0, 'ecount': 1, 'role': 'course'
            })

        count = 0
        errors = []

        for idx, row in df.iterrows():
            try:
                # Validate required fields
                required_fields = ['programme_code', 'batch', 'paper_code', 'paper_title', 'semester', 'sequence', 'category', 'credits', 'cie_max', 'ese_max', 'cie_wtg', 'ese_wtg']
                for field in required_fields:
                    if pd.isna(row[field]) or row[field] == '':
                        raise ValueError(f"Field '{field}' is required and cannot be empty.")
                # Validate Programme Exists 
                try:
                    programme = Program.objects.get(programme_code=row['programme_code'], batch=int(row['batch']))
                except Program.DoesNotExist:
                    raise ValueError(f"Programme with code '{row['programme_code']}' and '{row['batch']}' does not exist.")
                # Validate programme_code and batch
                programme_code = str(row['programme_code']).strip()
                batch = int(row['batch'])

                # Check if course already exists
                if Course.objects.filter(programme_code=programme_code, batch=batch, paper_code=row['paper_code']).exists():
                    raise ValueError(f"Course with code '{row['paper_code']}' for programme '{programme_code}' and batch '{batch}' already exists.")

                # Create or update Course
                Course.objects.update_or_create(
                    programme_code=programme_code,
                    batch=batch,
                    paper_code=row['paper_code'],
                    defaults={
                        'paper_title': row['paper_title'],
                        'semester': int(row['semester']),
                        'sequence': int(row['sequence']),
                        'category': row['category'],
                        'credits': safe_decimal(row['credits']),
                        'cie_max': int(row['cie_max']),
                        'cie_max_atp': int(row.get('cie_max_atp', 0)),
                        'cie_max_psn': int(row.get('cie_max_psn', 0)),
                        'cie_max_brn': int(row.get('cie_max_brn', 0)),
                        'cie_max_ndg': int(row.get('cie_max_ndg', 0)),
                        'ese_max': int(row['ese_max']),
                        'ese_max_atp': int(row.get('ese_max_atp', 0)),
                        'ese_max_psn': int(row.get('ese_max_psn', 0)),
                        'ese_max_brn': int(row.get('ese_max_brn', 0)),
                        'ese_max_ndg': int(row.get('ese_max_ndg', 0)),
                        'cie_wtg': safe_decimal(row['cie_wtg']),
                        'ese_wtg': safe_decimal(row['ese_wtg']),
                    }
                )
                count += 1
            except Exception as e:
                errors.append(f"Row {idx + 2}: {str(e)}")
        if errors:
            messages.error(request, "Some rows could not be uploaded:\n" + "\n".join(errors))
            return render(request, 'Error-Handler.html', {
                'errors': errors,
                'count': count,
                'ecount': len(errors),
                'role': 'course'
            })


# =======================
# ERROR PDF GENERATION


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