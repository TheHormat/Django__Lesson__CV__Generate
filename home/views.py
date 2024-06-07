from django.shortcuts import render
from django.contrib import messages
from .models import Profile
from django.http import HttpResponse
from django.template import loader
import pdfkit
# Create your views here.

def homePage(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        summary = request.POST.get("summary")
        degree = request.POST.get("degree")
        school = request.POST.get("school")
        university = request.POST.get("university")
        previous_work = request.POST.get("previous_work")
        skills = request.POST.get("skills")
        
        profile = Profile (
            name = name,
            email = email,
            phone = phone,
            summary = summary,
            degree = degree,
            school = school,
            university = university,
            previous_work = previous_work,
            skills = skills,
        )
        
        profile.save()
        
        messages.success(request,"CV-niz uğurla yaradıldı...")
        
    return render(request, 'index.html')


def resume(request, id):
    user_profile = Profile.objects.get(id=id)
    template = loader.get_template("resume.html")
    html = template.render({"user_profile": user_profile})
    options = {
        "page-size": "Letter",
        "encoding": "UTF-8",
    }
    pdf = pdfkit.from_string(html, False, options)
    response = HttpResponse(pdf, content_type="application/pdf")
    # response["Content-Disposition"] = "attachment"
    # filename = "download.pdf"
    response['Content-Disposition'] = f'attachment; filename="download.pdf"'
    return response


def resumeList(request):
    profiles = Profile.objects.all()
    context = {
        "profiles": profiles
    }
    return render(request, 'list.html', context)