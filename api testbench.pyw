import valo_api
import datetime
import time

def utc_to_local(utc_str):
    if utc_str.endswith('Z'):
        utc_str = utc_str[:-1]
    try:
        dt = datetime.datetime.strptime(utc_str, "%Y-%m-%dT%H:%M:%S.%f")
    except:
        dt = datetime.datetime.strptime(utc_str, "%Y-%m-%dT%H:%M:%S")
    dt = dt.replace(tzinfo=datetime.timezone.utc)
    local_dt = dt.astimezone()
    return local_dt

valo_api.set_api_key('HDEV-dec0a00b-3220-4745-81d7-f2908bf14a5d')

matches_today = 0
for match in valo_api.endpoints.get_lifetime_matches_by_name(version='v1', region='ap', name='blitz', tag='rizz', mode='Competitive'):
    if utc_to_local(match.meta.started_at).date() == datetime.datetime.now().date():
        matches_today += 1
print(matches_today)