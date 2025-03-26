# The script will try to fetch all your mistakes from now to
# TIME_DELTA hours back. For example if you want to grind
# all your mistakes from today in the evening set this to 24.

TIME_DELTA = 48


# Inorder to know what time "now" is the script needs to know
# your timezone. I am in Germany so my timezone is "Europe/Berlin".
# Pick your timezone from this list and set it accordingly:
#
# UTC (Coordinated Universal Time): "UTC"
# Eastern Time (US & Canada): "US/Eastern"
# Pacific Time (US & Canada): "US/Pacific"
# Central European Time: "Europe/Berlin"
# Greenwich Mean Time (GMT): "GMT"
# London Time (United Kingdom): "Europe/London"
# New York Time (US): "America/New_York"
# Tokyo Time (Japan): "Asia/Tokyo"
# Sydney Time (Australia): "Australia/Sydney"
# Mumbai Time (India): "Asia/Kolkata"
#
# If your timezone is not listed see the official documentation:
# https://pythonhosted.org/pytz/#country-information

TIME_ZONE = "Europe/Berlin"


# In order to aaccess your particular WaniKani data you will need to
# obtain an API token linked to your account. For that simply log in
# your WaniKani account and go to "Settings" > "API Tokens". Once there
# click on "Generate a new token" and give it only read permissions as
# the script does not need more than that. Next simply paste the token
# where it currently says PASTE_YOUR_TOKEN_HERE. Make sure not to remove
# the quotation marks. Once your done it should look something like this:
# API_TOKEN = "12345-67890ab-cdef1234-567890ab-cdef" (not a real token)

API_TOKEN = "PASTE_YOUR_TOKEN_HERE"
