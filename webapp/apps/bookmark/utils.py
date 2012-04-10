import urllib

def get_image_by_url(url):
    image = None
    fp = None
    try:
        fp = urllib.URLopener().open('http://api.snapito.com/free/sc?url=' + url)
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

