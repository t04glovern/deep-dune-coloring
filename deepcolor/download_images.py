import urllib2
import urllib
import json
import numpy as np
import cv2
import untangle

maxsize = 512
count = 0

for i in xrange(10000):
    stringreturn = urllib2.urlopen("http://safebooru.org/index.php?page=dapi&s=post&q=index&tags=1girl%20solo&pid="+str(i+3000)).read()
    xmlreturn = untangle.parse(stringreturn)
    for post in xmlreturn.posts.post:
        imgurl = "http:" + post["sample_url"]
        print imgurl
        if ("png" in imgurl) or ("jpg" in imgurl):
            cropped = None
            resp = urllib.urlopen(imgurl)
            image = np.asarray(bytearray(resp.read()), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            height, width = image.shape[:2]
            if height > width:
                scalefactor = (maxsize*1.0) / width
                res = cv2.resize(image,(int(width * scalefactor), int(height*scalefactor)), interpolation = cv2.INTER_CUBIC)
                cropped = res[0:maxsize,0:maxsize]
            if width > height:
                scalefactor = (maxsize*1.0) / height
                res = cv2.resize(image,(int(width * scalefactor), int(height*scalefactor)), interpolation = cv2.INTER_CUBIC)
                center_x = int(round(width*scalefactor*0.5))
                print center_x
                cropped = res[0:maxsize,center_x - maxsize/2:center_x + maxsize/2]

            count += 1
            if cropped is not None:
                cv2.imwrite("imgs/"+str(count)+".jpg",cropped)
            else:
                cv2.imwrite("imgs/"+str(count)+".jpg",image)
