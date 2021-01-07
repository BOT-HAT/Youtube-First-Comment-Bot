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
id, interval, comment, do_init_auth, duration, client_secrets = itemgetter("id", "interval", "comment", "do_init_auth",
                                                                           "duration", "client_secrets")(
    json.load(open("./config.json", "r")))
cycles = (((duration.get("hours", 0) * 60) + duration.get("minutes", 0)) * 60 + duration.get("seconds", 0)) / interval

CLIENT_SECRET_DIR = os.path.join(os.path.dirname(__file__), "client_secret")
OAUTH2_DIR = os.path.join(os.path.dirname(__file__), "oauth2")
YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
YOUTUBE_API_SERVICE_NAME = "service"
YOUTUBE_API_VERSION = "v3"
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0
To make this sample run you will need to populate the client_secret json files
found at:
   %s
with information from the APIs Console
https://console.developers.google.com
For more information about the client_secret.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(CLIENT_SECRET_DIR)
# converts id to playlistId and store in pid
pid = "UU" + id[2:] if id[:2] == "UC" else id
print "id:", id + ",", "pid:", pid


def authenticate_all(flags):
    for i in range(0, len(client_secrets)):
        print "Authenticating", client_secrets[i]
        run_flow(flow_from_clientsecrets(os.path.join(CLIENT_SECRET_DIR, client_secrets[i] + ".json"),
                                         scope=YOUTUBE_READ_WRITE_SSL_SCOPE, message=MISSING_CLIENT_SECRETS_MESSAGE),
                 Storage(os.path.join(OAUTH2_DIR, client_secrets[i] + "-oauth2.json")), flags)


def get_authenticated_service(flags, infoNum):
    flow = flow_from_clientsecrets(os.path.join(CLIENT_SECRET_DIR, client_secrets[infoNum] + ".json"),
                                   scope=YOUTUBE_READ_WRITE_SSL_SCOPE, message=MISSING_CLIENT_SECRETS_MESSAGE)

    storage = Storage(os.path.join(OAUTH2_DIR, client_secrets[infoNum] + "-oauth2.json"))
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
    return False if response.get("error", False) else response["items"][0]["snippet"]["resourceId"]["videoId"]


argparser.add_argument("--text", help="Required; text that will be used as comment.")
flags = argparser.parse_args()
flags.text = comment
if do_init_auth:
    authenticate_all(flags)

project = 0
youtube = None
last_video = None
while youtube is None:
    try:
        youtube = get_authenticated_service(flags, project)
        last_video = get_last_video(youtube, pid)
    except:
        print "Quota for project", project, "has been reached."
        project += 1
        if project >= len(client_secrets):
            print "Recycling projects..."
            project = 0

print "last_video:", last_video

i = 0
while i < cycles or duration.get("dontStop", False):
    try:
        current_last = get_last_video(youtube, pid)
        if not current_last or True:
            raise HttpError(403, "manually raised")
        if current_last != last_video:
            print "Current video:", current_last
            try:
                insert_comment(youtube, current_last, flags.text)
            except HttpError as e:
                print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
            else:
                print "Comment Inserted"
                break
    except:
        print "Quota for project", project, "has been reached."
        project += 1
        if project >= len(client_secrets):
            print "Recycling projects..."
            project = 0
        youtube = get_authenticated_service(flags, project)
    i += 1
    time.sleep(interval)
    print("waiting......")
    print "Cycle:", i
