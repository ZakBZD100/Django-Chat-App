from django.contrib import admin
from django.urls import path, include
from chat import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.accueil, name='accueil'),  
    path('connexion/', views.connexion, name='connexion'),
    path('inscription/', views.inscription, name='inscription'),
    path('salons/', views.liste_salons, name='liste_salons'),
    path('salon/<int:id>/', views.salon_details, name='salon_detail'),
    path('creer-salon/', views.creer_salon, name='creer_salon'),
    path('chat/', views.liste_salons, name='liste_salons'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),  
    path('salon/<int:salon_id>/messages/', views.get_messages, name='get_messages'), 
    path('salon/<int:id>/send_message/', views.send_message, name='send_message'), 
    path('chat/', include('chat.urls')), 
    
]
