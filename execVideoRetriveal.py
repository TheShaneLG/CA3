# import the required libraries
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import re
from datetime import datetime, timedelta

SCOPES = ['https://www.googleapis.com/auth/drive']

###############################################################
# This function will get the Videos from Google Drive
###############################################################
def getVideos(weeknum):
    # Variable creds will store the user access token.
    # If no valid token found, we will create one.
    creds = None
    # Check if file token.pickle exists
    if os.path.exists('token.pickle'):
        # Read the token from the file and
        # store it in the variable creds
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If no valid credentials are available,
    # request the user to log in.
    if not creds or not creds.valid:

        # If token is expired, it will be refreshed,
        # else, we will request a new one.
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

            # Save the access token in token.pickle
        # file for future usage
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

            # Connect to the API service
    service = build('drive', 'v3', credentials=creds)

    # request a list of first N files or
    # folders with name and id from the API.

    query = f"'1pFHUrmpLv9gEJsvJYKxMdISuQuQsd_qX' in parents"
    resource = service.files()
    result = resource.list(pageSize=20, q=query,fields="nextPageToken, files(id, name, mimeType, size, parents, modifiedTime,webViewLink)").execute()

    file_list = result.get('files')
    links = []
    names = []

    for file in file_list:
        names.append(file['name'])
        links.append(file['webViewLink'])

    names_links = dict(zip(names, links))
    start_date = '2020-09-28'
    w = (weeknum - 1) * 7
    week_start = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=w)).strftime('%Y-%m-%d')
    for n, l in names_links.items():
        date = re.search("([0-9]{4}\-[0-9]{2}\-[0-9]{2})", n).group()
        if date >= week_start and date <= (datetime.strptime(week_start, '%Y-%m-%d') + timedelta(days=6)).strftime(
                '%Y-%m-%d'):
            video_title = n
            video_link = l
            return '<br><a href ="' + video_link + '">' + video_title + '</a>'

