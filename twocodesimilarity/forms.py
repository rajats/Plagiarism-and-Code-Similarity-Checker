from django import forms

class CodeForm(forms.Form):
	code1 = forms.CharField(widget=forms.Textarea)
	code2 = forms.CharField(widget=forms.Textarea)