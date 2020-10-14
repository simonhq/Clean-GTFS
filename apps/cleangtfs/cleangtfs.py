############################################################
#
# This class aims to update a GTFS (SQLite3) database, and 
# remove the stops and stop times that are not relevant to 
# an application. 
#
# written to be run from AppDaemon for a HASS or HASSIO install
#
# After downloading your gtfs.zip file from https://transitfeeds.com/
# you can rename the file at this point so that you can watch multiple 
# feeds if necessary 
##
# all instructions below show where the zip file is renamed from [gtfs] 
##
# place it in the config\gtfs folder of your install
# delete the current [gtfs].sqlite file and Restart HA
# HA will build the new [gtfs].sqlite file from the [gtfs].zip
#
# then turn on your flag (input_boolean) and wait for it to turn off
# you will need to restart HA once more for the GTFS data to work
#
# Written: 27/12/2019
# This has been based upon Renemarc's guide
# https://github.com/renemarc/home-assistant-config/tree/master/gtfs
############################################################

############################################################
# 
# In the apps.yaml file you will need the following
# updated for your database path, stop ids and name of your flag
#
#gtfs_cleanup:
#  module: cleangtfs
#  class: Clean_GTFS
#  GTFS_DB: "action.sqlite"
#  MY_STOPS: "5513,5517,1736,1737,4979,4972,3418,3419,4529,3003,3409,13,1808,1803,1076,1075,1078,1077,2705,2709,2710,2706"
#  GTFS_FLAG: "input_boolean.clean_gtfs"
#  global_dependencies:
#    - globals
#    - secrets
#
############################################################


# import the database and database error function libraries
import os
import sqlite3
from sqlite3 import Error
import appdaemon.plugins.hass.hassapi as hass
#import globals

class Clean_GTFS(hass.Hass):

    # this assumes that the path to your gtfs file is /config/gtfs/[gtfs.sqlite]
    GTFS_PATH = ""
    # use the [name] of your [gtfs].sqlite file
    GTFS_DB = "" 
    # list the stops that you want to RETAIN in your database for use in the system
    MY_STOPS = "" 
    # the name of the flag in HA (input_boolean.xxx) that will be watched/turned off
    GTFS_FLAG = ""

    # run each step against the database
    def initialize(self):

        # get the values from the app.yaml that has the relevant personal settings
        #self.GTFS_DB = globals.get_arg(self.args, "GTFS_DB")
        self.GTFS_DB = self.args["GTFS_DB"]
        self.GTFS_PATH = os.path.join("/config","gtfs", self.GTFS_DB)
        #self.MY_STOPS = globals.get_arg(self.args, "MY_STOPS")
        self.MY_STOPS = self.args["MY_STOPS"]
        #self.GTFS_FLAG = globals.get_arg(self.args, "GTFS_FLAG")
        self.GTFS_FLAG = self.args["GTFS_FLAG"]
        

        # listen to HA for the flag to see if it is necessary to run this code against a new database
        self.listen_state(self.main, self.GTFS_FLAG, new="on")

    # run the app
    def main(self, entity, attribute, old, new, kwargs):
        """ create a connection to the gtfs database
            remove the stops and stop times 
            create indexes
            clean up the database 
        """
        # create the connection
        conn = self.create_connection(self.GTFS_PATH)

        # if connection is valid
        if conn != None:
            # run all the sql commands
            sql = "DELETE FROM stops WHERE stop_id NOT IN (" + self.MY_STOPS + ")"
            self.run_sql(conn, sql)
            sql = "DELETE FROM stop_times WHERE stop_id NOT IN (" + self.MY_STOPS + ")"
            self.run_sql(conn, sql)
            sql = "CREATE INDEX idx_trips_service_id ON trips(service_id)"
            self.run_sql(conn, sql)
            sql = "CREATE INDEX idx_stop_times_stop_id ON stop_times(stop_id)"
            self.run_sql(conn, sql)
            sql = "CREATE INDEX idx_stop_times_trip_id ON stop_times(trip_id)"
            self.run_sql(conn, sql)
            sql = "CREATE INDEX idx_stop_times_stop_sequence ON stop_times(stop_sequence)"
            self.run_sql(conn, sql)
            sql = "CREATE INDEX idx_stop_times_departure_time ON stop_times(departure_time)"
            self.run_sql(conn, sql)
            sql = "UPDATE routes SET agency_id = (SELECT agency_id FROM agency)"
            self.run_sql(conn, sql)
            sql = "vacuum"
            self.run_sql(conn, sql)
            
            # close the connection
            conn.close()
            # turn off the flag in HA to show completion
            self.turn_off(self.GTFS_FLAG)

        # otherwise log error
        else:
            self.log("Error connecting to database")


    def create_connection(self, db_file):
        """ create a connection to the gtfs database 
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            self.log(e)
        
        return conn

    def run_sql(self, conn, sql):
        """ delete the unwanted stops from the gtfs database 
        :param conn: connection object for the database
        :return: 
        """
        # log to Appdaemon log
        self.log(sql)
        # create a cursor to run commands
        curs = conn.cursor()

        # run the sql delete
        try:
            curs.execute(sql)
        except Error as e:
            self.log(e)

        # commit the changes
        try:
            conn.commit()
        except Error as e:
            self.log(e)


    



