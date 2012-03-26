from django import forms
from django.forms.models import ModelForm
from django.utils.translation import gettext_lazy as _
from models import Bookmark

class BookmarkForm(ModelForm):
    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if len(tags) > 3:
            raise forms.ValidationError(_(u'You can not add tags more the 3'))

        tags = [x.lower() for x in tags]
        return tags

    class Meta:
        model = Bookmark
        fields = ('title', 'url', 'tags', 'public')
        exclude = ('owner', 'create_time', 'favorite_users', 'screenshot')