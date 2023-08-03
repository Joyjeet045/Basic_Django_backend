from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.registerPage,name='register'),
    path('logout/',views.logoutPage,name='logout'),
    path('login/',views.LoginPage,name='login'),
    path('', views.home, name="home"),
    path('room/<str:pk>/',views.room,name='room'),
    path('profile/<str:pk>/',views.userProfile,name='user-profile'),
    path('create-room/',views.CreateRoom,name="create-room"),
    path('update-room/<str:pk>',views.UpdateRoom,name="update-room"),
    path('delete-room/<str:pk>',views.DeleteRoom,name="delete-room"),
    path('delete-message/<str:pk>',views.deleteMessage,name="delete-message")
]
