# GTFS Clean
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

_Removes unneeded stops in a GTFS database for faster usage in Home Assistant_

## Credit

[Renemarc](https://github.com/renemarc/home-assistant-config/tree/master/gtfs) did the hard work of detailing what needed to be done.

## Installation

This app is best installed using
[HACS](https://github.com/custom-components/hacs), so that you can easily track
and download updates.

Alternatively, you can download the `cleangtfs` directory from inside the `apps` directory here to your
local `apps` directory, then add the configuration to enable the `cleangtfs` module.

## How it works

When a transit group releases a new gtfs.zip for their network, A number of manual steps are required
for Home Assistant to most effectively use the new data. As described by 
[Renemarc](https://github.com/renemarc/home-assistant-config/tree/master/gtfs) there
will be a efficiency problem due to most people only requiring a few stops from the network
of any transit group, therefore removing all the unneeded stop information can speed up your system.

While this is an irregular occurance, I found that my local transit group was releasing over 4 new files
a year, making me redo the delete and index processes, and I needed to write myself a process to complete each time. 
This app removes the need to complete the manual steps.

_Note: That you can have multiple transit systems in HA, just rename each zip file to something appropriate._

* Download your GTFS zip file from [Open Mobility](https://transitfeeds.com/)
* Delete any earlier gtfs.zip and gtfs.sqlite related files in the /config/gtfs directory of Home Assistant
* Place the new zip file into the /config/gtfs directory of Home Assistant 
* Restart Home Assistant - this will build a new sqlite database from the zip file
* This app will complete the manual deletes, updates and build the indexes described by Renemarc 
* Restart Home Assistant

### To Run

You will need to create an entity for each gtfs database in use (see below to pass the name). When this
`input_boolean` is turned on, whether manually or by another automation you
create, the clean up process will be run on the GTFS file named in `apps.yaml`.

## App configuration

```yaml
gtfs_cleanup:
  module: cleangtfs
  class: Clean_GTFS
  GTFS_DB: "mygtfs.sqlite"
  MY_STOPS: "5000,5001,5023"
  GTFS_FLAG: "input_boolean.clean_mygtfs"
```

key | optional | type | default | description
-- | -- | -- | -- | --
`module` | False | string | | `cleangtfs`
`class` | False | string | | `Clean_GTFS`
`GTFS_DB` | False | string || The name of the gtfs database file to clean up
`MY_STOPS` | False | string || A comma separated list of the stop ids you want to RETAIN in your database
`GTFS_FLAG` | False | string || The name of the flag in HA for cleaning this database - e.g. input_boolean.clean_gtfs 

## Issues/Feature Requests

Please log any issues or feature requests in this GitHub repository for me to review.