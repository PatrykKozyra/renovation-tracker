from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Properties
    path('properties/', views.property_list, name='property_list'),
    path('properties/add/', views.property_add, name='property_add'),
    path('properties/<int:pk>/edit/', views.property_edit, name='property_edit'),
    path('properties/<int:pk>/switch/', views.property_switch, name='property_switch'),

    # Rooms
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/add/', views.room_add, name='room_add'),
    path('rooms/<int:pk>/', views.room_detail, name='room_detail'),
    path('rooms/<int:pk>/edit/', views.room_edit, name='room_edit'),

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

    # Dropdown mapping management
    path('dropdown-mapping/', views.dropdown_mapping_list, name='dropdown_mapping_list'),
    path('dropdown-mapping/add/', views.dropdown_choice_add, name='dropdown_choice_add'),
    path('dropdown-mapping/<int:pk>/edit/', views.dropdown_choice_edit, name='dropdown_choice_edit'),
    path('dropdown-mapping/<int:pk>/delete/', views.dropdown_choice_delete, name='dropdown_choice_delete'),

    # Equipment management
    path('equipment/', views.equipment_list, name='equipment_list'),
    path('equipment/add/', views.equipment_add, name='equipment_add'),
    path('equipment/<int:pk>/', views.equipment_detail, name='equipment_detail'),
    path('equipment/<int:pk>/edit/', views.equipment_edit, name='equipment_edit'),
    path('equipment/<int:pk>/delete/', views.equipment_delete, name='equipment_delete'),
    path('equipment/<int:equipment_pk>/photo/add/', views.equipment_photo_add, name='equipment_photo_add'),
    path('equipment/photo/<int:pk>/delete/', views.equipment_photo_delete, name='equipment_photo_delete'),
    path('equipment/<int:equipment_pk>/assign/', views.equipment_assign, name='equipment_assign'),
    path('equipment/<int:equipment_pk>/unassign/', views.equipment_unassign, name='equipment_unassign'),

    # To-Do List
    path('todo/', views.todo_list, name='todo_list'),
    path('todo/task/add/', views.renovation_task_add, name='renovation_task_add'),
    path('todo/task/<int:pk>/edit/', views.renovation_task_edit, name='renovation_task_edit'),
    path('todo/task/<int:pk>/delete/', views.renovation_task_delete, name='renovation_task_delete'),
    path('todo/shopping/add/', views.shopping_item_add, name='shopping_item_add'),
    path('todo/shopping/<int:pk>/edit/', views.shopping_item_edit, name='shopping_item_edit'),
    path('todo/shopping/<int:pk>/delete/', views.shopping_item_delete, name='shopping_item_delete'),
]
