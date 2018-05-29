# -*- coding: utf-8 -*-
"""
Created on Fri May 25 16:35:56 2018

@author: Siva
"""

import datetime
import collections

def datetime_str(recorddatetime):
    return recorddatetime.strftime("%Y-%m-%d %H:%M:%S")

class Session:
    doccount=0
    def __init__(self, inputrecord, session_duration):
        self.ip=inputrecord.ip
        self.docs=set()
        self.docs.add(inputrecord.doc)
        self.startdatetime= inputrecord.startdatetime
        self.enddatetime = inputrecord.startdatetime
        self.sessionenddatetime = inputrecord.startdatetime + session_duration

    def update(self, inputrecord, session_duration):
        if(inputrecord.ip == self.ip):
            self.docs.add(inputrecord.doc)
            self.enddatetime = inputrecord.startdatetime
            self.sessionenddatetime = inputrecord.startdatetime + session_duration

    def output(self):
        duration = self.enddatetime - self.startdatetime
        return "{},{},{},{},{}".format(self.ip, datetime_str(self.startdatetime), datetime_str(self.enddatetime), int(duration.total_seconds()+1), len(self.docs))

class ReadRecord:

    def __init__(self, recordstring):
        self.parse_record(recordstring)

    def parse_record(self,recordstring):
        splits = recordstring.split(",")
        self.ip =  splits[0]
        startdate = datetime.datetime.strptime(splits[1],"%Y-%m-%d").date()
        starttime = datetime.datetime.strptime(splits[2],"%H:%M:%S").time()
        self.startdatetime = datetime.datetime.combine(startdate,starttime)
        self.doc = (splits[4], splits[5], splits[6])

class Solution(object):
    def __init__(self):
        self.records_dic = collections.OrderedDict()

    def record(self,inputrecord, session_duration, outputfile):
        temp={}
        for key,value in self.records_dic.items():
            if value.sessionenddatetime < inputrecord.startdatetime:
                outputfile.write(value.output()+"\n")
                temp[key]=value
                #del self.records_dic[key]
        all(map(self.records_dic.pop,temp))


        if not inputrecord.ip in self.records_dic:
            sess = Session(inputrecord, session_duration)
            self.records_dic[inputrecord.ip]= sess
        else:
            self.records_dic[inputrecord.ip].update(inputrecord, session_duration)

    def run(self):
        
        with open("inactivity_period.txt","r") as iptxt:#Read input .txt file
            session_duration=datetime.timedelta(seconds=int(iptxt.read()))#Convert to time format
            
        optxt=open("sessionation.txt","w+")#Open output .txt file
        
        with open("log1.csv", "r") as f:#Read each line of .csv file
            f.readline() #skip header
            for line in f :
                inputrecord = ReadRecord(line)
                self.record(inputrecord, session_duration, optxt)

        for key, value in self.records_dic.items(): #At the end,writing output to all open sessions
            optxt.write(value.output()+"\n")

if __name__ == "__main__":
    Solution().run()