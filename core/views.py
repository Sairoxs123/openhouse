from django.shortcuts import render, redirect
from .models import *

# Create your views here.


def timechecker(results):
    timeslots = [
        "8:00",
        "8:15",
        "8:30",
        "8:45",
        "9:00",
        "9:15",
    ]

    for i in results:
        if i.time in timeslots:
            timeslots.remove(i.time)

    return timeslots


def bookingcheck(teacherinst):
    students = [x for x in Students.objects.all()]
    reservations = Reservations.objects.all().filter(teacher=teacherinst)

    for i in reservations:
        if i.student in students:
            students.remove(i.student)

    return students



teacherpassword = "hello"


def index(request):
    return render(request, "index.html")


def teacher(request):
    if request.method == "POST":
        teacher = request.POST["teacher"]
        password = request.POST["pass"]

        if password == teacherpassword:
            request.session["teacher"] = teacher

            teacherinst = Teachers.objects.get(name=request.session["teacher"])

            reservations = Reservations.objects.all().filter(teacher=teacherinst)

            return render(request, "teacher.html", {"teacher":teacher, "reservations":reservations})

        else:
            return render(request, "teacher-login.html", {"teachers": Teachers.objects.all(), "wrong":True})

    try:
        teacherinst = Teachers.objects.get(name=request.session["teacher"])
        reservations = Reservations.objects.all().filter(teacher=teacherinst).order_by('time')
        return render(request, "teacher.html", {"teacher":request.session["teacher"], "reservations":reservations})

    except:
        teachers = Teachers.objects.all()

        return render(request, "teacher-login.html", {"teachers": teachers})


def add(request):
    if request.method == "POST":
        student = request.POST["student"]
        time = request.POST["time"]

        teacherinst = Teachers.objects.get(name=request.session["teacher"])
        studentinst = Students.objects.get(jssid=student)

        try:
            results = Reservations.objects.get(student=studentinst, teacher=teacherinst)
            teacherinst = Teachers.objects.get(name=request.session["teacher"])
            reservations = Reservations.objects.all().filter(teacher=teacherinst)
            return render(request, "add.html", {"booked":False, "available": timechecker(reservations), "students": bookingcheck(teacherinst)})

        except:
            try:
                res = Reservations.objects.get(student=studentinst, time=time)
                teacherinst = Teachers.objects.get(name=request.session["teacher"])
                reservations = Reservations.objects.all().filter(teacher=teacherinst)
                return render(request, "add.html", {"busy":True, "available": timechecker(reservations), "students": bookingcheck(teacherinst)})

            except:
                Reservations.objects.create(student=studentinst, teacher=teacherinst, time=time)
                teacherinst = Teachers.objects.get(name=request.session["teacher"])
                reservations = Reservations.objects.all().filter(teacher=teacherinst)
                return render(request, "add.html", {"booked":True, "available": timechecker(reservations), "students": bookingcheck(teacherinst)})

    if not request.session["teacher"]:
        return redirect("/")

    teacherinst = Teachers.objects.get(name=request.session["teacher"])

    reservations = Reservations.objects.all().filter(teacher=teacherinst)

    return render(
        request,
        "add.html",
        {"available": timechecker(reservations), "students": bookingcheck(teacherinst)},
    )


def addStudent(request):
    if request.method == "POST":

        name = request.POST["name"]
        grade_sec = request.POST["class"]
        jssid = request.POST["jssid"]

        try:
            res = Students.objects.get(name=name, jssid=jssid)
            return render(request, "add-student.html", {"student_exists":True})

        except:
            Students.objects.create(name=name, grade_sec=grade_sec, jssid=jssid)
            return render(request, "add-student.html", {"student_added":True})

    if not request.session["teacher"]:
        return redirect("/teacher")

    return render(request, "add-student.html")


def delete(request):

    if request.method == "POST":
        student = request.POST["student"]

        studentinst = Students.objects.get(jssid=student)

        teacherinst = Teachers.objects.get(name=request.session["teacher"])

        Reservations.objects.get(student=studentinst, teacher=teacherinst).delete()

        return redirect("/teacher/")

    return redirect("/teacher/")

def student(request):

    if request.method == "POST":
        jssid = request.POST['jssid']

        try:
            studentinst = Students.objects.get(jssid=jssid)

        except:
            return render(request, "student.html", {"no_exist":True})

        reservations = Reservations.objects.all().filter(student=studentinst)

        time = []

        for i in reservations:
            time.append(str(i.time))

        return render(request, "student-reservations.html", {"reservations":reservations, "timings":time})


    return render(request, "student.html")

def logout(request):
    del request.session["teacher"]

    return redirect("/teacher")
