from django import forms
from models import Person



class PersonForm(forms.ModelForm):
	class Meta:
		model = Person 
		exclude = ["person_id"]
