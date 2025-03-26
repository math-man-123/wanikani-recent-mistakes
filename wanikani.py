import requests, time, sys, json
from datetime import datetime, timedelta
from pytz import timezone, utc
from SETTINGS import API_TOKEN, TIME_ZONE


# Requests WaniKani API endpoint with given params
def apiRequest(endpoint, params={}, retries=3, delay=2):
    url = "https://api.wanikani.com/v2/" + endpoint
    token = API_TOKEN
    headers = {"Authorization": "Bearer " + token}

    print(f"Sending API request to endpoint {endpoint}.")
    for attempt in range(retries):
        try:  # fetching data from endpoint and returning it
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()

            print(f"Successfully fetched data from {endpoint}.")
            return response.json()

        except requests.exceptions.RequestException as e:
            # if some error occures print a warning
            print(f"API request error on attempt {attempt + 1}: {e}")

            # retry fetching data after short delay
            if attempt < retries - 1:
                print(f"Retrying in {delay} seconds.")
                time.sleep(delay)
                delay *= 2

    # Terminate script if no data is received
    print(f"Failed fetching data from {endpoint}.")
    print("Terminating script now.")
    sys.exit()


# Dumps given data into a named JSON file
def dumpJsonFile(data, name):
    print(f"Dumping data into {name}.json.")
    with open(f"wanikani/{name}.json", "w") as file:
        json.dump(data, file, indent=4)


# Current time delta hours ago (UTC) formated for API
def getHoursAgo(delta):
    now_cet = datetime.now(timezone(TIME_ZONE))
    ago_cet = now_cet - timedelta(hours=delta)
    ago_utc = ago_cet.astimezone(utc)

    return ago_utc.strftime("%Y-%m-%dT%H:%M:%SZ")


# Checks if given review is a mistake or not
def isMistake(review):
    meaning_mistake = review["data"]["meaning_current_streak"] <= 1
    reading_mistake = review["data"]["reading_current_streak"] <= 1

    return meaning_mistake or reading_mistake


# Finds primary item that matches condition
def getPrimary(items, condition=(lambda item: True)):
    for item in items:
        if item["primary"] and condition(item):
            return item
    return {}


# Returns similar visually kanji as character array
def getSimilar(subject):
    # return [] as subject is not a kanji
    if not subject["object"] == "kanji":
        return []
    print("Looking for visually similar Kanjis.")

    # return [] as no visually similar Kanjis exist
    ids = subject["data"]["visually_similar_subject_ids"]
    if not ids:
        print("No visually similar Kanjis found.")
        return []

    # grab data from WaniKani API about similar Kanjis
    ids = ",".join(map(str, ids))
    similar = apiRequest(endpoint="subjects", params={"ids": ids})["data"]

    # return only important data i.e. character and meaning
    return [
        {
            "character": subject["data"]["characters"],
            "meaning": getPrimary(subject["data"]["meanings"]).get("meaning", ""),
        }
        for subject in similar
    ]


# Gets review and subject data from WaniKani API
# Returns relevant data for anki notes to use
def getNoteData(delta):
    # Get recent review data from WaniKani API
    reviews = apiRequest(
        endpoint="review_statistics", params={"updated_after": getHoursAgo(delta)}
    )

    # Only keep ids of recent mistakes
    reviews = reviews["data"]
    mistakes = [
        str(review["data"]["subject_id"]) for review in reviews if isMistake(review)
    ]

    # Get mistaken subject data from WaniKani API
    subjects = apiRequest(endpoint="subjects", params={"ids": ",".join(mistakes)})

    # Only keep relevant info for Anki
    subjects = subjects["data"]
    subjects = [
        {**subject["data"], "type": subject["object"], "similar": getSimilar(subject)}
        for subject in subjects
    ]

    # fmt: off
    meaning = lambda data: {
        "meaning": data["meaning"], 
        "primary": data["primary"]}

    reading = lambda data: {
        "reading": data["reading"],
        "primary": data["primary"],
        "type": data.get("type", "")}

    # organise relevant data in easibly accesible format
    note = lambda subject: {
        # basic information about the note
        "type": subject["type"],
        "subject": subject["characters"],

        # meanings information about the note
        "meanings": [meaning(data) for data in subject.get("meanings", [])],
        "meaning_mnemonic": subject.get("meaning_mnemonic", ""),

        # readings information about the note
        "readings": [reading(data) for data in subject.get("readings", [])],
        "reading_mnemonic": subject.get("reading_mnemonic", ""),

        # visually similar kanji information
        "similar_kanji": subject["similar"],
    }

    return [note(subject) for subject in subjects]
