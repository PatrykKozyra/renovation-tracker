from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Purchases
    path('purchases/', views.purchases_list, name='purchases_list'),
    path('purchases/add/', views.purchase_add, name='purchase_add'),
    path('purchases/<int:pk>/edit/', views.purchase_edit, name='purchase_edit'),

    # Progress
    path('progress/', views.progress_list, name='progress_list'),
    path('progress/add/', views.progress_add, name='progress_add'),

    # Sessions
    path('sessions/', views.sessions_list, name='sessions_list'),
    path('sessions/add/', views.session_add, name='session_add'),

    # Electrical circuits
    path('circuits/add/', views.circuit_add, name='circuit_add'),
]
