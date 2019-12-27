
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

