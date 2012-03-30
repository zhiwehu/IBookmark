import os
from django import forms
from django.forms.forms import Form
from django.forms.models import ModelForm
from django.template.defaultfilters import filesizeformat
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
        fields = ('url', 'title', 'tags', 'public')
        exclude = ('owner', 'create_time', 'screen_shot', 'last_modified_time')

class FileForm(Form):
    file  = forms.FileField('Bookmark file', help_text=u'(Maximum file size of 1 MB)')

    def clean_file(self):
        data = self.cleaned_data["file"]
        if data:
            (root, ext) = os.path.splitext(data.name.lower())
            if ext not in ['.html']:
                raise forms.ValidationError(
                    _(u"%(ext)s is an invalid file extension. Authorized extensions are : %(valid_exts_list)s") %
                    { "ext" : ext, "valid_exts_list" : ", ".join(['.html']) })

            if data.size > 1*1024*1024:
                raise forms.ValidationError(
                    _(u"Your file is too big (%(size)s), the maximum allowed size is %(max_valid_size)s") %
                    { "size" : filesizeformat(data.size), "max_valid_size" : filesizeformat(1*1024*1024)} )
        return data