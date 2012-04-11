import utils
from models import Bookmark, BookmarkUrl
from threading import Timer

#second
t = 7200

def cronjob():
    def update_bk_image():
        bookmarks = Bookmark.objects.all()
        for bookmark in bookmarks:
            if bookmark.screen_shot:
                break
            utils.update_bk_screen_shot_async(bookmark)

    update_bk_image()
    Timer(t, cronjob).start()

cronjob()
