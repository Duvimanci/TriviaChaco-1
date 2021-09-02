"""Info URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from . import views as v

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', v.index, name='index'),
    path('login/', v.login, name='login'),
    path('logout/', v.user_logout, name='logout'),
    path('game/', v.game, name='game'),
    path('lobby/', v.lobby, name='lobby'),
    path('register/', v.register, name='register'),
    path('us/', v.us, name='us'),
    path('game/', v.game, name='game'),
    path('ranking/', v.ranking, name='ranking'),
    path('<int:partida_id>/', v.historial, name='historial'),
    path('data/', v.data, name='data')
    
    #---------------------------------------------
    #posts de formularios
    #registro
]

