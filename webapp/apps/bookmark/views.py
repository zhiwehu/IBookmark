import json
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models.aggregates import Count
from django.forms.forms import NON_FIELD_ERRORS
from django.forms.util import ErrorList
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from forms import BookmarkForm, FileForm
from taggit.models import Tag
from taggit.utils import parse_tags
from models import Bookmark
from utils import parse_firefox_bookmark

def bookmark(request, template_name='bookmark/bookmark.html'):
    form = BookmarkForm()
    return render_to_response(template_name, RequestContext(request, {
        'active': 'bookmark',
        }))

@login_required()
def my_bookmark(request, template_name='bookmark/my_bookmark.html'):
    form = BookmarkForm()
    file_form = FileForm()
    return render_to_response(template_name, RequestContext(request, {
        'form': form,
        'file_form': file_form,
        'active': 'my_bookmark'
        }))

@login_required()
def delete_all_bookmarks(request):
    bookmarks = Bookmark.objects.filter(owner=request.user).delete()
    return HttpResponseRedirect(reverse('my_bookmark'))

'''
@login_required()
def import_bookmark(request, template_name='bookmark/import_bookmark.html'):
    file_form = FileForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and file_form.is_valid():
        file = request.FILES['file']
        try:
            bookmarks = BookmarkCsvModel.import_data(data=file)
            for bk in bookmarks:
                bookmark = Bookmark.objects.create(url=bk.url, title=bk.title, owner=request.user)
                tags=parse_tags(bk.tags)
                for tag in tags:
                    bookmark.tags.add(tag)
            return HttpResponseRedirect(reverse("my_bookmark"))
        except Exception, e:
            file_form._errors[NON_FIELD_ERRORS] = ErrorList([e.message])

    return render_to_response(template_name, RequestContext(request, {
        'file_form': file_form,
        'active': 'my_bookmark'
    }))
'''

@login_required()
def import_firefox_bookmark(request, template_name='bookmark/import_bookmark.html'):
    file_form = FileForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and file_form.is_valid():
        file = request.FILES['file']
        try:
            bookmarks = parse_firefox_bookmark(file)
            for bk in bookmarks:
                bookmark = Bookmark.objects.create(url=bk['url'], title=bk['title'], owner=request.user)
                tags=parse_tags(bk['tags'])
                for tag in tags:
                    bookmark.tags.add(tag)
            return HttpResponseRedirect(reverse("my_bookmark"))
        except Exception, e:
            file_form._errors[NON_FIELD_ERRORS] = ErrorList([e.message])

    return render_to_response(template_name, RequestContext(request, {
        'file_form': file_form,
        'active': 'my_bookmark'
    }))

@login_required()
def my_tag(request):
    tags = Tag.objects.filter(bookmark__owner=request.user)\
    .annotate(bookmark_count=Count('bookmark'))\
    .order_by('-bookmark_count')
    total_count=tags.count()
    tags_data=[]
    for tag in tags:
        tags_data.append({'id': tag.id, 'name': tag.name, 'bookmark_count': tag.bookmark_count})
    data = {'data': tags_data, 'total_count': total_count}
    return HttpResponse(json.dumps(data), mimetype="application/json")

def tag(request):
    tags = Tag.objects.filter(bookmark__public=True)\
    .annotate(bookmark_count=Count('bookmark'))\
    .order_by('-bookmark_count')[0:10]

    total_count=tags.count()
    tags_data=[]
    for tag in tags:
        tags_data.append({'id': tag.id, 'name': tag.name, 'bookmark_count': tag.bookmark_count})
    data = {'data': tags_data, 'total_count': total_count}
    return HttpResponse(json.dumps(data), mimetype="application/json")