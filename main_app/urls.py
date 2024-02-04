from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.events_index, name='events_index'),
    path('events/<int:event_id>/', views.events_detail, name='events_detail'),
    path('events/create/', views.EventCreate.as_view(), name='events_create'),
    path('events/<int:event_id>/collide_create/', views.CollideCreate.as_view(), name='collide_create'),
    path('collides/<int:collide_id>/', views.collides_detail, name='collides_detail'),
    path('collides/<int:collide_id>/add_rsvp/', views.rsvp_create, name='add_rsvp'),
    path('users/', views.user_profile, name='user_profile'),
    path('accounts/signup/', views.signup, name='signup'),
]