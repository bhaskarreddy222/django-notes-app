from django.shortcuts import render, redirect
from .models import Note
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required(login_url='/login/')
def editor(request):
    docid = int(request.GET.get('docid', 0))
    notes = Note.objects.all()

    if request.method == 'POST':
        docid = int(request.POST.get('docid', 0))
        title = request.POST.get('title')
        content = request.POST.get('content', '')

        if docid > 0:
            note = Note.objects.get(pk=docid)
            note.title = title
            note.content = content
            note.save()
            return redirect('/?docid=%i' % docid)
        else:
            note = Note.objects.create(title=title, content=content)
            return redirect('/?docid=%i' % note.id)

    note = Note.objects.get(pk=docid) if docid > 0 else ''

    return render(request, 'editor.html', {
        'docid': docid,
        'notes': notes,
        'note': note
    })


@login_required(login_url='/login/')
def delete_note(request, docid):
    Note.objects.get(pk=docid).delete()
    return redirect('/?docid=0')


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, "Username not found")
            return redirect('/login/')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('editor')

        messages.error(request, "Wrong password")
    return render(request, "login.html")


def register_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('/register/')

        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()
        messages.success(request, "Account created successfully")
        return redirect('/login/')
    return render(request, "register.html")


def custom_logout(request):
    logout(request)
    return redirect('login')
