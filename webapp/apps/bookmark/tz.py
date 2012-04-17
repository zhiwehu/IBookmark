import sys
import urllib2
import BeautifulSoup
from datetime import tzinfo, timedelta

# A class building tzinfo objects for fixed-offset time zones.
# Note that FixedOffset(0, "UTC") is a different way to build a
# UTC tzinfo object.
class FixedOffset(tzinfo):
    ZERO = timedelta(0)
    """Fixed offset in minutes east from UTC."""

    def __init__(self, offset, name):
        self.__offset = timedelta(minutes = offset)
        self.__name = name

    def utcoffset(self):
        return self.__offset

    def tzname(self):
        return self.__name

    def dst(self, dt):
        return ZERO

def ip_to_tz(ip_address):
    geo = None
    timezone = None
    try:
        xml = BeautifulSoup.BeautifulSoup(urllib2.urlopen('http://66.114.171.187:10000/__ip2geo__?opt=65535&ip=' + ip_address))
        geo = xml.item
        offset = geo['tz']
        int_offset= int(float(offset))
        timezone = FixedOffset(int_offset * 60, "GMT %s" % int_offset)
    except Exception as e:
        pass

    return geo, timezone

if __name__ == "__main__":
    ip_address = sys.argv[1]
    geo, timezone = ip_to_tz(ip_address)
    if geo:
        print 'Country=%s, CountryCode=%s, City=%s' % (geo['country'], geo['countrycode'], geo['city'])
    if timezone:
        print 'TZ_Name=%s, UTC_Offset=%s' % (timezone.tzname(), timezone.utcoffset())
