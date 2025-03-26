# WaniKani recent mistakes to Anki cards
A simple python script to fetch your recent mistakes from WaniKani and turn them into Anki cards.

![example](https://github.com/user-attachments/assets/9b0331c6-39e0-412f-ab51-319e0b399d6e)

# Step by step guide
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

3. On Windows simply double click on RUNME.bat. On other systems manually run anki.py. Now simply import IMPORTME.apkg into Anki.
