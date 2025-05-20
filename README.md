## This project has been replaced by [wani-kani-downloader](https://github.com/math-man-123/wanikani-downloader)!
It is now part of my personal website, providing even more functionality directly from your web browser.

## WaniKani recent mistakes to Anki cards
A simple python script to fetch your recent mistakes from WaniKani and turn them into Anki cards.

## Step by step guide
1. First make sure to install needed python librarys. Mainly genanki, requests, and pytz.

  ```bash
  pip install genanki
  pip install requests
  pip install pytz
  ``` 

2. Open SETTINGS.py and paste in your WaniKani API token. Also set your timezone and how recent your mistakes should be.

  ```python
  API_TOKEN = "12345-67890ab-cdef1234-567890ab-cdef"
  TIME_ZONE = "Europe/Berlin"
  TIME_DELTA = 24
  ``` 

3. Download all the files and put them in some folder. Next on Windows simply double click on RUNME.bat. On other systems manually run anki.py. Now simply import IMPORTME.apkg into Anki. Enjoy!
