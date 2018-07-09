from django import forms

from .models import Event


class EventForm(forms.ModelForm):

	class Meta:
		model = Event
		exclude = ('host', 'slug',)


class EventDeleteForm(forms.Form):
	title = forms.CharField(max_length=250)
	password = forms.CharField(widget=forms.PasswordInput)


class SearchForm(forms.Form):
	q = forms.CharField()