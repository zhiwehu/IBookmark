import threading
import urllib2
import uuid
from django.core.files.base import ContentFile
import os
import BeautifulSoup
from webapp.apps.bookmark.models import Bookmark

def get_title_by_url(url):
    title = None
    try:
        html = BeautifulSoup.BeautifulSoup(urllib2.urlopen(url))
        title = html.title.string.strip()
    except:
        pass
    return title

def get_image_by_url(url):
    image = None
    fp = None
    try:
        #request = urllib2.Request('http://api.snapito.com/free/sc?url=' + url)
        request = urllib2.Request('http://api.snapito.com/web/1958c07f5c68ec902e8ae368b4691f3511c7a5bb/sc?url=' + url)
        opener = urllib2.build_opener(SmartRedirectHandler())
        fp = opener.open(request)
        image = fp.read()
    except Exception as error:
        pass
    finally:
        if fp:
            fp.close()

    return image

def get_tag(line):
    result = None
    ssZero = '<DT><H3'
    zzZero = line.find(ssZero)
    if zzZero != -1:
        lssZero = zzZero + len(ssZero)

        ssOne = '>'
        zzOne = line[lssZero:].find(ssOne)
        if zzOne != -1:
            lssOne = lssZero + zzOne + len(ssOne)

            ssTwo = '<'
            zzTwo = line[lssOne:].find(ssTwo)
            if zzTwo != -1:
                lssTwo = lssOne + zzTwo
                result = line[lssOne:lssTwo]
    return result

def get_bookmark(line):
    bookmark = None
    s = '<DT><A HREF=\"'
    ls = len(s)
    z = line.find(s)
    if z != -1:
        ls = z + len(s)

        sOne = '\"'
        z1 = line[ls:].find(sOne)
        if z1 != -1:
            lsOne = ls + z1
            url = line[ls:lsOne]
            if url.startswith('http'):
                bookmark = {'url':'', 'title':'', 'tags':''}
                bookmark['url']=url
                lsTwo = lsOne + len(sOne)
                sTwo = '>'
                z2 = line[lsTwo:].find(sTwo)
                if z2 != -1:
                    lsThree = lsTwo + z2 + len(sTwo)
                    sThree = '</A>'
                    z3 = line[lsThree:].find(sThree)
                    if z3 != -1:
                        lsFour = lsThree + z3
                        title = line[lsThree:lsFour]
                        if title != '':
                            bookmark['title']=title
                tag_key='TAGS"'
                tag_key_len = len(tag_key)
                tag_start_pos = line.find('TAGS="')
                if tag_start_pos != -1:
                    tag_end_pos = line[tag_start_pos:].find('">') + tag_start_pos
                    if tag_end_pos != -1:
                        tags = line[tag_start_pos + tag_key_len+1: tag_end_pos]
                        bookmark['tags'] = tags
    return bookmark

def parse_firefox_bookmark(file):
    bookmarks = []
    while 1:
        line=file.readline()
        if not line: break

        try:
            bk = get_bookmark(line)
            if bk:
                bookmarks.append(bk)
        except Exception, e:
            pass

    return bookmarks

#print parse_firefox_bookmark(open('bookmarks.html', 'r'))

class SmartRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_301(self, req, fp, code, msg, headers):
        result = urllib2.HTTPRedirectHandler.http_error_301(
            self, req, fp, code, msg, headers)
        result.status = code
        return result

    def http_error_302(self, req, fp, code, msg, headers):
        result = urllib2.HTTPRedirectHandler.http_error_302(
            self, req, fp, code, msg, headers)
        result.status = code
        return result

def update_bk_screen_shot(bookmark):
    image = get_image_by_url(bookmark.url)
    if image:
        image_file_name = str(uuid.uuid1()) + ".png"
        try:
            os.remove(bookmark.screen_shot.path)
        except:
            pass
        bookmark_id = bookmark.id
        # Retreve the bookmark again make sure the bookmark others data is correct
        try:
            bookmark = Bookmark.objects.get(id=bookmark_id)
            if bookmark:
                bookmark.screen_shot.save(image_file_name, ContentFile(image))
                bookmark.save()
        except:
            pass

class BookmarkThread(threading.Thread):
    def __init__(self, bookmark):
        self.bookmark = bookmark
        threading.Thread.__init__(self)

    def run(self):
        update_bk_screen_shot(self.bookmark)

def update_bk_screen_shot_async(bookmark):
    BookmarkThread(bookmark).start()