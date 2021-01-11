from sys import path, argv
import matplotlib.pyplot as plt
from os import system, getcwd
path.append(getcwd() + "/..")
import nstrace

bttnck_sizes=[0,5,23,24,25,26,35,36,40,41,45,60,61,85,110]

#todo? 
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
    for sz in bttnck_sizes:
        system(f'ns basic2.tcl {sz}')
#

def experiment_lab3():
    btt_nck = {}
    for sz in bttnck_sizes: 
        btt_nck[sz] = link_count(f'bottleneck_tests/bttnck_{sz}.tr')
        print("dropped (A): ", btt_nck[sz][0], "dropped (B): ", btt_nck[sz][1], "Received (from) A:", btt_nck[sz][2], "Received (from) B: ", btt_nck[sz][3])
    return btt_nck
#

def plot_ex_1(packets):
    for btt_size in packets:
        # A drop => 0 (red)
        plt.plot(btt_size, packets[btt_size][0], 'r*')
        # B drop => 1 (blue)
        plt.plot(btt_size, packets[btt_size][1], 'b*')
    plt.show()

def plot_ex_2(packets):
    x = list(packets.keys())
    y = list(packets.values())
    plt.plot(x,y)
    for btt_size in packets:
        print(": ", packets[btt_size][0])
        plt.plot(btt_size, packets[btt_size][0], 'r*')
    plt.show()

#packets = experiment_lab3()

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
110 : [3.808113]}

plot_ex_2(packets)
#prepare_testfiles()
#print(experiment_lab3())
