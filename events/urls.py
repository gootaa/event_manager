from django.conf.urls import url
from . import views

urlpatterns = [
	# Home View
	url(r'^$', views.HomeView.as_view(), name='home'),
	# List and Detail Views
	url(r'^events/$', views.event_list, name='event_list'),
	url(r'^events/(?P<event_slug>[-\w]+)/$',
		views.event_list,
		name='event_list_by_category'),
	url(r'^event/(?P<event_slug>[-\w]+)/$',
		views.event_detail,
		name='event_detail'),
	url(r'^my-events/$', views.my_events, name='my_events'),
	# Add, Edit, Delete Views
	url(r'^add-event/$', views.add_event, name='add_event'),
	url(r'^edit-event/(?P<event_slug>[-\w]+)/$',
		views.edit_event,
		name='edit_event'),
	url(r'^delete-event/(?P<event_slug>[-\w]+)/$',
		views.delete_event,
		name='delete_event'),
	# Search View
	url(r'^search/', views.search, name='search'),
]