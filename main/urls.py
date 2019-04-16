from django.urls import path

from main.views.api import incomeApi
from main.views import index, authentication, user

urlpatterns = [
    path('', index.IndexView.as_view(), name='main'),
    path('auth/register/', authentication.RegisterView.as_view(),
         name='register'),
    path('auth/login/', authentication.LoginView.as_view(), name='login'),
    path('auth/logout/', authentication.LogoutView.as_view(), name='logout'),
    path('user/<int:id>/', index.UserpageView.as_view(), name='userpage'),


    path('api/create_income/<int:pk>', incomeApi.IncomeCreate.as_view(),
         name='create_income'),

    path('user/<int:pk>/edit', user.UserUpdateBioView.as_view(), name='edit_user')

]
