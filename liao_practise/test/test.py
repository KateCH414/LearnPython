# --*-- coding:utf-8 --*--
from datetime import  datetime
import re
def to_timestamp(dt_str, tz_str):
    dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
    zone = re.match(r'UTC\+(\d):00', tz_str)
    if zone:
        zone.group(1)

if __name__ == '__main__':
    t1 = to_timestamp('2015-6-1 08:10:30', 'UTC+7:00')
