snakeberry
==========

Snakeberry is a lightweight media server for Raspberry Pi written in Python. It can be controlled by an Android app. At the moment Snakeberry can play radio streams using mplayer.

Snakeberry founder page: http://github.com/salendron/Snakeberry

This modification can save the last radio station to a config file and resume playing after a service / device restart. Saving and restoring the last mixer volume is possible too.

On the founders project page wiki you can find installing instructions. For snakeberry intalling to the raspberry pi using the "snakeberryService" from this repository.

Additional files are:
* configMgr.py - a simple config file manager
* snakeberry.cfg - a config file (would be generated automatically)

Entries for snakeberry.cfg are following (in the "LastStream" section)
- description (holds the station description string displaying in top of the Android app)
- url (holds the station stream url)
- mustresume: true/false (indicates if a station wants to resume playing after a restart of the pi / service)
- forceresume: true/false (indicates if the last station should resume without accept - always)

The first three entries are auto updated. "MustResume" is updating if the radio station is playing or was stopped. Stopped streams would not be resumed after a restart. The manually setting of "ForceResume" to "true" cause to well-defined resuming of the last radio station.

In the "Common" section will be stored the current mixer volume as an entry named "LastVolume".


Snakberry is dual-licensed under the MIT (http://www.opensource.org/licenses/mit-license.php) and the Beerware (http://en.wikipedia.org/wiki/Beerware) license.
