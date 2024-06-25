from django.shortcuts import render, redirect
from . models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        try:
            company = Company.objects.get(user=request.user)
            context = {'user_type': 'company', 'profile': company}
        except Company.DoesNotExist:

            student = Student.objects.get(user=request.user)
            context = {'user_type': 'student', 'profile': student}

        return render(request, 'index.html', context)

    return render(request, 'index.html')
def user_logout(request):
    logout(request)
    return redirect('index')

def company_registration(request):
    if request.method=="POST":
        company_name = request.POST['company_name']
        company_address = request.POST['address']
        company_bio = request.POST['company_bio']
        website = request.POST['company_web']
        contact_number = request.POST['phone_number']
        email = request.POST['email']
        password = request.POST['password']

        try:
            if User.objects.filter(username=email).exists():
                raise IntegrityError('Username already exists.')

            user = User.objects.create_user(email=email, username=email, password=password)
            company = Company.objects.create(user=user, company_name=company_name, company_address=company_address, company_bio=company_bio, website=website, contact_number=contact_number, email= email, type="company")

            user.save()
            company.save()
            messages.success(request, 'Account created successful!')
            return redirect('company_login')

        except IntegrityError as e:
            messages.success(request, f'Username already exists. Please choose a different username.')
            return render(request, 'company_registration.html',{'company_name': company_name, 'company_address': company_address, 'company_bio': company_bio, 'website': website, 'contact_number': contact_number, 'email': email, })

        except Exception as e:
            messages.success(request, 'There was an error in signup. {str(e)}')
            return render(request, 'company_registration.html')
    else:
        return render(request, 'company_registration.html')


def company_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            user1 = Company.objects.get(user=user)
            if user1.type == "company":
                login(request, user)

                return redirect('index')
        else:
            messages.success(request, 'Invalid username or password')
            return render(request, 'company_login.html')
    else:
        return render(request, 'company_login.html')
def add_job(request):
    if not request.user.is_authenticated:
        return redirect('company_login')
    user = request.user
    company = Company.objects.get(user=user)
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        email = request.POST['email']
        time_date = request.POST['time_date']  # You may need to adjust the date input handling
        skill = request.POST['skill']
        job_type = request.POST['job_type']
        location = request.POST['location']
        category = request.POST['category']


        try:
            job = Job.objects.create(
                company=company,
                title=title,
                description=description,
                email=email,
                time_date=time_date,
                skill=skill,
                job_type=job_type,
                location=location,
                category=category,

            )
            job.save()
            messages.success(request, 'Job added successfully!')
            return redirect('index')  # Redirect to the same page or any other page as needed

        except Exception as e:
            messages.error(request, f'There was an error adding the job: {str(e)}')

    return render(request, 'add_job.html',{'user_type': 'company','profile': company,})

  
def company_profile(request, comp_id):
    if not request.user.is_authenticated:
        return redirect("company_login")
    company = Company.objects.get(id=comp_id)
    if request.method == "POST":
        company_name = request.POST['company_name']
        company_address = request.POST['address']
        company_bio = request.POST['company_bio']
        website = request.POST['company_web']
        contact_number = request.POST['phone_number']
        email = request.POST['email']
        password = request.POST['password']

        company.company_name = company_name
        company.company_address = company_address
        company.company_bio = company_bio
        company.website = website
        company.contact_number = contact_number
        company.email = email
        company.user.username = email
        company.user.set_password = password

        company.save()
        company.user.save()

        messages.success(request, 'Account updated successful!')

        return render(request, 'company-profile.html', {'user_type': 'company','profile': company,'company': company})

    return render(request, 'company-profile.html', {'user_type': 'company','profile': company,'company': company})


def my_joblist(request, comp_id):
    if request.user.is_authenticated:
        profile = Company.objects.get(user=request.user)

        company = get_object_or_404(Company, pk=comp_id)

        # Query jobs associated with the company
        joblist = Job.objects.filter(company=company)

        return render(request, "company_joblist.html", {'user_type': 'company', 'profile': profile, 'joblist': joblist, 'comp_id': comp_id})

    else:
        return redirect('company_login')


      

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            user1 = Student.objects.get(user=user)
            if user1.type == "student":
                login(request, user)

                return redirect('index')
        else:
            messages.success(request, 'Invalid username or password')
            return render(request, 'user_login.html')
    else:
        return render(request, 'user_login.html')

# user register
def user_register(request):
    if request.method=="POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        category = request.POST['category']

        try:
            if User.objects.filter(username=username).exists():
                raise IntegrityError('Username already exists.')

            user = User.objects.create_user(username=username, email=email, password=password)
            student = Student.objects.create(user=user, username=username, category=category, type="student")

            user.save()
            student.save()
            messages.success(request, 'Account created successful!')
            return redirect('user_login')

        except IntegrityError as e:
            messages.success(request, f'Username already exists. Please choose a different username.')
            return render(request, 'user_register.html',{'username': username, 'email': email, 'password': password, 'category': category })

        except Exception as e:
            messages.success(request, 'There was an error in signup. {str(e)}')
            return render(request, 'user_register.html')
    else:
        return render(request, 'user_register.html')
    
def user_job_list(request):
    if request.user.is_authenticated:
        try:
            user1 = Company.objects.get(user=request.user)

            all_jobs = Job.objects.all()
            context = {'joblist': all_jobs, 'user_type': 'company','profile': user1}    
        except Company.DoesNotExist:

            user1 = Student.objects.get(user=request.user)

            suggested_jobs = Job.objects.filter(category=user1.category)
            context = {'joblist': suggested_jobs ,'user_type': 'student','profile': user1}
            
        return render(request, 'user_job_list.html', context)
    all_jobs = Job.objects.all()
    context = {'joblist': all_jobs}
    return render(request, 'user_job_list.html', context)

def student_profile(request, stu_id):
    student = Student.objects.get(id=stu_id)
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        category = request.POST['category']

        student.username = username
        student.email = email
        student.category = category
        student.user.username = username
        student.user.set_password = password

        student.save()
        student.user.save()

        messages.success(request, 'Account updated successful!')

        return render(request, 'student_profile.html', {'user_type': 'company','profile': student,'student': student})

    return render(request, 'student_profile.html', {'user_type': 'company','profile': student,'student': student})


def job_details(request, job_id):
    if request.user.is_authenticated:
        try:
            profile = Company.objects.get(user=request.user)
            user_type = 'company'
        except Company.DoesNotExist:

            profile = Student.objects.get(user=request.user)
            user_type = 'student'

        job = Job.objects.get(id=job_id)
        return render(request, "job_details.html", {'user_type': user_type, 'profile': profile, 'job': job}, )

    job = Job.objects.get(id=job_id)
    return render(request, "job_details.html", {'job': job}, )

def edit_job(request, job_id,comp_id):
    if not request.user.is_authenticated:
        return redirect('company_login')

    user = request.user
    company = user.company

    job = get_object_or_404(Job, pk=job_id)

    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        email = request.POST.get('email')
        time_date = request.POST.get('time_date')
        skill = request.POST.get('skill')
        job_type = request.POST.get('job_type')
        location = request.POST.get('location')
        category = request.POST.get('category')

        try:
            job.title = title
            job.description = description
            job.email = email
            job.time_date = time_date
            job.skill = skill
            job.job_type = job_type
            job.location = location
            job.category = category
            job.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('index')  # Redirect to the same page or any other page as needed

        except Exception as e:
            messages.error(request, f'There was an error updating the job: {str(e)}')

    return render(request, 'edit_job.html', {'job': job, 'user_type': 'company', 'profile': company})


def delete_job(request, job_id):
    if request.method == 'POST':
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You don't have permission to access this page.")

        # Get the job object
        job = get_object_or_404(Job, pk=job_id)

        # Ensure the user owns the job
        if job.company.user != request.user:
            return HttpResponseForbidden("You don't have permission to delete this job.")

        # Delete the job
        job.delete()

        messages.success(request, 'Job deleted successfully!')
        return redirect('my_joblist', comp_id=request.user.company.id)
    else:
        return HttpResponseForbidden("Invalid request method.")