from django import forms
from tools_over.models import Rating


class ReviewForm(forms.ModelForm):
    comment=forms.CharField()
    score=forms.IntegerField()


    class Meta:
        model=Rating
        fields=('comment','score',)


#{% url 'Post_Review' tool.id %}