import optparse
import json
import urllib2
import commands
import time
import os
import gntp.notifier
from datetime import datetime, timedelta
import re

parser = optparse.OptionParser()
parser.add_option("-g", "--growl",
                  dest="growl", default=False,
                  action="store_true",
                  help="Enable Growl notifications. Must have 'growlnotify' installed")

parser.add_option("-i", "--interval",
                  dest="interval", default=24,
                  help="Update interval (hours)")
parser.add_option("-b", "--begin",
                  dest="begin",
                  default="2012-01-01",
                  help="Begin date")
parser.add_option("-e", "--end",
                  dest="end",
                  default="2012-01-02",
                  help="End date")
parser.add_option("-f", "--format",
                  dest="format",
                  default="%Y-%m-%d",
                  help="Format of date in URL")

parser.add_option("-t", "--target",
                  dest="target",
                  default=os.getcwd(),
                  help="Target directory")

parser.add_option("-u", "--url",
                  dest="url",
                  default = "http://freshplum.com/%s",
                  help="URL to check")
(options, args) = parser.parse_args()


def intervals(start, stop, interval, format):
    start = datetime.strptime(start, format)
    stop = datetime.strptime(stop, format)
    interval = timedelta(hours=int(interval))

    dates = []
    i = start
    while i <= stop:
        dates.append(i.strftime(format))
        i += interval
    return dates

dates = intervals(options.begin, options.end, options.interval, options.format)
for i in dates:
    try:
        url = options.url % i

        remotefile = urllib2.urlopen(url)
        cd = remotefile.info().get('Content-Disposition')
        if cd:
            name = re.findall("filename=(\S+)", cd)[0].strip('"\'')
        else:
            name = options.url.rsplit('/')[-1] or options.url.rsplit('/')[-2]
            print url
        filename = '%s_%s' % (i.replace('/', '-'), name)

        path = os.path.join(options.target, filename)

        localFile = open(path, 'w')
        localFile.write(remotefile.read())
        localFile.close()

        if options.growl:
            gntp.notifier.mini('Saved "%s"' % url)

    except (urllib2.HTTPError, urllib2.URLError), e:
        print "Error loading resource: %s" % e
        result = None