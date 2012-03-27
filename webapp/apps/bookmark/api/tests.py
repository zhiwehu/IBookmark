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

from django.contrib.auth.models import User
from django.test import TestCase
from models import Bookmark, BookmarkUrl

class BookmarkTestCase(TestCase):
    def test_bookmarks(self):
        # Test get without login
        response = self.client.get('/api/bookmarks/')
        self.assertEqual(response.status_code, 200)

        # Test create bookmark for user not login
        response = self.client.post('/api/bookmarks/', {})
        self.assertEqual(response.status_code, 302)

        # Create a user and login
        user = User.objects.create_user('admin', 'admin@admin.com', 'admin')
        user.save()
        self.client.login(username='admin', password='admin')

        # Test get again
        response = self.client.get('/api/bookmarks/')
        self.assertEqual(response.status_code, 200)

        # Test get not exist bookmark
        response = self.client.get('/api/bookmarks/1/')
        self.assertEqual(response.status_code, 404)

        # Create a good data
        url = u'http://www.baidu.com/'
        title = u'baidu'
        tags = u'abc, def'
        public = True
        bookmark_data = {
            'url': url,
            'title' : title,
            'tags': tags,
            'public': public
        }

        # Post the bookmark for create
        response = self.client.post('/api/bookmarks/', bookmark_data)
        self.assertEqual(response.status_code, 201)
        bookmark = Bookmark.objects.get(id=1)
        self.assertEqual(bookmark.owner, user)
        self.assertEqual(bookmark.url, url)
        self.assertEqual(bookmark.title, title)
        self.assertEqual(bookmark.public, public)
        self.assert_tags_equal(bookmark.tags.all(), ['abc', 'def'])

        bookmark_url = BookmarkUrl.objects.get(url=bookmark.url)
        self.assertEqual(bookmark_url.url, bookmark.url)
        self.assertEqual(bookmark_url.count, 1)

        # Test get exist bookmark
        response = self.client.get('/api/bookmarks/1/')
        self.assertEqual(response.status_code, 200)

        # Logout and get the bookmark, should 200(public=True)
        self.client.logout()
        response = self.client.get('/api/bookmarks/1/')
        self.assertEqual(response.status_code, 200)

        # Change the bookmark values
        url=u'http://www.google.com/'
        title=u'google'
        public=False
        tags=u'google, baidu'
        bookmark_data = {
            'url': url,
            'title' : title,
            'tags': tags,
            'public': public
        }


        # Put data not login
        response = self.client.put('/api/bookmarks/1/', bookmark_data)
        self.assertEqual(response.status_code, 302)

        self.client.login(username='admin', password='admin')
        # Put the bookmark for update
        response = self.client.put('/api/bookmarks/1/', bookmark_data)
        self.assertEqual(response.status_code, 200)
        bookmark = Bookmark.objects.get(id=1)
        self.assertEqual(bookmark.owner, user)
        self.assertEqual(bookmark.url, url)
        self.assertEqual(bookmark.title, title)
        self.assertEqual(bookmark.public, public)
        self.assert_tags_equal(bookmark.tags.all(), ['google', 'baidu'])

        bookmark_url = BookmarkUrl.objects.get(url=bookmark.url)
        self.assertEqual(bookmark_url.url, bookmark.url)
        self.assertEqual(bookmark_url.count, 1)

        # Put an not exist bookmark
        response = self.client.put('/api/bookmarks/2/', bookmark_data)
        self.assertEqual(response.status_code, 404)

        # Logout and get the bookmark, should 404(public=False)
        self.client.logout()
        response = self.client.get('/api/bookmarks/1/')
        self.assertEqual(response.status_code, 404)

        # Delete without login
        response = self.client.delete('/api/bookmarks/2/')
        self.assertEqual(response.status_code, 302)

        # Delete an not exist bookmark, should get NOT_FOUND
        self.client.login(username='admin', password='admin')
        response = self.client.delete('/api/bookmarks/2/')
        self.assertEqual(response.status_code, 404)

        # Delete an exist bookmark
        response = self.client.delete('/api/bookmarks/1/')
        self.assertEqual(response.status_code, 204)
        try:
            bookmark = Bookmark.objects.get(id=1)
        except Bookmark.DoesNotExist:
            pass

        # Create the bookmark again
        url = u'http://www.baidu.com/'
        title = u'baidu'
        tags = u'abc, def'
        public = False
        bookmark_data = {
            'url': url,
            'title' : title,
            'tags': tags,
            'public': public
        }

        # Post the bookmark for create
        response = self.client.post('/api/bookmarks/', bookmark_data)
        self.assertEqual(response.status_code, 201)
        self.client.logout()

        # Create another user and login
        user = User.objects.create_user('jeffrey', 'jeffrey@admin.com', 'jeffrey')
        user.save()
        self.client.login(username='jeffrey', password='jeffrey')

        # user jeffrey try to get a not public bookmark, should 404
        response = self.client.get('/api/bookmarks/1/')
        self.assertEqual(response.status_code, 404)

    def assert_tags_equal(self, qs, tags, sort=True, attr="name"):
        got = map(lambda tag: getattr(tag, attr), qs)
        if sort:
            got.sort()
            tags.sort()
        self.assertEqual(got, tags)