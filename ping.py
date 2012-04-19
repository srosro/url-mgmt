import optparse
import json
import urllib2
import commands
import time
import os
import gntp.notifier

interval = 30 #interval in seconds
duration = 3 #duration of check in hours
threshold = 199.0 #alert threshold
n = 0

try:
    from local import COOKIE_STRING
except ImportError:
    COOKIE_STRING = ''
    
parser = optparse.OptionParser()
parser.add_option("-g", "--growl",
                  dest="growl", default=False,
                  action="store_true",
                  help="Enable Growl notifications. Must have 'growlnotify' installed")
parser.add_option("-i", "--interval",
                  dest="interval", default="600",
                  help="Update interval",
                  metavar="SECONDS")
parser.add_option("-d", "--duration",
                  dest="duration", default="24",
                  help="Duration to continue checking",
                  metavar="HOURS")
parser.add_option("-u", "--url",
                  dest="url", default="https://news.google.com/",
                  help="URL to check")
parser.add_option("-s", "--string",
                  dest="searchstring", default="unicorn",
                  help="The string to search for")

(options, args) = parser.parse_args()

while n < (int(options.duration)*60*60/int(options.interval)):
    try:
        opener = urllib2.build_opener()
        opener.addheaders.append(('Cookie', COOKIE_STRING))
        result = opener.open(options.url).read()
    except (urllib2.HTTPError, urllib2.URLError), e:
        print "Error loading resource: %s" % e
        result = None
    if result and options.searchstring in result:
        if options.growl:
            gntp.notifier.mini('Found "%s"' % options.searchstring)
        print 'Found %s' % options.searchstring
    else:
        print 'Could not find "%s"' % options.searchstring
    time.sleep(int(options.interval))
