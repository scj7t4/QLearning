from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

import urllib2

register_openers() # Poster stuff

TARGET = "http://localhost:11234/log"

def upload(name, tracefile):
    tracefile.seek(0)
    datagen, headers = multipart_encode({"data": tracefile, "name":name})
    request = urllib2.Request(TARGET, datagen, headers)
    print urllib2.urlopen(request).read()