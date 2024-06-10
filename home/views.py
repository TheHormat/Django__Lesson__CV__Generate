from django.core.mail import EmailMessage
from django.shortcuts import render
from django.contrib import messages
from .models import Profile, Contact
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.template.loader import render_to_string
import pdfkit
from django.conf import settings
from django.utils import translation
from django.urls.base import resolve, reverse
from django.urls.exceptions import Resolver404
from urllib.parse import urlparse

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

        profile = Profile(
            name=name,
            email=email,
            phone=phone,
            summary=summary,
            degree=degree,
            school=school,
            university=university,
            previous_work=previous_work,
            skills=skills,
        )

        profile.save()

        messages.success(request, "CV-niz uğurla yaradıldı...")

    return render(request, "index.html")


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
    response["Content-Disposition"] = 'attachment; filename="download.pdf"'
    return response


def resumeList(request):
    profiles = Profile.objects.all()
    context = {"profiles": profiles}
    return render(request, "list.html", context)


def contactPage(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        contact = Contact(
            name=name,
            email=email,
            message=message,
        )

        contact.save()

        html_message = render_to_string(
            "email.html",
            {
                "name": name,
            },
        )

        email_message = EmailMessage(
            subject="Yeni Müraciət",
            body=html_message,
            from_email="codersaz@gmail.com",
            to=[email],
        )

        email_message.content_subtype = "html"

        email_message.send()

        messages.success(request, "Müraciətiniz uğurla göndərildi...")

    return render(request, "contact.html")


def set_language(request, language):
    for lang, _ in settings.LANGUAGES:
        translation.activate(lang)
        try:
            view = resolve(urlparse(request.META.get("HTTP_REFERER")).path)
        except Resolver404:
            view = None
        if view:
            break
    if view:
        translation.activate(language)
        next_url = reverse(view.url_name, args=view.args, kwargs=view.kwargs)
        response = HttpResponseRedirect(next_url)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    else:
        response = HttpResponseRedirect("/")
    return response