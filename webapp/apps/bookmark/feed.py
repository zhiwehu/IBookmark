from django.contrib.syndication.views import Feed
from django.utils.translation import ugettext_lazy as _
from models import Bookmark

class BookmarkFeed(Feed):
    title = _(u"Latest public bookmarks")
    link = "/sitenews/"
    description = _(u"The latest 10 public bookmarks")

    def items(self):
        return Bookmark.objects.filter(public=True).order_by('-create_time')[:10]

    def item_description(self, item):
        tags = ', '.join([tag.name for tag in item.tags.all()])
        return "%s (Taged by %s)" %(item.title, tags)