'''
Created on 27-09-2013

@author: Damian
'''
import datetime

def to_string(o):
    if o:
        if isinstance(o, basestring):
            return "'" + o + "'"
        elif isinstance(o, datetime.datetime):
            return "'" + str(o) + "'"
        else:
            return str(o)
    else:
        return "None"
