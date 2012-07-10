#!/usr/bin/env python

import os

from twisted.internet import defer, reactor
from twisted.web import client


URLS = [
    """http://ngm.nationalgeographic.com/photo-contest/2009/img/wallpaper/1109wallpaper-%s_1600.jpg""",
    """http://ngm.nationalgeographic.com/photo-contest/2009/img/wallpaper/1102wallpaper-%s_1600.jpg""",
    """http://ngm.nationalgeographic.com/photo-contest/2009/img/wallpaper/1026wallpaper-%s_1600.jpg""",
    """http://ngm.nationalgeographic.com/photo-contest/2009/img/wallpaper/1019wallpaper-%s_1600.jpg""",
    """http://ngm.nationalgeographic.com/photo-contest/2009/img/wallpaper/1013wallpaper-%s_1600.jpg""",
    """http://ngm.nationalgeographic.com/photo-contest/2009/img/wallpaper/1005wallpaper-%s_1600.jpg""",
    """http://ngm.nationalgeographic.com/photo-contest/2009/img/wallpaper/0928wallpaper-%s_1600.jpg""",
    """http://ngm.nationalgeographic.com/photo-contest/2009/img/wallpaper/0921wallpaper-%s_1600.jpg""",
    """http://ngm.nationalgeographic.com/photo-contest/2009/img/wallpaper/0914wallpaper-%s_1600.jpg""",
    """http://ngm.nationalgeographic.com/photo-contest/2009/img/wallpaper/0907wallpaper-%s_1600.jpg""",
    """http://ngm.nationalgeographic.com/photo-contest/2009/img/wallpaper/0831wallpaper-%s_1600.jpg""",
    """http://ngm.nationalgeographic.com/photo-contest/2009/img/wallpaper/0824wallpaper-%s_1600.jpg""",
    """http://ngm.nationalgeographic.com/photo-contest/2009/img/wallpaper/0817wallpaper-%s_1600.jpg""",
]


def urlIter(urls):
    for url in urls:
        for x in xrange(1, 27):
            nurl = url % (x,)
            path = os.path.basename(nurl)
            yield nurl, path

iterator = urlIter(URLS)
# for url, path in iterator:
#     print url, path

def printError(failure):
    print "failed:", failure
    print "getting next image:"
    d = downloadImages()
    print "returning deferred"
    return d

def getNextImage(ignored):
    return downloadImages()

def downloadImages():
    try:
        url, path = iterator.next()
        print "downloading:", url
        d = client.downloadPage(url, path)
        d.addCallback(getNextImage)
        d.addErrback(printError)
        return d
    except StopIteration:
        print "done downloading all images!"
        reactor.stop()

reactor.callWhenRunning(downloadImages)
reactor.run()
