"""
Work-in-progress!!!

Fetches some data from the fronius.db (filled by livedata2db.py)
and generats a graph.
"""

import matplotlib.pyplot as plt
import sqlite3 as lite
import argparse
import pandas
from datetime import timedelta, date, datetime

parser = argparse.ArgumentParser()

tomorrow = (datetime.today()+timedelta(days=1)).strftime('%Y-%m-%d')
yesterday = (datetime.today()-timedelta(days=1)).strftime('%Y-%m-%d')

parser.add_argument('start_date',
                    help='StartDate for json file generation: %Y-%m-%d', nargs='?', const=yesterday, default=yesterday)
parser.add_argument('end_date',
                    help='EndDate for json file generation: %Y-%m-%d',  nargs='?', const=tomorrow, default=tomorrow)
parser.add_argument('imageoutput',
                    help='Imageoutput path and filename',  nargs='?', const="/tmp/plot.jpg", default="/tmp/plot.jpg")
args = parser.parse_args()
start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
end_date = datetime.strptime(args.end_date, "%Y-%m-%d")
imageout = args.imageoutput

con = lite.connect('fronius.db')

with con:
    sql = "SELECT meter_timestamp, powerflow_P_PV FROM fronius WHERE date(meter_timestamp) BETWEEN '"+str(start_date)+"' AND '"+str(end_date)+"'"
    data = pandas.read_sql(sql, con)
#print (data)
plt.plot(data.meter_timestamp, data.powerflow_P_PV, linewidth=2.0)
plt.title("Powerflow between {0} and {1}".format(str(start_date), str(end_date)))
plt.savefig(imageout)