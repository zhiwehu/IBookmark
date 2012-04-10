import uuid
from django.core.files.base import ContentFile

__author__ = 'zhiwehu'

import utils
from models import Bookmark, BookmarkUrl
from threading import Timer
#second
t = 300

def cronjob():
    def update_bk_image():
        bookmarks = Bookmark.objects.all()
        for bookmark in bookmarks:
            if bookmark.screen_shot:
                break
            url = bookmark.url
            image = utils.get_image_by_url(url)
            if image:
                image_file_name = str(uuid.uuid1()) + ".jpg"
                bookmark.screen_shot.save(image_file_name, ContentFile(image))
                bookmark.save()

    update_bk_image()
    Timer(t, cronjob).start()

cronjob()
