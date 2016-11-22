# Wifi hunter by Clyde Smets <clyde.smets@gmail.com>
#
# @Desc
# Wifi hunter will scan for any available networks and store them into a JSON
# file. This is just a fun little tool to find networks around your area. Put it
# on a Raspberry Pi and run Strava to find out where the networks are according
# to the timestamp.
#
# Will require iwlist install on your OS. Should come standard with any linux
# distro.
#
# Process:
# 1. Scan for all available wifi networks
# 2. Create a json file to store found connection if file doesn't already exist.
#    If file already exists open it.
# 3. Scan through imported json file to see if the connection already exists.
#    If it's a new ESSID add it into the object with a time stamp, otherwise
#    check it's signal level. If the number is lower update the result and
#    update the time stamp.
# 4. Set wait time before looping back to step 1.

import iwlist
import json
import os.path
import datetime
import sched, time

def writeJSONFile (file, content):
    with open(file, 'w') as f:
        json.dump(content, f, sort_keys = True, indent = 4,
                  ensure_ascii = False)

def scan (s, loopTime):
    # Run iwlist to store all found wifi results into a list
    content = iwlist.scan()
    wifiList = iwlist.parse(content) # list containing objects with wifi data

    wifiFile  = 'wifi_found.json'
    wifiJSON = [] #list to store updated results

    # Load json file if it already exists
    if os.path.isfile(wifiFile):
        with open(wifiFile) as jsonFile:
            wifiJSON = json.load(jsonFile)

        wifiListCount = len(wifiList) # Number of wifi connections found
        wifiJSONCount = len(wifiJSON) # Number of wifi connections stored

        # Loop through found networks
        for wi in range(wifiListCount):

            found = False

            # Loop through stored networks
            for wfi in range(wifiJSONCount):
                # Check if the wifi network id already exists
                if wifiList[wi]['essid'] == wifiJSON[wfi]['essid']:
                    # Check if it shares the same mac address
                    if wifiList[wi]['mac'] == wifiJSON[wfi]['mac']:
                        found = True
                        # Update it's signal strength if it's closer
                        # and update it's timestamp
                        if int(wifiList[wi]['signal_level']) < int(wifiJSON[wfi]['signal_level']):
                            wifiJSON[wfi]['signal_level'] = wifiList[wi]['signal_level']
                            time = datetime.datetime.now().time()
                            wifiJSON[wfi]['time'] = str(time)
                        break

            # If it's a new network found add it to the list
            if found == False:
                wifiJSON.append(wifiList[wi])

        # Overwrite the existing JSON file with the new list.
        writeJSONFile(wifiFile, wifiJSON)

    else:
        # Write original wifi list to JSON if no file exists.
        writeJSONFile(wifiFile, wifiList)

    # Loop through scan
    s.enter(1, loopTime, scan(s, loopTime))


def hunt (loopTime = 1):
    # Init the schedular which will be used to loop the scan every x amount of
    # time.
    s = sched.scheduler(time.time, time.sleep)
    s.enter(1, loopTime, scan(s, loopTime))
    s.run()

hunt(1)
