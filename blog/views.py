from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
import re
from django.shortcuts import render, redirect
from .models import Profile, Paper, Notes, Resources, Blog, Contact
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from .utils import extract_text, ask_ai
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai
import json


def home(request):
    return render(request,'blog/homepage.html')


def valid_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters."

    if not re.search(r"[A-Z]", password):
        return False, "Password must contain an uppercase letter."

    if not re.search(r"[a-z]", password):
        return False, "Password must contain a lowercase letter."

    if not re.search(r"\d", password):
        return False, "Password must contain a digit."

    if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]", password):
        return False, "Password must contain a special character."

    return True, "Valid password"


def register(request):
    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")


        is_valid, message = valid_password(password1)

        if not is_valid:
            messages.error(request, message)
            return redirect("register")


        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if len(username)>=3:
            if User.objects.filter(username=username).exists():
               messages.error(request, "Username already exists.")
               return redirect("register")
        else:
            messages.error(request, "Please enter a valid username.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("register")


        user=User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )


        messages.success(request, "Account created successfully.")

        return redirect("login")

    return render(request, "blog/register.html")
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        user = auth.authenticate(username=username, password=password1)
        if user is not None:
            auth.login(request=request, user=user)
            return render(request, "blog/homepage.html")

        else:
            messages.info(request, 'Username or password is incorrect')
            return redirect('login')
    else:
             return render(request, 'blog/login.html')
def logout_user(request):
        auth.logout(request)
        return redirect('login')
def password_reset(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")

@login_required(login_url='login')
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        if request.FILES.get("image"):
            profile.image = request.FILES["image"]
            profile.save()
            return redirect("profile")

    return render(request, "blog/profile.html", {"profile": profile})

@login_required(login_url='login')
def paper(request):
    papers = Paper.objects.all()
    title = request.GET.get("title")
    year = request.GET.get("year")
    print("Year =", year)
    print("Title =", title)

    if year:
        papers = papers.filter(year=year)
    if title:
        papers = papers.filter(title=title)
    print("Count =", papers.count())
    years = Paper.objects.values_list('year', flat=True).distinct()
    title = Paper.objects.values_list('title', flat=True).distinct()
    return render(request, "blog/paper.html", {
        "papers": papers,
        'years': years,
         'title': title,
    })
@login_required(login_url='login')
def Notes_list(request):
    Note = Notes.objects.all()
    Subject=request.GET.get("subject")
    if Subject:
        Note=Note.filter(Subject=Subject)
    subjects = Notes.objects.values_list("Subject",flat=True).distinct()

    return render(request, "blog/Notes.html", {"Notes": Note, "subject": subjects})
@login_required(login_url='login')
def Resources_list(request):
    Resource = Resources.objects.all()
    return render(request, "blog/Resource.html", {"Resources": Resource})
@login_required(login_url='login')
def blog_list(request):

        blog = Blog.objects.first()

        if blog and blog.image:
            print(blog.image.url)

        return render(request, "blog/blog.html", {"blog": Blog.objects.all()})
@login_required(login_url='login')
def about(request):
    return render(request, "blog/about.html")
@login_required(login_url='login')
def contact_list(request):
    if request.method == "POST":
        Contact.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            message=request.POST.get("message")
        )
        messages.success(request, "Message sent successfully!")

    return render(request, "blog/contact_list.html",{"contact_list": contact_list})

import requests
import tempfile
import os

def analyze_paper(request, paper_id):

    paper = get_object_or_404(Paper, id=paper_id)

    file_url = paper.file.url
    response = requests.get(file_url)

    if response.status_code != 200:
        return render(request, "blog/analysis.html", {
            "result": "Error: Could not download file from Cloudinary."
        })


    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(response.content)
        tmp_path = tmp.name

    try:

        text = extract_text(tmp_path)
        text = re.sub(r'\s+', ' ', text)

        prompt = f"""
You are an expert university exam analyst.

Analyze the following exam paper and return:

1. Subject Name
2. Important Topics
3. Frequently Asked Concepts
4. Difficulty Level (Easy/Medium/Hard)
5. 5 Study Tips

Write the response in proper markdown with headings and bullet points.
Keep answer under 300 words.

Paper:
{text[:3000]}
        """

        result = ask_ai(prompt)

    except Exception as e:
        result = f"Error during analysis: {str(e)}"

    finally:
        os.remove(tmp_path)  #

    return render(request, "blog/analysis.html", {"result": result})
from django.conf import settings
genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash")

@csrf_exempt
def chatbot(request):
    if request.method == "POST":
        data = json.loads(request.body)
        message = data.get("message", "")

        prompt = f"""
You are AKTU Student Help AI Assistant.

Rules:
- Help B.Tech students with studies.
- Explain concepts in simple language.
- Help with Python, C, DSA, DBMS, Operating Systems, Mathematics, Physics, and Engineering subjects.
- Answer AKTU-related academic questions when possible.
- Be concise and student-friendly.
- If asked non-academic questions, answer normally.

User Question:
{message}
"""

        response = model.generate_content(prompt)

        return JsonResponse({
            "reply": response.text
        })

    return render(request, "blog/chatbot.html")