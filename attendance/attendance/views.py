from django.http import HttpResponse
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.http import JsonResponse
from .models import *
import datetime
import os
import cv2
import cv2,os,urllib.request
import numpy as np
from django.http.response import StreamingHttpResponse
from django.conf import settings
import json
from deepface import DeepFace
from django.http import StreamingHttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import HttpRequest
def Index(request):
    err = ""
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username,password = password)
        try:
            if user.is_staff:
                login(request,user)
                err = "no"
            else:
                login(request,user)
                err = "no"
        except:
            err = "yes"
    data = {'error':err}
    return render(request,'index.html',data)

def Register(request):
    er = 'yes'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username is already taken'})
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email is already taken'})
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        er = 'no'
    #     u = username
    #     p = password
    #     user = authenticate(username=u, password=p)
    #     try:
    #         if user.is_staff:
    #             login(request,user)
    #             error = "no"
    #         else:
    #             login(request,user)
    #             error = "no"
    #     except:
    #         error = "yes"
    d = {'er': er}
    return render(request, 'register.html',d)

def Dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    obj = Course.objects.all()
    L=[]
    for i in obj:
        if '/'+i.coursecode+'/' in request.user.first_name:
            L.append(i)

    data = {'data':obj,'data1':L}
    return render(request,'dashboard.html',data)
def Attendance(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.is_staff:
        if request.method == 'POST':
            date = request.POST['date']
            rollno = request.POST['rollno']
            code = request.POST['code']
            if date=='':
                try:
                    u = Attendancemodel.objects.filter(username=rollno,coursecode=code)
                    return render(request,'attendance.html',{'maindata':u})
                except Attendancemodel.DoesNotExist:
                    return render(request,'attendance.html',{'maindata':[]})

            else:
                try:
                    u = Attendancemodel.objects.filter(username=rollno,date=date,coursecode=code)
                    return render(request,'attendance.html',{'maindata':u})
                except Attendancemodel.DoesNotExist:
                    return render(request,'attendance.html',{'maindata':[]})
        u = Attendancemodel.objects.all()
        return render(request,'attendance.html',{'maindata':u})
    else:
        if request.method == 'POST':
            date = request.POST['date']
            rollno = request.user.username
            code = request.POST['code']
            if date=='':
                try:
                    u = Attendancemodel.objects.filter(username=rollno,coursecode=code)
                    return render(request,'attendance.html',{'maindata':u})
                except Attendancemodel.DoesNotExist:
                    return render(request,'attendance.html',{'maindata':[]})

            else:
                try:
                    u = Attendancemodel.objects.filter(username=rollno,date=date,coursecode=code)
                    return render(request,'attendance.html',{'maindata':u})
                except Attendancemodel.DoesNotExist:
                    return render(request,'attendance.html',{'maindata':[]})
        u = Attendancemodel.objects.filter(username=request.user.username)
        return render(request,'attendance.html',{'maindata':u})

def Timetable(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.is_staff:
        error = 'yes'
        if request.method == 'POST':
            classes = request.POST['classes']
            instructorname = request.POST['instructorname']
            coursecode = request.POST['coursecode']
            slots = request.POST['slots']
            startdate = request.POST['startdate']
            enddate = request.POST['enddate']
            try:
                    try:
                        Course.objects.get(coursecode=coursecode)
                    except Course.DoesNotExist:
                        Course.objects.create(coursecode=coursecode,instructorname=instructorname,startdate=startdate,enddate=enddate,totalclasses=classes,slots=slots)
                        i = 0
                        temp = ''
                        L=[]
                        L1=[]
                        start = 0
                        end = 0
                        while (i<len(slots)):
                            if str(slots[i])=='&':
                                end = i-1
                                L.append(start)
                                L1.append(end)
                                start = i+1
                            i+=1
                        L.append(start)
                        L1.append(len(slots))
                        # print((start,end,L,L1))
                        for i in range(len(L)):
                            ini = L[i]
                            fin = L1[i]
                            # print((i,L[i],L1[i]))
                            temp1=''
                            temp = ''
                            j=0
                            cont = True
                            while (j<len(slots[ini:fin])):
                                if str(slots[ini:fin])[j]!='/' and cont==True:
                                    temp = temp+str(slots[ini:fin])[j]
                                    
                                elif str(slots[ini:fin])[j]!='-' and cont==False:
                                    temp1 = temp1+str(slots[ini:fin])[j]
                                elif str(slots[ini:fin])[j]=='/':
                                    cont = False
                                else:
                                    j=len(slots[ini:fin])+1
                                # print((temp,temp1,str(slots[ini:fin])))
                                j+=1
                            
                            u = Times.objects.get(codenumber=temp,codestime=temp1)
                            # print((u,u.codes,u.id))
                            if str(coursecode) not in str(u.codes):
                                # print(Times.objects.get(codenumber=temp,codestime=temp1).codes)
                                u = Times.objects.filter(codenumber=temp,codestime=temp1).update(codes = u.codes+'/'+str(coursecode)+str('/'))
                            
                            
                        error = "no"
            except:
                    error = "yes"
        d={'error':error}

        return render(request,'timetable.html',d)
    else:
        obj = Course.objects.all()
        u = User.objects.get(username = request.user.username).first_name
        return render(request,'timetable.html',{'data':obj,'userdata':u})


def Logout(request):
    if not request.user.is_authenticated:
        return redirect('login')
    logout(request)
    return redirect('login')
def Remove(request,coursecode):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.is_staff:
        course = Course.objects.get(coursecode=coursecode)
        course.delete()
        return redirect('dashboard')
    else:
        return redirect('dashboard')
    
def Addtostudent(request,coursecode):
    if not request.user.is_authenticated:
        return redirect('login')
    u = User.objects.get(username = request.user.username)
    if '/'+str(coursecode)+'/' not in u.first_name:
        u = User.objects.filter(username=request.user.username).update(first_name = u.first_name+'/'+str(coursecode)+str('/'))
    
    
    return redirect('dashboard')

def Take(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method=='POST':
        rollno = request.POST['rollno']
        if rollno=='':
            return render(request,'take.html',{})
        

        # Get current date and time
        now = datetime.datetime.now()

        # Format day of the week to lowercase and first three letters
        day_string = now.strftime("%A")[:3].lower()

        # Format time in 24-hour clock
        time_string = now.strftime("%H:%M:%S")

        # Format date in DD/MM/YYYY format
        date_string = now.strftime("%Y/%m/%d")
        time_string = (time_string[:2]+':'+'00')
        try:
            tem = Times.objects.get(codenumber=day_string,codestime=time_string)
            tem1 = tem.codes
            tem2 = User.objects.get(username=rollno).first_name
            print((tem1,tem2))
            i=0
            L=[]
            tem3 = ''
            while(i<len(tem1)):
                if tem1[i]!='/':
                    tem3 = tem3+tem1[i]
                else:
                    if tem3!='':
                        L.append(tem3)
                        tem3=''
                i+=1
            print(L)
            for j in L:
                if j in tem2:
                    for k in range(len(date_string)):
                        date_string = date_string.replace("/", "-")
                    try:
                        Attendancemodel.objects.get(username=rollno,date=date_string,time=time_string)
                        return render(request,'take.html',{'error':'alreadydone'})
                    except Attendancemodel.DoesNotExist:
                        Attendancemodel.objects.create(username=rollno,date=date_string,time=time_string,coursecode=j)
                        return render(request,'take.html',{'error':'data'})
            if L==[]:
                return render(request,'take.html',{'error':'nodata'})

        except Times.DoesNotExist:
            return render(request,'take.html',{'error':'nodata'})
        
        data = {}
        return render(request,'take.html',data)
    else:
        if request.user.is_staff:
            return render(request,'take.html')

        else:
            return redirect('dashboard')
        






face_detection_videocam = cv2.CascadeClassifier(os.path.join(
			settings.BASE_DIR,'opencv_haarcascade_data/haarcascade_frontalface_default.xml'))
face_detection_webcam = cv2.CascadeClassifier(os.path.join(
			settings.BASE_DIR,'opencv_haarcascade_data/haarcascade_frontalface_default.xml'))

def check_face(frame):
    folder_path = os.path.join(settings.BASE_DIR,'Database')
    for filename in os.listdir(folder_path):
        if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
            img_path = os.path.join(folder_path, filename)
            reference_img = cv2.imread(img_path)
            try:
                if DeepFace.verify(frame, reference_img.copy())['verified']:
                    return filename
            except ValueError:
                pass
    return ''

import cv2
global_filename=''

class VideoCamera:
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()

        # Check if the video was read successfully
        if not success:
            raise Exception("Failed to read video")

        # Convert image to grayscale for face detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        global global_filename
        # Detect faces in the image
        faces_detected = face_detection_videocam.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        filename=''
        # Loop over the detected faces
        for (x, y, w, h) in faces_detected:
            # Draw a rectangle around the face
            cv2.rectangle(image, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=2)

            # Check if the face matches a known face
            filename = check_face(image[y:y+h, x:x+w])
            global_filename = filename
            if filename!='':
                # Add the name of the person to the image
                cv2.putText(image, filename, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
                
                
                # return redirect('ok',global_filename=filename)

                # Redirect to a new page
            

        # Encode the image to JPEG format
        _, jpeg = cv2.imencode('.jpg', image)
        return (jpeg.tobytes(),filename)






# def gen(camera):
#     while True:
#         global global_filename
#         # Get the next video frame and filename
#         print(global_filename)
#         try:
#             frame, filename = camera.get_frame()
#         except ValueError:
#             print(global_filename)
#             print('successtwo')
#             return redirect('ok',global_filename=global_filename)
        
#         # Check if a filename was returned
#         # if filename!='':
#         #     global_filename=filename
#         #     print((filename,global_filename))
            
#             # break
#         # Yield the frame as a multipart response
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
#             # Redirect to a new page
#             # return HttpResponseRedirect('/ok')
#             # return redirect('ok', userone=filename)

def gen(camera):
    global global_filename
    match_found = False
    while True:
        # Get the next video frame and filename
        frame, filename = camera.get_frame()
        
        # Check if a filename was returned
        if filename!='':
            global_filename = filename
            match_found = True
            # request = HttpRequest()

            #     # Set the request method
            # request.method = 'GET'

            #     # Use the request object to perform some action
            # response = Ok(request)
            
        
        # Yield the frame as a multipart response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    
    # Redirect to the 'ok' view with the filename of the matched face
    

        
    



def video_feed(request):
    # global global_filename
    # print(global_filename)
    # if global_filename!='':
    #     return redirect('ok',global_filename=global_filename)
    
    return StreamingHttpResponse(gen(VideoCamera()),
                                    content_type='multipart/x-mixed-replace; boundary=frame')
    
        # return redirect('ok')

def Ok(request):
    global global_filename
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method=='POST':
        print('successone')
        userone = global_filename
        rollno=''
        if userone!='':
            for i in userone:
                if i!='.':
                    rollno+=i
                else:
                    break
        print(rollno)
        print('hello')
        if rollno=='':
            return render(request,'take.html',{})
        
        
            # Get current date and time
        now = datetime.datetime.now()
        print('helloz')
        # Format day of the week to lowercase and first three letters
        day_string = now.strftime("%A")[:3].lower()

            # Format time in 24-hour clock
        time_string = now.strftime("%H:%M:%S")

            # Format date in DD/MM/YYYY format
        date_string = now.strftime("%Y/%m/%d")
        time_string = (time_string[:2]+':'+'00')
        try:
            try:
                tem = Times.objects.get(codenumber=day_string,codestime=time_string)
            except Times.DoesNotExist:
                print('hello3')
                return render(request,'take.html',{'error':'nodata'})
            tem1 = tem.codes
            try:
                tem2 = User.objects.get(username=rollno).first_name
            except User.DoesNotExist:
                print('hello4')
                return render(request,'take.html',{'error':'nouser'})
            print((tem1,tem2))
            i=0
            L=[]
            tem3 = ''
            while(i<len(tem1)):
                if tem1[i]!='/':
                    tem3 = tem3+tem1[i]
                else:
                    if tem3!='':
                        L.append(tem3)
                        tem3=''
                i+=1
            print(L)
            for j in L:
                if j in tem2:
                    for k in range(len(date_string)):
                        date_string = date_string.replace("/", "-")
                    try:
                        Attendancemodel.objects.get(username=rollno,date=date_string,time=time_string)
                        global_filename=''
                        return render(request,'take.html',{'error':'alreadydone'})
                    except Attendancemodel.DoesNotExist:
                        Attendancemodel.objects.create(username=rollno,date=date_string,time=time_string,coursecode=j)
                        global_filename=''
        
                    return render(request,'take.html',{'error':'data'})
            if L==[]:
                global_filename=''
                print('predeclare')
                return render(request,'take.html',{'error':'nodata'})

        except Times.DoesNotExist:
            global_filename=''
            return render(request,'take.html',{'error':'nodata'})
            
    data = {}
        # print('hello2')
    global_filename=''
    return render(request,'take.html',data)
    

def Declare(request,statement):
    print('declared')
    return render(request,'take.html',{'error':statement})