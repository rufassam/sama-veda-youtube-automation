# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 00:00:43 2025

@author: Rufas
"""

#!/usr/bin/env python3

import os
import datetime
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def auth():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            "client_secret.json",
            SCOPES,
        )
        creds = flow.run_local_server(port=0)

        with open("token.json", "w") as f:
            f.write(creds.to_json())

    return build("youtube", "v3", credentials=creds)


def upload(video_path, day):
    yt = auth()

    title = f"Sama Veda Healing — Day {day} | Sleep • Peace • Meditation"
    desc = f"""
Sama Veda healing meditation series — Day {day}

Close your eyes.
Listen deeply.
Let the mind soften.

Music by Rufas Sam  
🙏
    """.strip()

    publish = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat("T") + "Z"

    request = yt.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": desc,
                "tags": ["sama veda", "meditation", "healing", "sleep music"],
                "categoryId": "10",
            },
            "status": {
                "privacyStatus": "private",
                "publishAt": publish
            },
        },
        media_body=MediaFileUpload(video_path, resumable=True),
    )

    response = None
    while response is None:
        status, response = request.next_chunk()

    print("Uploaded:", response["id"])


def main():
    files = sorted([
        f for f in os.listdir("output")
        if f.endswith(".mp4")
    ])

    if not files:
        raise RuntimeError("No videos to upload")

    day = len(files)
    video = os.path.join("output", files[-1])

    upload(video, day)


if __name__ == "__main__":
    main()
