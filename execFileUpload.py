import json
from bs4 import BeautifulSoup
import bs4
import datetime
import os
import re
from requests import get, post
from moodleintegration import LocalGetSections,LocalUpdateSections
from execVideoRetriveal import getVideos

#############################################
# This function will initiate the data upload
#############################################
class OperationUpload():
    def __init__(self,cid):
        self.updateSummary = getFiles(cid)

####################################
# This function will retrieve the files
####################################
def getFiles(cid):
    sec = LocalGetSections(cid)
    for subdir, dirs, files in os.walk("./"):
        for filename in files:
            if (filename.endswith(".html") or filename.endswith(".md") or filename.endswith(".pdf")) and subdir != "./":
                if filename.endswith(".md"):

                    title = open(os.path.join(subdir,filename),"r").readlines()[1]
                    title = title.replace('#','').strip()
                    weeknum = int(re.findall('\d+',subdir)[0])

                    concatinateLink(weeknum,title,subdir,sec,cid)

###############################################################
# This function will concatinate the links and upload in moodle
###############################################################
def concatinateLink (weeknum,title,dir,sec,cid):

      markdownlink = '<a href="https://mikhail-cct.github.io/ca3-test/wk' + str(weeknum) + '">Week ' + str (weeknum) + ': ' + title + '</a>'
      pdflink = '<br><a href="https://mikhail-cct.github.io/ca3-test/wk' + str(weeknum) + '/wk' + str (weeknum) + '.pdf">Week '+ str (weeknum)  + ": " + title + '.pdf</a>'

      summary = json.dumps(sec.getsections[weeknum]['summary'],indent=4,sort_keys=True)

      upload = False

      htmlfile = os.path.join(dir,"index.html")
      pdffile = os.path.join(dir,"wk" + str(weeknum) +".pdf")



      if os.path.exists(htmlfile) and title not in summary:
         summary = markdownlink

         upload = True
         print("Uploaded index.html file for week" + str(weeknum))

      if os.path.exists(pdffile) and title +'.pdf' not in summary:
          summary = markdownlink + pdflink
          upload = True
          print("Uploaded class pdf file for week" + str(weeknum))

      videoLink = getVideos(weeknum)

      if videoLink is not None and '.mp4' not in summary:
              summary = markdownlink + pdflink + videoLink
              upload = True
              print("Uploaded recorded videos for the week" + str(weeknum))

      if upload:
             data =[{'type':'num','section':0,'summary':'','summaryformat':1,'visible':1,'highlight':0,'sectionformatoptions':[{'name':'level','value':1}]}]
             data[0]['summary']= summary
             data[0]['section'] = weeknum
             LocalUpdateSections(cid,data)
      else:
             print("The week " + str(weeknum) + " files are up to date and no need for any further updates")








