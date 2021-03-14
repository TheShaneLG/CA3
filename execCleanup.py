import json
from bs4 import BeautifulSoup
import datetime
import os
import re
from requests import get, post
from moodleintegration import LocalGetSections,LocalUpdateSections

###############################################################
# This function will initiate the cleaning process
###############################################################
class OperationCleanup():
    def __init__(self, cid):
        self.reset = emptyMoodle (courseid=cid)

###############################################################
# This function will clean the moodle data
###############################################################
def emptyMoodle(courseid):
    for i in range(1, 8):
        data = [{'type': 'num', 'section': 0, 'summary': '', 'summaryformat': 1, 'visible': 1, 'highlight': 0,
                 'sectionformatoptions': [{'name': 'level', 'value': '1'}]}]
        data[0]['summary'] = ""
        data[0]['section'] = i
        sec_write = LocalUpdateSections(courseid, data)
        print("The data is reset to initial stage for week : " + str(i))
