#!/usr/bin/env python
# star-greader-posts.py
# Erik Paulson
# epaulson@unit1127.com
# 10-4-2011
#
# Based heavily on code
# from http://blog.yjl.im/2010/08/using-python-to-get-google-reader.html
# and other sources included in the README

from xml.dom import minidom
from xml.dom import EMPTY_NAMESPACE
import urllib
import urllib2
import sys


def addStar(feed, item, token):
  item_star_data = urllib.urlencode({
       'a': 'user/-/state/com.google/starred',
       'async': 'true',
       's' : feed,
       'i' : item,
       'T' : token
      })

  reader_star_url = r'http://www.google.com/reader/api/0/edit-tag?client=myApp'
  reader_star_req = urllib2.Request(reader_star_url, item_star_data, header)
  try:
    reader_star_resp = urllib2.urlopen(reader_star_req)

  except urllib2.HTTPError, e:
    print('There was a problem with the HTTP server: ' + str(e.code))
  except urllib2.URLError, e:
    print('There was a problem with the URL: ' + str(e.reason))
  except: 
    print("An unexpected error occurred")   
 
  for line in reader_star_resp:
    print line



# Main program starts here
if len(sys.argv) != 4: 
	sys.exit("Usage: python star-greader-posts.py starred.xml your-new-google-reader-account your-password")

posts_to_star = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]

# Authenticate to obtain Auth
auth_url = 'https://www.google.com/accounts/ClientLogin'
auth_req_data = urllib.urlencode({
    'Email': username,
    'Passwd': password,
    'service': 'reader'
    })
auth_req = urllib2.Request(auth_url, data=auth_req_data)
auth_resp = urllib2.urlopen(auth_req)
auth_resp_content = auth_resp.read()
auth_resp_dict = dict(x.split('=') for x in auth_resp_content.split('\n') if x)
AUTH = auth_resp_dict["Auth"]

# Create a cookie in the header using the Auth
header = {'Authorization': 'GoogleLogin auth=%s' % AUTH}

# Now, we need to get a token to write values into Google Reader
token_url = r'http://www.google.com/reader/api/0/token'
token_req = urllib2.Request(token_url, None, header)
token_resp = urllib2.urlopen(token_req)
token = token_resp.read()


# Scan through the Atom doc you saved from the previous account
# and for each entry, star it
ATOM_NS = 'http://www.w3.org/2005/Atom'
doc = minidom.parse(posts_to_star)
doc.normalize()

for entry in doc.getElementsByTagNameNS(ATOM_NS, u'entry'):
  title = entry.getElementsByTagNameNS(ATOM_NS, u'title')[0].firstChild.data
  id = entry.getElementsByTagNameNS(ATOM_NS, u'id')[0].firstChild.data

  feed = entry.getElementsByTagNameNS(ATOM_NS, u'source')[0]
  feedVal = feed.getAttribute('gr:stream-id');

  print "Starring %s  - id %s of feed %s" % (title, id, feedVal)
  addStar(feedVal, id, token)
