#!/usr/bin/env python
import os

from twisted.internet import defer, reactor, task
from twisted.python import log
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


def generateDownloadArgs(urls):
    for url in urls:
        for x in xrange(1, 27):
            nurl = url % (x,)
            path = os.path.basename(nurl)
            yield nurl, path

            
def parallel(iterable, count, callable, *args, **named):
    coop = task.Cooperator()
    work = (callable(elem, *args, **named) for elem in iterable)
    return defer.DeferredList([coop.coiterate(work) for i in xrange(count)])


def handleError(x):
    """Any error reporting or error handling we want to do"""


def handleSuccess(x):
    """Anything extra we want to do on a successful download"""


def download((url, fileName)):
    d = client.downloadPage(url, fileName)
    d.addCallback(handleSuccess)
    d.addErrback(handleError)
    return d


if __name__=="__main__":
    finished = parallel(generateDownloadArgs(URLS), 10, download)
    finished.addErrback(handleError)
    finished.addCallback(lambda ignore: reactor.stop())
    reactor.run()
