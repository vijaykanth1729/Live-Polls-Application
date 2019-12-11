from django.urls import path
from .views import home, list_polls, poll_detail, poll_vote,add_poll, \
    edit_poll, add_choice,edit_choice,delete_choice,delete_poll
app_name = 'polls'
urlpatterns = [
    path('', home, name='home'),
    path('list/',list_polls,name='list'),
    #path('list/your_polls/',your_polls,name='your_polls'),
    path('add/',add_poll,name='add'),
    path('edit/<int:poll_id>/',edit_poll,name='edit'),
    path('edit/<int:poll_id>/choice/add/',add_choice,name='add_choice'),
    path('edit/choice/<int:choice_id>/', edit_choice, name='edit_choice'),
    path('delete/choice/<int:choice_id>/',delete_choice,name='choice_confirm_delete'),
    path('delete/poll/<int:poll_id>/',delete_poll,name='poll_confirm_delete'),
    path('list/<int:poll_id>/', poll_detail, name='detail'),
    path('list/<int:poll_id>/vote/', poll_vote, name='vote'),

]