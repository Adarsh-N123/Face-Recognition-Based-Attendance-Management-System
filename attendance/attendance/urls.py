"""attendance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from attendance import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Index,name='login'),
    path('register',views.Register,name='register'),
    path('dashboard',views.Dashboard,name='dashboard'),
    path('attendance',views.Attendance,name='attendance'),
    path('timetable',views.Timetable,name='timetable'),
    path('logout',views.Logout,name='logout'),
    path('remove/<str:coursecode>',views.Remove,name='remove'),
    path('addtostudent/<str:coursecode>',views.Addtostudent,name='addtostudent'),
    path('take',views.Ok,name='take'),
    path('video_feed', views.video_feed, name='video_feed'),
    # path('ok', views.Ok, name='ok'),
    path('declare/<str:statement>',views.Declare,name='declare')
]
