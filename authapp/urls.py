from django.urls import path
from authapp import views
urlpatterns=[
            path('register/',views.RegisterAPI.as_view()),
    path('login/',views.LoginAPI.as_view()),
    path('userdata/',views.userview.as_view()),
    path('logout/',views.Logout.as_view())
]
