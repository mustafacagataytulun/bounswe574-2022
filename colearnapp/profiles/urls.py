from django.urls import path

from .views import edit, edit_success, view, add_friend, notifications, notif_read, remove_friend

app_name = 'profiles'

urlpatterns = [
    path('<int:id>', view, name='view'),
    path('edit', edit, name='edit'),
    path('saved', edit_success, name='edit_success'),
    path('add_friend/<int:id>', add_friend, name='add_friend'),
    path('notifications', notifications, name='notifications'),
    path('notif_read/<int:id>', notif_read, name='notif_read'),
    path('remove_friend/<int:id>', remove_friend, name='remove_friend'),

]
