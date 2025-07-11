from django.urls import path
from . import views
urlpatterns=[
    path('',views.home),
    path('userregistration/',views.userregistraion),
    path('shopregister/',views.shopregistraion),
    path('login/',views.loginall,name="login"),
    path('logout',views.logoutall,name="logout"),
    path('homepage',views.homepage,name="homepage"),
    path('about',views.about),
    path('forgotPassword',views.forgotPassword),
    path('resetPassword',views.resetPassword,name='resetPassword')
]