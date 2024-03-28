from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings

from accounts.decorators import admin_required, lecturer_required
from accounts.models import User
from .forms import SessionForm, SemesterForm, NewsAndEventsForm
from .models import *



# Yangilik va voqelar uchun 

@login_required
def home_view(request):
    items = NewsAndEvents.objects.all().order_by("-updated_date")
    context = {
        "title": "Yangiliklar",
        "items": items,
    }
    return render(request, "core/index.html", context)


@login_required
def post_add(request):
    if request.method == "POST":
        form = NewsAndEventsForm(request.POST)
        title = request.POST.get("title")
        if form.is_valid():
            form.save()

            messages.success(request, (title + " yuklangan."))
            return redirect("home")
        else:
            messages.error(request, "Quyidagi xato(lar)ni tuzating.")
    else:
        form = NewsAndEventsForm()
    return render(
        request,
        "core/post_add.html",
        {
            "title": "Post joylash",
            "form": form,
        },
    )


@login_required
@lecturer_required
def edit_post(request, pk):
    instance = get_object_or_404(NewsAndEvents, pk=pk)
    if request.method == "POST":
        form = NewsAndEventsForm(request.POST, instance=instance)
        title = request.POST.get("title")
        if form.is_valid():
            form.save()

            messages.success(request, (title + " yangilandi."))
            return redirect("home")
        else:
            messages.error(request, "Quyidagi xato(lar)ni tuzating.")
    else:
        form = NewsAndEventsForm(instance=instance)
    return render(
        request,
        "core/post_add.html",
        {
            "title": "Post taxrirlash",
            "form": form,
        },
    )


@login_required
@lecturer_required
def delete_post(request, pk):
    post = get_object_or_404(NewsAndEvents, pk=pk)
    title = post.title
    post.delete()
    messages.success(request, (title + " "))
    return redirect("home")



# Sessiyalar uchun

@login_required
@lecturer_required
def session_list_view(request):
    
    sessions = Session.objects.all().order_by("-is_current_session", "-session")
    return render(request, "core/session_list.html", {"sessions": sessions})


@login_required
@lecturer_required
def session_add_view(request):

    if request.method == "POST":
        form = SessionForm(request.POST)
        if form.is_valid():
            data = form.data.get(
                "is_current_session"
            )  # returns string of 'True' if the user selected Yes
            print(data)
            if data == "true":
                sessions = Session.objects.all()
                if sessions:
                    for session in sessions:
                        if session.is_current_session == True:
                            unset = Session.objects.get(is_current_session=True)
                            unset.is_current_session = False
                            unset.save()
                    form.save()
                else:
                    form.save()
            else:
                form.save()
            messages.success(request, "Sessiya muvafaqiyatli qo'shildi!")
            return redirect("session_list")

    else:
        form = SessionForm()
    return render(request, "core/session_update.html", {"form": form})


@login_required
@lecturer_required
def session_update_view(request, pk):
    session = Session.objects.get(pk=pk)
    if request.method == "POST":
        form = SessionForm(request.POST, instance=session)
        data = form.data.get("is_current_session")
        if data == "true":
            sessions = Session.objects.all()
            if sessions:
                for session in sessions:
                    if session.is_current_session == True:
                        unset = Session.objects.get(is_current_session=True)
                        unset.is_current_session = False
                        unset.save()

            if form.is_valid():
                form.save()
                messages.success(request, "Sessiya muvafaqiyatli yangilandi!")
                return redirect("session_list")
        else:
            form = SessionForm(request.POST, instance=session)
            if form.is_valid():
                form.save()
                messages.success(request, "Sessiya muvafaqiyatli yangilandi! ")
                return redirect("session_list")

    else:
        form = SessionForm(instance=session)
    return render(request, "core/session_update.html", {"form": form})


@login_required
@lecturer_required
def session_delete_view(request, pk):
    session = get_object_or_404(Session, pk=pk)

    if session.is_current_session:
        messages.error(request, "Joriy sessiyani oʻchira olmaysiz")
        return redirect("session_list")
    else:
        session.delete()
        messages.success(request, "Sessiya muvaffaqiyatli o'chirildi!")
    return redirect("session_list")










@login_required
@lecturer_required
def semester_list_view(request):
    semesters = Semester.objects.all().order_by("-is_current_semester", "-semester")
    return render(
        request,
        "core/semester_list.html",
        {
            "semesters": semesters,
        },
    )


@login_required
@lecturer_required
def semester_add_view(request):
    if request.method == "POST":
        form = SemesterForm(request.POST)
        if form.is_valid():
            data = form.data.get(
                "is_current_semester"
            )  # returns string of 'True' if the user selected Yes
            if data == "True":
                semester = form.data.get("semester")
                ss = form.data.get("session")
                session = Session.objects.get(pk=ss)
                try:
                    if Semester.objects.get(semester=semester, session=ss):
                        messages.error(
                            request,
                            semester
                            + " semester in "
                            + session.session
                            + " session already exist",
                        )
                        return redirect("add_semester")
                except:
                    semesters = Semester.objects.all()
                    sessions = Session.objects.all()
                    if semesters:
                        for semester in semesters:
                            if semester.is_current_semester == True:
                                unset_semester = Semester.objects.get(
                                    is_current_semester=True
                                )
                                unset_semester.is_current_semester = False
                                unset_semester.save()
                        for session in sessions:
                            if session.is_current_session == True:
                                unset_session = Session.objects.get(
                                    is_current_session=True
                                )
                                unset_session.is_current_session = False
                                unset_session.save()

                    new_session = request.POST.get("session")
                    set_session = Session.objects.get(pk=new_session)
                    set_session.is_current_session = True
                    set_session.save()
                    form.save()
                    messages.success(request, "Oraliq mavfaqiyatli qo'shildi.")
                    return redirect("semester_list")

            form.save()
            messages.success(request, "Oraliq mavfaqiyatli qo'shildi. ")
            return redirect("semester_list")
    else:
        form = SemesterForm()
    return render(request, "core/semester_update.html", {"form": form})


@login_required
@lecturer_required
def semester_update_view(request, pk):
    semester = Semester.objects.get(pk=pk)
    if request.method == "POST":
        if (
            request.POST.get("is_current_semester") == "True"
        ):  # returns string of 'True' if the user selected yes for 'is current semester'
            unset_semester = Semester.objects.get(is_current_semester=True)
            unset_semester.is_current_semester = False
            unset_semester.save()
            unset_session = Session.objects.get(is_current_session=True)
            unset_session.is_current_session = False
            unset_session.save()
            new_session = request.POST.get("session")
            form = SemesterForm(request.POST, instance=semester)
            if form.is_valid():
                set_session = Session.objects.get(pk=new_session)
                set_session.is_current_session = True
                set_session.save()
                form.save()
                messages.success(request, "Oraliq muvafaqiyatli yangilandi !")
                return redirect("semester_list")
        else:
            form = SemesterForm(request.POST, instance=semester)
            if form.is_valid():
                form.save()
                return redirect("semester_list")

    else:
        form = SemesterForm(instance=semester)
    return render(request, "core/semester_update.html", {"form": form})


@login_required
@lecturer_required
def semester_delete_view(request, pk):
    semester = get_object_or_404(Semester, pk=pk)
    if semester.is_current_semester:
        messages.error(request, "Siz joriy semestrni o'chira olmaysiz.")
        return redirect("semester_list")
    else:
        semester.delete()
        messages.success(request, "Semestr muvaffaqiyatli oʻchirildi.")
    return redirect("semester_list")


@login_required
@admin_required
def dashboard_view(request):
    logs = ActivityLog.objects.all().order_by("-created_at")[:10]
    context = {
        "student_count": User.get_student_count(),
        "lecturer_count": User.get_lecturer_count(),
        "superuser_count": User.get_superuser_count(),
        "logs": logs,
    }
    return render(request, "core/dashboard.html", context)



from django.shortcuts import render

def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)