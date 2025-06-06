#from atproto import Client
from bsky_bridge import BskySession, post_text

import argparse
import sqlite3
import datetime
from zoneinfo import ZoneInfo
from talkgroups import talkgroups
from secret_credentials import username, password

# Potentially use https://github.com/viktorholk/push-notifications-api 
# https://blog.finxter.com/5-best-ways-to-set-timezone-in-pythons-datetime/

parser = argparse.ArgumentParser()
parser.add_argument("talkgroup", help="The talkgroup of the message")
args = parser.parse_args()
tg = args.talkgroup
timezone = ZoneInfo('US/Eastern')

def convert_timestamp(val):
    """Convert Unix epoch timestamp to datetime.datetime object."""
    return datetime.datetime.fromtimestamp(int(val))

def convert_timestamp_to_local_string(val):
    """Convert Unix epoch timestamp to local time string"""
    return datetime.datetime.fromtimestamp(int(val), tz=timezone).strftime('%c')

def adapt_datetime_epoch(val):
    """Adapt datetime.datetime to Unix timestamp."""
    return int(val.timestamp())

sqlite3.register_converter("timestamp", convert_timestamp_to_local_string)
sqlite3.register_adapter(datetime.datetime, adapt_datetime_epoch)

con = sqlite3.connect("/code/db/activity.db", autocommit=True)
cur = con.cursor()

# Create tables if they don't already exist, and populate the talkgroup lookup table with the verbose names and IDs of the talkgroups we care about.
cur.execute("CREATE TABLE IF NOT EXISTS message_activity(talkgroup, timestamp)")
cur.execute("CREATE TABLE IF NOT EXISTS talkgroup_lookup(talkgroup text primary key, name)")
cur.executemany("INSERT INTO talkgroup_lookup (talkgroup, name) values (?, ?) ON CONFLICT(talkgroup) DO NOTHING;", talkgroups)



print("Inserting {} {}".format(args.talkgroup, datetime.datetime.now()))
cur.execute("INSERT INTO message_activity (talkgroup, timestamp) values (?, ?)", (args.talkgroup, datetime.datetime.now()))



res = cur.execute("SELECT talkgroup, name FROM talkgroup_lookup WHERE talkgroup = ?", (args.talkgroup,))
talkgroup_id, talkgroup_name = res.fetchone()

duration = datetime.datetime.now()-datetime.timedelta(minutes=15)
res = cur.execute("SELECT count(*) FROM message_activity WHERE talkgroup = ? AND timestamp > ?", (talkgroup_id, duration.timestamp(),) )
recent_activity_count = res.fetchone()[0]

day_duration = datetime.datetime.now()-datetime.timedelta(hours=24)
res = cur.execute("SELECT count(*) FROM message_activity WHERE talkgroup = ? AND timestamp > ?", (talkgroup_id, day_duration.timestamp(),) )
daily_activity_count = res.fetchone()[0]

res = cur.execute("SELECT timestamp FROM message_activity WHERE talkgroup = ? ORDER BY timestamp limit 2 offset 1", (talkgroup_id,) )
row = res.fetchone()
if row is not None and len(row)>0:
    last_timestamp = convert_timestamp_to_local_string(row[0])
else:
    last_timestamp = None


msg = f"Encrypted radio traffic detected on {talkgroup_id}: {talkgroup_name}. {daily_activity_count} messages detected in the last 24 hours, most recent previous on {last_timestamp}"

session = BskySession(username, password)
if recent_activity_count < 2:
    response = post_text(session, msg)
    #print('Would send skeet')
