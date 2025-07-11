from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Message

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'description']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text'] 
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Write a message...', 'rows': 4}),
        }
