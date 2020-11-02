import json

import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from student_management_app.EmailBackEnd import EmailBackEnd


def showDemoPage(request):
    return render(request, 'demo.html')


def showLoginPage(request):
    return render(request, 'login_page.html')


def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        captcha_token = request.POST.get("g-recaptcha-response")
        cap_url = "https://www.google.com/recaptcha/api/siteverify"
        cap_secret = "6Legqs4ZAAAAAI8rkKMolHzxiMd4Gcajq_gJzv0e"
        cap_data = {"secret": cap_secret, "response": captcha_token}
        cap_server_response = requests.post(url=cap_url, data=cap_data)
        cap_json = json.loads(cap_server_response.text)

        if cap_json['success'] == False:
            messages.error(request, "Invalid Captcha Try Again")
            return HttpResponseRedirect("/")
        user = EmailBackEnd.authenticate(request, username=request.POST.get("email"), password=request.POST.get("password"))

        if user is not None:
            login(request, user)
            if user.user_type == "1":
                return HttpResponseRedirect("/admin_home")
            elif user.user_type == "2":
                return HttpResponseRedirect(reverse("staff_home"))
            else:
                return HttpResponseRedirect(reverse("student_home"))
        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect("/")


def getUserDetails(request):
    if request.user is not None:
        return "User : " + request.user.email + " usertype : " + str(request.user.user_type)
    else:
        return HttpResponse("Please Login First")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")


def showFirebaseJS(request):
    data = 'importScripts("https://www.gstatic.com/firebasejs/7.20.-/firebase-app.js");' \
           'importScripts("https://www.gstatic.com/firebasejs/7.20.-/firebase-messaging.js");' \
           'var firebaseConfig = {' \
           '    apiKey: "AIzaSyDHsJoKwJPfMj0J1Q5rsgLXH3J7PqVFQIc",' \
           '    authDomain: "studentmanagementsystem-151db.firebaseapp.com",' \
           '    databaseURL: "https://studentmanagementsystem-151db.firebaseio.com",' \
           '    projectId: "studentmanagementsystem-151db",' \
           '    storageBucket: "studentmanagementsystem-151db.appspot.com",' \
           '    messagingSenderId: "244420994811",' \
           '    appId: "1:244420994811:web:afffc17ee9ed67d96ff25e",' \
           '    measurementId: "G-8HNRCKCZ64"' \
           '};' \
           'firebase.initializeApp(firebaseConfig);' \
           'const messaging=firebase.messaging();' \
           'messaging.setBackgroundMessageHandler(function (payload) {' \
           '    console.log(payload)' \
           'const notification=JSON.parse(payload);' \
           'const notificationOption={' \
           'body:notification.body,' \
           'icon:notification.icon' \
           '}' \
           'return self.registration.showNotification(payload.notification.title,notificationOption);' \
           '});'

    return HttpResponse(data, content_type="text/javascript")