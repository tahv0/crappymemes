from django import forms
from crappymemes.models import Meme, Comment

class NewCrappyMemeForm(forms.ModelForm):
    # pic = forms.ImageField(label='Meme image',required=True,
    #                        error_messages={'invalid':"Image files only"},
    #                        widget=forms.FileInput)

    class Meta:
        model = Meme
        fields = ['pic', 'title']
        widgets = {
            'title': forms.TextInput({'class': 'form-control'}),
        }


class UpdateCrappyMemeForm(forms.Form):
    pic = forms.ImageField(
        label='Meme image',
        required=False,
        error_messages={'invalid':"Image files only"},
        widget=forms.FileInput)
    title = forms.CharField(max_length=128, required=True)

    def __init__(self, *args, instance=None, **kwargs):
        super(UpdateCrappyMemeForm, self).__init__(*args, **kwargs)
        if instance:
            self.fields['pic'].initial = instance.pic
            self.fields['title'].initial = instance.title


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']
