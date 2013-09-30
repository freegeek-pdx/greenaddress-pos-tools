import urllib
import json
from PyQt4.Qt import QThread
from urllib import FancyURLopener

class TrackerOpener(FancyURLopener):
   version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'

class Ticker(QThread):
    def __init__(self, source, currency, url, fields, interval, callback):
        QThread.__init__(self)
        self.source = source
        self.url = url
        self.fields = fields
        self.interval = interval
        self.callback = callback

    def run(self):
        self.sleep(5)   # give GUI time to initialize
        while True:
            try:
                myopener = TrackerOpener()
                f = myopener.open(self.url)
                data = f.read()
                feed = json.loads(data)
                rate = feed
                for field in self.fields:
                    rate = rate[field]
                rate = float(rate)
                self.callback(rate, self.source)
            except (ValueError, KeyError):
                print "Warning: Unable to parse exchange rate ticker"
            except IOError:
                print "Warning: Unable to access exchange rate ticker"
            self.sleep(self.interval)
