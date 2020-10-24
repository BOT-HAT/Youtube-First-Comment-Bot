# Youtube-First-Comment-Bot
A bot for automatically post comment when a youtube channel upload a new video. This bot checks a specified channel
every certain amount of seconds, and if a new video is found, this bot will post a pre-defined comment on that video.

## Requirments
- python version >= 3.5
- [Google API Client (Python)](https://github.com/googleapis/google-api-python-client)
- Google API Console project (create one [here](https://console.developers.google.com/))
- YouTube account

## Setup
Go to [Google API Console](https://console.developers.google.com/) to create an account (if you haven't) and create a
project. Remember to enable YouTube Data API for that project. Add an OAuth Client ID from "Create credentials" and
choose "Desktop app" from the drop-down menu on the next screen. After the client ID is created, download it by clicking
on the download button. Rename the file to `client_secret.json` and place it in the project's root directory, which is
in the same folder as this readme. Then, create a virtualenv environment and install google-api-python-client and
oauth2client in this project's root directory. Finally, create `config.json` using this as a template:
```json
{
  "id": "replace with channel id or playlist id",
  "interval": "replace with number of seconds per query as a number (not a string)",
  "comment": "replace with the comment you want to post"
}
```
`id` is the channel id or playlist id, `interval` is the number of seconds between each query (put a number here, the
string is just a placeholder), and `comment` is the comment to be posted.

## Running
Run `bot.py` with the virtualenv you've created. If this is the first time the program is run, or if the
`bot.py-oauth2.json` file is missing or empty, you will be prompted to login. You can always delete or clear that file
before running to log into another account. The script will then query YouTube API to retrieve the last posted video,
and then it will query every certain number of seconds (defined in `config.json`) to check whether there's a new video,
and if there is a new video, it will comment, and the program will terminate.

## Help
How to find video ID? see [this video](https://www.youtube.com/watch?v=RjUlmco7v2M).
To find last video, go the YouTube channel and check the URL of the latest upload. Using this URL
https://www.youtube.com/watch?v=RjUlmco7v2M for example, and the `v` parameter is the video ID (in this case, it is
"RjUlmco7v2M"). To set up a good time interval you must consider several things eg youtube API quata limit system
resources etc... If you are planning to run this bot 24/7, then set the interval between 20 and 25 seconds, and if you
are running this bot only for one or two hours, you can set this interval to 1 or 2 seconds. This is to prevent reaching
the API limit.

Note.
Feel free to modify. I have messed up with arguments in the last few section, the code still works but there is a lot of
room for improvements.
