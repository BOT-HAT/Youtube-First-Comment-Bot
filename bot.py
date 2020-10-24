import httplib2
import os
import sys
import time
import json
from operator import itemgetter

from googleapiclient.discovery import build_from_document
from googleapiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

# Configure these variables in config.json
id, interval, comment = itemgetter("id", "interval", "comment")(json.load(open("./config.json", "r")))

CLIENT_SECRETS_FILE = "client_secret.json"
YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
YOUTUBE_API_SERVICE_NAME = "service"
YOUTUBE_API_VERSION = "v3"
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0
To make this sample run you will need to populate the client_secret.json file
found at:
   %s
with information from the APIs Console
https://console.developers.google.com
For more information about the client_secret.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))
# converts id to playlistId and store in pid
pid = "UU" + id[2:] if id[:2] == "UC" else id
print "id:", id + ",", "pid:", pid

def get_authenticated_service(flags):
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SSL_SCOPE,
                                   message=MISSING_CLIENT_SECRETS_MESSAGE)

    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, flags)
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


def get_last_video(youtube, pid):
    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=pid
    )
    response = request.execute()
    return response["items"][0]["snippet"]["resourceId"]["videoId"]


argparser.add_argument("--text", help="Required; text that will be used as comment.")
flags = argparser.parse_args()
flags.text = comment
youtube = get_authenticated_service(flags)
last_video = get_last_video(youtube, pid)
print "last_video:", last_video

i = 0
while True:
    current_last = get_last_video(youtube, pid)
    i += 1
    if current_last != last_video:
        print current_last
        try:
            insert_comment(youtube, current_last, flags.text)
        except HttpError, e:
            print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
        else:
            print "Comment Inserted"
            break
    time.sleep(interval)
    print("waiting......")
    print "Cycle:", i
