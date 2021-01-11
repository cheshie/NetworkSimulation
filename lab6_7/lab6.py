from sys import path, argv
import matplotlib.pyplot as plt
from os import system, getcwd
path.append(getcwd() + "/..")
import nstrace

delayB=[0,5,23,24,25,26,35,36,40,41,45,60,61,85,110]

def link_count(filename):
   count_A = 0
   count_B = 0
   rec_A = 0
   rec_B = 0

   fhandle = nstrace.nsopen(filename)
   for fline in fhandle.readlines():
       if nstrace.isEvent(fline):
           eventpl = nstrace.getEvent(fline)
           # 0 => A, 1 => B
           drop_ev = nstrace.drop_event_id(eventpl, send_node=(0,1), dest_node=3)
           if drop_ev == 0:
               count_A += 1
           elif drop_ev == 1:
               count_B += 1
           elif drop_ev == 3:
               rec_A += 1
           elif drop_ev == 4:
               rec_B += 1
   return count_A, count_B, rec_A // 2, rec_B // 2

def prepare_testfiles():
    for sz in delayB:
        system(f'ns basic2.tcl {sz}')
#

def plot_lab6(packets):
    x = list(packets.keys())
    y = list(packets.values())
    plt.plot(x,y)
    for btt_size in packets:
        plt.plot(btt_size, packets[btt_size][0], 'r*')
    plt.show()

packets = {
    0 : [1.006228],
    5 : [0.172296],
    23 : [3.218782 ],
    24 : [1.796688],
    25 : [1.087538],
    26 : [4.678606],
    35 : [1.485915],
    36 : [7.157924],
    40 : [2.331585],
    41 : [5.925741],
    45 : [1.805602],
    60 : [1.909918],
    61 : [8.240510],
    85 : [2.493663 ],
    110 : [3.808113]
}

plot_lab6(packets)
