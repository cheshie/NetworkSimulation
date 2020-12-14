from sys import path, argv
import matplotlib.pyplot as plt
from os import system, getcwd
path.append(getcwd() + "/..")
import nstrace

bttnck_sizes=[0.8,1,1.5,2,2.5,3,3.5,4,4.5,5,6,7,8]

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
    for sz in btnck_sizes:
        system(f'ns competing.tcl {sz} && mv bttnck_{sz}.tr bottleneck_tests')
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
    for btt_size in packets:
        print(": ", (packets[btt_size][0]+packets[btt_size][1]) / (packets[btt_size][2] + packets[btt_size][3]))
        plt.plot(btt_size, (packets[btt_size][0]+packets[btt_size][1]) / (packets[btt_size][2] + packets[btt_size][3]), 'r*')
    plt.show()

#packets = experiment_lab3()

packets = {
0.8 : [91,86,14936,14856],
1 : [93,92,18407,18382],
1.5 : [78,85,26963,26347],
2 : [66,75,34531,34345],
2.5 : [61,70,41656,41494],
3 : [57,65,49190,49032],
3.5 : [52,60,56132,55922],
4 : [47,56,63590,63340],
4.5 : [45,54,70267,69975],
5 : [42,51,77441,76577],
6 : [38,47,91388,90511],
7 : [34,43,104284,103895],
8 : [32,41,121125,114825]}

plot_ex_2(packets)

#prepare_testfiles()
#print(experiment_lab3())
