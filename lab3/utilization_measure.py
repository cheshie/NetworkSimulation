from sys import path, argv
from os import system, getcwd
path.append(getcwd() + "/..")
import nstrace

queue_sizes = [4, 5, 8, 10, 12, 16, 20, 22, 26, 30]

def link_count(filename):
   count = 0

   fhandle = nstrace.nsopen(filename)
   for fline in fhandle.readlines():
       if nstrace.isEvent(fline):
           eventpl = nstrace.getEvent(fline)
           if nstrace.checkevent(eventpl):
               count += 1
   return count

def prepare_testfiles():
    for sz in queue_sizes:
        system(f'ns basic1.tcl {sz} && mv queue_{sz}.tr queue_util_tests')
#

def experiment_lab3():
    queues = {}
    for sz in queue_sizes: 
        queues[sz] = link_count(f'queue_util_tests/queue_{sz}.tr')
    return queues
#

#prepare_testfiles()
print(experiment_lab3())
