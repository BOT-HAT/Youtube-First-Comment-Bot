# -*- coding: utf-8 -*-
import httplib2
import os
import sys
import time

from apiclient.discovery import build_from_document
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

# ======== Configure the following variables ===========
#uploads id
cid="UUX6OQ3DkcsbYNE6v8uQQuVA"
#last video id wMuYiLby3-s
lastvid="Z9WQy9uEY8M"
# waiting time intervel in seconds
intervel=5
#comment you need to post
comment="Put your text here"

CLIENT_SECRETS_FILE = "./client_secrets.json"
YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0
To make this sample run you will need to populate the client_secrets.json file
found at:
   %s
with information from the APIs Console
https://console.developers.google.com
For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))
def get_authenticated_service(args):
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SSL_SCOPE,
    message=MISSING_CLIENT_SECRETS_MESSAGE)

  storage = Storage("%s-oauth2.json" % sys.argv[0])
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, args)
  with open("youtube-v3-discoverydocument.json", "r") as f:
    doc = f.read()
    return build_from_document(doc, http=credentials.authorize(httplib2.Http()))
def insert_comment(youtube, parent_id, text):
  insert_result = youtube.commentThreads().insert(
  part="snippet",
  body={
    "snippet": {
      "videoId": parent_id,
      "topLevelComment": {
        "snippet": {
          "textOriginal": text
          }
        }
      }
    }
  )
  response = insert_result.execute()
  print ("comment added")
def lastvideo(youtube, cid):
  request = youtube.playlistItems().list(
    part="snippet",
    playlistId=cid
    )
  response = request.execute()
  return(response["items"][0]["snippet"]["resourceId"]["videoId"])
argparser.add_argument("--text", help="Required; text that will be used as comment.")
args = argparser.parse_args()
args.videoid=lastvid
args.text=comment
youtube = get_authenticated_service(args)
i=0
while True:
    last=lastvideo(youtube,cid)
    i=i+1
    if(last!=lastvid):
      print(last)
      try:
        insert_comment(youtube, last, args.text)
      except HttpError as e:
        print ("An HTTP error %d occurred:\n%s") % (e.resp.status, e.content)
      else:
        print ("Comment Inserted")
        break
    time.sleep(intervel)
    print("waiting......")
    print ("Cycle:", i)
