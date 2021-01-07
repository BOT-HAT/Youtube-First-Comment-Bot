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
project. Remember to enable YouTube Data API for that project. Set up the OAuth consent screen, where you only need to
input the application name. Then, add an OAuth Client ID from "Create credentials" and choose "Desktop app" from the
drop-down menu on the next screen. After the client ID is created, download it by clicking on the download button.
Create the folders `client_secret` and `oauth2` in the project root directory and place the client ID file in
`client_secret`. You can add more than one from other projects to increase the quota limit. Then, create a virtualenv
environment and install google-api-python-client and oauth2client in this project's root directory. Finally, create
`config.json` using this as a template:
```json
{
  "id": "replace with channel id or playlist id",
  "interval": "replace with number of seconds per query as a number (not a string)",
  "comment": "replace with the comment you want to post",
  "do_init_auth": "replace with a boolean indicating whether you want to authenticate (it is recommended that you set it to true for the first run and leave it false until you need to switch YouTube accounts)",
  "duration": {
    "hours": "hours you intend the bot to run (as a number, not string)",
    "minutes": "minutes you intend the bot to run after the specified number of hours has passed (as a number, not string)",
    "seconds": "seconds you intend the bot to run after the specified number of hours and minutes has passed (as a number, not string)",
    "dontStop": "replace with a boolean indicating whether or not to ignore the specified duration and run indefinitely"
  },
  "client_secrets": "replace with an array of the client ID file names without the file extensions"
}
```

<details>
    <summary>Example:</summary>
    
```json
{
  "id": "UCBR8-60-B28hp2BmDPdntcQ",
  "interval": 5,
  "comment": "I'm the first to post!",
  "do_init_auth": true,
  "client_secrets": [
    "client_secret_1",
    "client_secret_2",
    "client_secret_3",
    "client_secret_4",
    "client_secret_5"
  ]
}
```

</details>

`id` is the channel id or playlist id, `interval` is the number of seconds between each query (put a number here, the
string is just a placeholder), `comment` is the comment to be posted, `do_init_auth` determines whether to prompt the
sign-in screens right after  the program is run, and `client_secrets` is an array of every client ID file name without
the extension.

## Running
Run `bot.py` with the virtualenv you've created. If this is the first time the program is run, set `do_init_auth` to
true so that the program will prompt the sign-in screens when the program starts instead of when the program switches to
a different project. If any one of the oauth2 files are missing or empty, you will be prompted to login when the program
gets to that project. You can always set `do_init_auth` to `true` before running to log into another account. The script
will query YouTube API to retrieve the last posted video, and then it will query every certain number of seconds
(defined in `config.json`) to check whether there's a new video, and if there is a new video, it will comment, and the
program will terminate. If the quota limit is reached before that, the program will automatically choose a new project.

## Help
How to find video ID? see [this video](https://www.youtube.com/watch?v=RjUlmco7v2M).
To find last video, go the YouTube channel and check the URL of the latest upload. Using this URL
https://www.youtube.com/watch?v=RjUlmco7v2M for example, and the `v` parameter is the video ID (in this case, it is
"RjUlmco7v2M"). To set up a good time interval you must consider several things eg youtube API quata limit system
resources etc... If you are planning to run this bot 24/7, then set the interval between 20 and 25 seconds, and if you
are running this bot only for one or two hours, you can set this interval to 1 or 2 seconds. This is to prevent reaching
the API limit. However, you can extend that time by including more client ID files, each from a different project.

Note.
Feel free to modify. I have messed up with arguments in the last few section, the code still works but there is a lot of
room for improvements.
