
from django.shortcuts import render, redirect
from .models import Program, Student,State,District
from datetime import datetime
from django.contrib import messages  
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

def studenthome(request):
    return render(request,'home.html')


def add_student(request):
    states = State.objects.all()
    programs = Program.objects.all()

    if request.method == 'POST':
        regd_no = request.POST.get('regd_no')
        name = request.POST.get('name')
        email = request.POST.get('email')
        state_id = request.POST.get('state')
        district_id = request.POST.get('district')
        city = request.POST.get('city')
        prev_degree1_name = request.POST.get('prev_degree1_name')
        prev_degree1_university = request.POST.get('prev_degree1_university')
        prev_degree1_gpa = request.POST.get('prev_degree1_gpa') or None
        prev_degree2_name = request.POST.get('prev_degree2_name')
        prev_degree2_university = request.POST.get('prev_degree2_university')
        prev_degree2_gpa = request.POST.get('prev_degree2_gpa') or None
        blood_group = request.POST.get('blood_group')
        birthday = request.POST.get('birthday') or None
        batch = request.POST.get('batch')
        status = request.POST.get('status')
        program_id = request.POST.get('program')

        if Student.objects.filter(regd_no=regd_no).exists():
            messages.error(request, f"Registration number {regd_no} already exists.")
        elif Student.objects.filter(email=email).exists():
            messages.error(request, f"Email {email} is already in use.")
        else:
            program = Program.objects.get(id=program_id)
            state_name = State.objects.get(id=state_id).name
            district_name = District.objects.get(id=district_id).name

            Student.objects.create(
                regd_no=regd_no,
                name=name,
                email=email,
                state_name=state_name,
                district_name=district_name,
                city=city,
                prev_degree1_name=prev_degree1_name,
                prev_degree1_university=prev_degree1_university,
                prev_degree1_gpa=prev_degree1_gpa,
                prev_degree2_name=prev_degree2_name,
                prev_degree2_university=prev_degree2_university,
                prev_degree2_gpa=prev_degree2_gpa,
                blood_group=blood_group,
                birthday=birthday,
                batch=batch,
                status=status,
                program=program
            )
            return redirect('studenthome')

    return render(request, 'student_form.html', {
        'states': states,
        #'districts':district,
        'programs': programs,
        'gpa_choices': [round(i * 0.1, 2) for i in range(0, 101)],
        'current_year': datetime.now().year,
        'blood_groups': Student.BLOOD_GROUP_CHOICES,
        'status': Student.STATUS_CHOICES,
    })




def update_student(request, regd_no):
    student = get_object_or_404(Student, regd_no=regd_no)
    programs = Program.objects.all()

    if request.method == 'POST':
        student.name = request.POST.get('name')
        student.email = request.POST.get('email')
        state_id = request.POST.get('state')
        district_id = request.POST.get('district')
        student.state_name = State.objects.get(id=state_id).name
        student.district_name = District.objects.get(id=district_id).name
        student.city = request.POST.get('city')
        student.prev_degree1_name = request.POST.get('prev_degree1_name')
        student.prev_degree1_university = request.POST.get('prev_degree1_university')
        student.prev_degree1_gpa = request.POST.get('prev_degree1_gpa') or None
        student.prev_degree2_name = request.POST.get('prev_degree2_name')
        student.prev_degree2_university = request.POST.get('prev_degree2_university')
        student.prev_degree2_gpa = request.POST.get('prev_degree2_gpa') or None
        student.blood_group = request.POST.get('blood_group')
        student.birthday = request.POST.get('birthday') or None
        student.batch = request.POST.get('batch')
        student.status = request.POST.get('status')

        program_id = request.POST.get('program')
        student.program = Program.objects.get(id=program_id)

        student.save()
        messages.success(request, "Student details updated successfully.")
        return redirect('studenthome')

    return render(request, 'student_update_form.html', {
        'student': student,
        'programs': programs,
        'blood_groups': Student.BLOOD_GROUP_CHOICES,
        'status_choices': Student.STATUS_CHOICES
    })


def get_states(request):
    states = State.objects.all().values('id', 'name')
    return JsonResponse(list(states), safe=False)

def get_districts_by_state(request, state_id):
    districts = District.objects.filter(state_id=state_id).values('id', 'name')
    return JsonResponse(list(districts), safe=False)


