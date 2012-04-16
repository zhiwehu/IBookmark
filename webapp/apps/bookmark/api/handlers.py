"""
HTTP CODE
Variable	        Result	                            Description
rc.ALL_OK	        200 OK	                            Everything went well.
rc.CREATED	        201 Created	                        Object was created.
rc.DELETED	        204 (Empty body, as per RFC2616)	Object was deleted.
rc.BAD_REQUEST	    400 Bad Request	                    Request was malformed/not understood.
rc.FORBIDDEN	    401 Forbidden	                    Permission denied.
rc.NOT_FOUND	    404 Not Found	                    Resource not found.
rc.DUPLICATE_ENTRY	409 Conflict/Duplicate	            Object already exists.
rc.NOT_HERE	        410 Gone	                        Object does not exist.
rc.NOT_IMPLEMENTED	501 Not Implemented	                Action not available.
rc.THROTTLED	    503 Throttled	                    Request was throttled.
"""
from piston.utils import rc, validate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from piston.handler import AnonymousBaseHandler, BaseHandler
from django.db.models.query_utils import Q
from taggit.models import Tag
from bookmark.forms import BookmarkForm
from bookmark.models import Bookmark
from bookmark import utils

def get_data(bookmarks, request):
    # Get tag
    try:
        tag_id = int(request.GET.get('tag', 0))
    except:
        tag_id = 0

    if tag_id > 0:
        try:
            tag = Tag.objects.get(pk=tag_id)
            bookmarks = bookmarks.filter(tags__name__in=[tag.name])
        except ObjectDoesNotExist:
            # The tag does not exist, return none
            bookmarks = bookmarks.none()

    # Get owner
    try:
        owner_id = int(request.GET.get('owner_id', 0))
    except:
        owner_id = 0
    if owner_id > 0:
        try:
            owner = User.objects.get(id=owner_id)
            bookmarks = bookmarks.filter(owner=owner)
        except ObjectDoesNotExist:
            # The tag does not exist, return none
            bookmarks = bookmarks.none()

    keyword = request.GET.get('keyword', '')
    if keyword:
        bookmarks = bookmarks.filter(Q(title__contains=keyword) | Q(url__contains=keyword))

    # Get total records.
    total_count = bookmarks.count()

    # Get items_per_page
    items_per_page = int(request.GET.get('items_per_page', 10))
    if items_per_page not in [1, 10, 30, 50]:
        items_per_page = 10

    # Get current_page
    current_page = int(request.GET.get('current_page', 1))
    if current_page <= 0:
        current_page = 1
    page_number = total_count / items_per_page + 1
    if current_page > page_number:
        current_page = page_number
    bookmarks = bookmarks[(current_page - 1) * items_per_page: current_page * items_per_page]
    data = {'data': bookmarks, 'total_count': total_count, 'current_page': current_page,
            'items_per_page': items_per_page}
    return data

class MyBookmarkHandler(BaseHandler):
    model = Bookmark
    fields = ('id',
              ('owner', ('id', 'username',)),
              'title',
              'screen_shot',
              'url',
              ('tags', ('id', 'name',)),
              'public',
              'screen_shot',
              'create_time',
              'last_modified_time',
        )

    def read(self, request):
        bookmarks = Bookmark.objects.filter(owner = request.user)
        return get_data(bookmarks, request)

class BookmarkHandler(BaseHandler):
    model = Bookmark
    anonymous = 'AnonymousBookmarkHandler'
    fields = ('id',
              ('owner', ('id', 'username',)),
              'title',
              'url',
              ('tags', ('id', 'name',)),
              'public',
              'screen_shot',
              'create_time',
              'last_modified_time',
        )

    def read(self, request, bookmark_id=None):
        """
        Return a bookmark if 'bookmark_id' is given,
        otherwise a subset.
        """
        # bookmarks = all public + owner
        bookmarks = Bookmark.objects.filter(Q(public = True) | Q(owner = request.user))

        if bookmark_id:
            try:
                return bookmarks.get(pk=bookmark_id)
            except ObjectDoesNotExist:
                return rc.NOT_FOUND
        else:
            return get_data(bookmarks, request)

    @validate(BookmarkForm)
    def create(self, request):
        """
        Creates a new bookmark.
        """
        form = request.form
        bookmark = form.save(commit=False)
        bookmark.owner = request.user
        if not bookmark.title:
            bookmark.title = utils.get_title_by_url(bookmark.url)
        bookmark.save()
        form.save_m2m()

        utils.update_bk_screen_shot_async(bookmark)

        return bookmark

    @validate(BookmarkForm)
    def update(self, request, bookmark_id):
        # Get bookmark first, if not return NOT_FOUND
        try:
            bookmark = Bookmark.objects.get(pk = int(bookmark_id), owner=request.user)
            oldUrl = bookmark.url
            form = BookmarkForm(request.PUT, instance=bookmark)
            bookmark = form.save()

            if not bookmark.title:
                bookmark.title = utils.get_title_by_url(bookmark.url)
                bookmark.save()

            # update screen shot
            if oldUrl != bookmark.url:
                utils.update_bk_screen_shot_async(bookmark)

            return bookmark
        except ObjectDoesNotExist:
            return rc.NOT_FOUND

    def delete(self, request, bookmark_id):
        try:
            bookmark = Bookmark.objects.get(pk = int(bookmark_id), owner=request.user)
            bookmark.delete()
            return rc.DELETED
        except ObjectDoesNotExist:
            return rc.NOT_FOUND

class AnonymousBookmarkHandler(BookmarkHandler, AnonymousBaseHandler):
    """
    Anonymous entrypoint for bookmarks.
    """
    def read(self, request, bookmark_id=None):
        """
        Return a bookmark if 'bookmark_id' is given,
        otherwise a subset.
        """
        bookmarks = Bookmark.objects.filter(public=True)

        if bookmark_id:
            try:
                return bookmarks.get(pk=bookmark_id)
            except ObjectDoesNotExist:
                return rc.NOT_FOUND
        else:
            return get_data(bookmarks, request)