from csvImporter.fields import CharField
from csvImporter.model import CsvModel
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch.dispatcher import receiver
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager

class Bookmark(models.Model):
    owner = models.ForeignKey(User, verbose_name=_(u'Owner'), related_name='owner_bookmarks')
    url = models.URLField(verbose_name=_(u'URL'))
    title = models.CharField(verbose_name=_(u'Title'), blank=True, max_length=100,
        help_text=_(u'Limit of 100 characters'))
    tags = TaggableManager(verbose_name=_(u'Tags'), blank=True,
        help_text=_(u'A comma-separated list of tags. At most 3.'))
    public = models.BooleanField(verbose_name=_(u'Public this bookmark'), blank=True, default=True)
    screen_shot = models.ImageField(verbose_name=_(u'Screen shot'), upload_to='bookmark', blank=True)
    create_time = models.DateTimeField(verbose_name=_(u'Create time'), auto_now_add=True)
    last_modified_time = models.DateTimeField(verbose_name=_(u'Last modified time'), auto_now=True)

    def __unicode__(self):
        return self.url

    class Meta:
        ordering = ['-create_time']

class BookmarkCsvModel(CsvModel):
    url = CharField()
    title = CharField()
    tags = CharField()
    class Meta:
        has_header = False
        silent_failure = True
        delimiter = ";"


class BookmarkUrl(models.Model):
    url = models.URLField(verbose_name=_(u'URL'), unique=True)
    count = models.IntegerField(verbose_name=_(u'Count'), default=0)
    create_time = models.DateTimeField(verbose_name=_(u'Create time'), auto_now_add=True)
    last_modified_time = models.DateTimeField(verbose_name=_(u'Last modified time'), auto_now=True)

    def __unicode__(self):
        return self.url

    class Meta:
        ordering = ['-create_time']

@receiver(post_save, sender=Bookmark)
@receiver(post_delete, sender=Bookmark)
def create_bookmark_url(sender, instance=None, **kwargs):
    if instance is None:
        return
    bookmark_url, created = BookmarkUrl.objects.get_or_create(url=instance.url)
    count = Bookmark.objects.filter(url=instance.url).count()
    bookmark_url.count = count
    bookmark_url.save()