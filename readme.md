# Wifi Hunter

Discover wifi networks near you and store them into a log.

Requires `iwlist` installed. Which should be install on most if not all linux distros.

Uses `python 3`

**Example use case**

Set this up on a raspberry pi and use a battery block to take it around with you and collect wifi networks. Since it stores a time stamp you can run this in parallel with a gps tracking app like Strava. Record your path and correlate the time stamp of the fetched wifi connection to the time of your walk/run/cycle.

**To run**
In terminal go to the location of the cloned/downloaded repo and run
`python3 wifihunter.py`