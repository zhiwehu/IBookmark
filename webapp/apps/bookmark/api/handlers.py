from piston.handler import BaseHandler, AnonymousBaseHandler
from urlparse import urlparse
from bookmark.models import Bookmark
from django.core.exceptions import ObjectDoesNotExist
from piston.utils import rc, validate
from django.db.models.aggregates import Count
from bookmark.forms import BookmarkForm
from django.utils.http import urlquote
from taggit.models import Tag
from webapp import settings

class BookmarkHandler(BaseHandler):
    model = Bookmark
    anonymous = 'AnonymousBookmarkHandler'
    fields = ('id',
              ('owner', ('id', 'username',)),
              ('favorite_users', ('id',)),
              'num_favorite_users',
              'title',
              'url',
              ('tags', ('name',)),
              'screenshot',
              'create_time',
        )

    def read(self, request, bookmark_id=None):
        """
        Return a bookmark if 'bookmark_id' is given,
        otherwise a subset.
        """

        bookmarks = Bookmark.objects

        if bookmark_id:
            try:
                return bookmarks.get(pk=bookmark_id)
            except ObjectDoesNotExist:
                return rc.NOT_FOUND

        else:
            # Get mine data or all data
            mine = request.GET.get('mine')
            if mine:
                bookmarks = bookmarks.filter(owner = request.user).annotate(num_favorite_users=Count('favorite_users'))
            else:
                bookmarks = bookmarks.filter(public = True).annotate(num_favorite_users=Count('favorite_users'))

            # Get tag
            tag_name = request.GET.get('tag')
            if tag_name:
                tag = Tag.objects.get(name=tag_name)
                bookmarks = bookmarks.filter(tags__name__in=[tag.name])

            # Get total records.
            total = bookmarks.count()

            # Get order by, and save into session or get from session
            order_by = request.GET.get('order_by')
            if order_by:
                request.session['order_by'] = order_by
            else:
                order_by = request.session.get('order_by', 'newest')
            if order_by not in ['newest', 'hottest']:
                order_by = 'newest'
            if order_by == 'newest':
                order_by = '-create_time'
            else:
                order_by = '-num_favorite_users'
            bookmarks = bookmarks.order_by(order_by)

            # Get items_per_page
            items_per_page = int(request.GET.get('items_per_page', 10))
            if items_per_page not in [1, 10, 30, 50]:
                items_per_page = 10

            # Get current_page
            current_page = int(request.GET.get('current_page', 1))
            if current_page <= 0:
                current_page = 1
            page_number = total/items_per_page + 1
            if current_page > page_number:
                current_page = page_number

            bookmarks = bookmarks[(current_page - 1) * items_per_page : current_page * items_per_page]

            data = {}
            data['data'] =  bookmarks
            data['total']  = total
            data['current_page'] = current_page
            data['items_per_page'] = items_per_page
            return data

    @validate(BookmarkForm)
    def create(self, request):
        """
        Creates a new bookmark.
        """
        form = request.form

        bookmark = form.save(commit=False)
        bookmark.owner = request.user
        bookmark.save()
        form.save_m2m()
        return bookmark

    def update(self, request, bookmark_id):
        #TODO not finished
        bookmark = Bookmark.objects.get(pk = bookmark_id)
        if not bookmark:
            return rc.NOT_FOUND

        # Update favorite_users
        # TODO check the request.user in bookmark.favorite_users
        if request.PUT.get('update_favorite_users'):
            bookmark.favorite_users.add(request.user)
            bookmark.save()
            return {'num_favorite_users' : bookmark.favorite_users.count()}

        return bookmark

    def delete(self, request, bookmark_id):
        bookmark = Bookmark.objects.get(pk = int(bookmark_id))

        if not request.user == bookmark.owner:
            return rc.FORBIDDEN # returns HTTP 401

        bookmark.delete()
        return rc.DELETED # returns HTTP 204

class AnonymousBookmarkHandler(BookmarkHandler, AnonymousBaseHandler):
    """
    Anonymous entrypoint for blogposts.
    """
    def read(self, request, bookmark_id=None):
        """
        Return a bookmark if 'bookmark_id' is given,
        otherwise a subset.
        """
        bookmarks = Bookmark.objects

        if bookmark_id:
            try:
                return bookmarks.get(pk=bookmark_id)
            except ObjectDoesNotExist:
                return rc.NOT_FOUND

        else:
            # Get mine data or all data
            mine = request.GET.get('mine')
            if mine:
                relative_url = urlparse(request.META.get('HTTP_REFERER', '/')).path
                path = urlquote(relative_url)
                tup = settings.LOGIN_URL, 'next', path
                json = {'redirect': '%s?%s=%s' % tup}
                return json

            bookmarks = bookmarks.filter(public = True).annotate(num_favorite_users=Count('favorite_users'))

            # Get tag
            tag_name = request.GET.get('tag')
            if tag_name:
                tag = Tag.objects.get(name=tag_name)
                bookmarks = bookmarks.filter(tags__name__in=[tag.name])

            # Get total records.
            total = bookmarks.count()

            # Get order by, and save into session or get from session
            order_by = request.GET.get('order_by')
            if order_by:
                request.session['order_by'] = order_by
            else:
                order_by = request.session.get('order_by', 'newest')
            if order_by not in ['newest', 'hottest']:
                order_by = 'newest'
            if order_by == 'newest':
                order_by = '-create_time'
            else:
                order_by = '-num_favorite_users'
            bookmarks = bookmarks.order_by(order_by)

            # Get items_per_page
            items_per_page = int(request.GET.get('items_per_page', 10))
            if items_per_page not in [1, 10, 30, 50]:
                items_per_page = 10

            # Get current_page
            current_page = int(request.GET.get('current_page', 1))
            if current_page <= 0:
                current_page = 1
            page_number = total/items_per_page + 1
            if current_page > page_number:
                current_page = page_number

            bookmarks = bookmarks[(current_page - 1) * items_per_page : current_page * items_per_page]

            data = {}
            data['data'] =  bookmarks
            data['total']  = total
            data['current_page'] = current_page
            data['items_per_page'] = items_per_page
            return data