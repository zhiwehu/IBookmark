from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from forms import BookmarkForm
from taggit.utils import parse_tags
from webapp.apps.bookmark.forms import FileForm
from webapp.apps.bookmark.models import BookmarkCsvModel, Bookmark

def bookmark(request, template_name='bookmark/bookmark.html'):
    form = BookmarkForm()
    return render_to_response(template_name, RequestContext(request, {
        'active': 'bookmarks',
        }))

@login_required()
def my_bookmark(request, template_name='bookmark/my_bookmark.html'):
    form = BookmarkForm()
    file_form = FileForm()
    return render_to_response(template_name, RequestContext(request, {
        'form': form,
        'file_form': file_form,
        'active': 'my_bookmarks'
        }))

@login_required()
def delete_all_bookmarks(request):
    bookmarks = Bookmark.objects.filter(owner=request.user).delete()
    return HttpResponseRedirect(reverse('my_bookmark'))

@login_required()
def import_bookmarks(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            bookmarks = BookmarkCsvModel.import_data(data=file)
            for bk in bookmarks:
                bookmark = Bookmark.objects.create(url=bk.url, title=bk.title, owner=request.user)
                tags=parse_tags(bk.tags)
                for tag in tags:
                    bookmark.tags.add(tag)


            return HttpResponseRedirect(reverse('my_bookmark'))
    return HttpResponseRedirect(reverse('my_bookmark'))