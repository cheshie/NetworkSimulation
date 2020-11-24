# Source: http://intronetworks.cs.luc.edu/current/html/auxiliary_files/ns2/nstrace.py

# python routines for processing tracefiles.

# interface functions:
# nsopen(filename)
# isEvent(): Boolean for is the line just read in a 12-item trace line
# isVar(): the other option
# isEOF(): no more input
# getEvent(): returns tuple of 12 vars of the appropriate types, then gets new line
# getVar(): returns tuple of 7 vars of the appropriate types, then gets new line

# skipline(): reads in the next line

import sys
import re
from collections import namedtuple

# regular expressions can be used to check for specific trace-line formats,
# but they are slow, and are disabled by default
# # # # # # # # # # # # # # # # # # # # # # # # # # # 
numre = r"-?[0-9]+"
floatre = numre + r"(\.[0-9]+)?"
dotpairre = numre + r"\." + numre
stringre = r"\S+"
space = r'\s+'

event_re = r"\A[rd+-]" + space + floatre + space + numre + space + numre \
    + space + stringre + space + numre + space + r"\S{7}" + space + numre \
    + space +  dotpairre + space + dotpairre + space + numre + space + numre + "$"

var_re   = r"\A" + floatre + space + numre + space + numre + space + numre \
    + space + numre + space + stringre + space + floatre + "\s*$"
# # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # 
eventTpl_scheme = namedtuple('event_tuple', ["event", "time", "sendnode", "destnode", 
    "protocol", "size", "flags", "flow", "src_id", "dest_id", "seqno", "packet_id"])


def nsopen(filename):	
    try:
        theFile = open(filename, 'r')	# throws exception on failure
    except FileNotFoundError:
        print("file not found:", filename)
        exit(0)
    return theFile
#

def isEvent(line):
    if len(line.split()) == 12:
        if re.match(event_re, line):
            return True
        else:
            return False
    return len(line.split()) == 12
#

def isVar(line):
    if len(line.split()) == 7:
        if re.match(var_re, line):
            return True
        else:
            return False
    return len(line.split()) == 7
#

# action:str, time:float, source_node, dest_node, proto:str, size, flags:str, 
def getEvent(line):
    splitLine = line.split()
    tpl = eventTpl_scheme(
		splitLine[0],			# "r", "d", "+", "-"
		float(splitLine[1]),		# time
		int(splitLine[2]),		# sending node
		int(splitLine[3]),		# dest node
		splitLine[4],			# protocol
		int(splitLine[5]),		# size
		splitLine[6],			# flags
		int(splitLine[7]),		# flow ID
		pair(splitLine[8]),		# source (node flowid)
		pair(splitLine[9]),		# dest (node flowid)
		int(splitLine[10]),		# seq #
		int(splitLine[11])		# packet ID
		)
    return tpl
#

# time, source_node, source flowid, dest_node, dest_flowid, varname, value(float)
# double, int, int, int, int, string, double
def getVar(line):
    splitLine = line.split()
    tpl = (
		float(splitLine[0]),		# time
		int(splitLine[1]),		# source node
		int(splitLine[2]),		# source flowid
		int(splitLine[3]),		# dest node
		int(splitLine[4]),		# dest flowid
		splitLine[5],			# name of traced var
		float(splitLine[6])		# value
		)
    return tpl
#

# pair() takes a string of the form "n.m" and converts it to a tuple (n m)
def pair(dotline):
    lt = dotline.split(".")
    return (int(lt[0]), int(lt[1]))
#

def checkevent(eventpl):
    SEND_NODE = 1
    DEST_NODE = 2
    FLOW = 0
    
    if eventpl.event == "-" and eventpl.sendnode == SEND_NODE and eventpl.destnode == DEST_NODE \
        and eventpl.size >= 1000 and eventpl.flow == FLOW:
        return True
    else:
        return False
#

def rec_event(eventpl):
    SEND_NODE = 1
    DEST_NODE = 2
    FLOW = 0
    
    if eventpl.event == "r" and eventpl.destnode == DEST_NODE and eventpl.size >= 1000 \
        and eventpl.flow == FLOW:
        return True
    else:
        return False
#

def drop_event(eventpl):
    SEND_NODE = 1
    DEST_NODE = 2
    FLOW = 0
    
    if eventpl.event == "d" and eventpl.destnode == DEST_NODE and eventpl.size >= 1000 \
        and eventpl.flow == FLOW:
        return True
    else:
        return False
#
