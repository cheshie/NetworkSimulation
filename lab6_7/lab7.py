from sys import path, argv
import matplotlib.pyplot as plt
from os import getcwd
from subprocess import PIPE, Popen
path.append(getcwd() + "/..")
import nstrace

delayB = list(range(60 + 1))

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
    packets = {}
    for sz in delayB:
        cmd = Popen(['ns', 'basic2.tcl', f'{sz}'], stdout=PIPE)
        res = [y for x in list(cmd.stdout)[0].decode().rstrip('\n').split('=') 
                    for y in x.split()]
        packets[int(float(res[1]))] = [float(res[3]), float(res[5])]
        
    return packets
#

def plot_lab7(packets):
    # plot RTTratio ** 2
    plt.plot(packets.keys(), [x[0] for x in packets.values()], 'r')
    # plot goodput
    plt.plot(packets.keys(), [x[1] for x in packets.values()], 'b')
    
    # plot points for RTTration and goodput
    for btt_size in packets:
        plt.plot(btt_size, packets[btt_size][0], 'ro')
        plt.plot(btt_size, packets[btt_size][1], 'bo')
    plt.show()

#packets = prepare_testfiles()
packets  = {0: [1.0, 1.006228], 1: [1.018264, 1.011139], 2: [1.036694, 1.011964], 3: [1.055289, 1.011905], 4: [1.07405, 1.01103], 5: [1.092975, 0.172296], 6: [1.112066, 1.273773], 7: [1.131322, 1.250254], 8: [1.150744, 1.150193], 9: [1.170331, 0.902664], 10: [1.190083, 0.286836], 11: [1.21, 2.268141], 12: [1.230083, 2.191325], 13: [1.250331, 1.256758], 14: [1.270744, 1.212483], 15: [1.291322, 1.121637], 16: [1.312066, 4.037981], 17: [1.332975, 3.733443], 18: [1.35405, 3.61885], 19: [1.375289, 2.309711], 20: [1.396694, 0.962498], 21: [1.418264, 4.165131], 22: [1.44, 4.3112], 23: [1.461901, 3.218782], 24: [1.483967, 1.796688], 25: [1.506198, 1.087538], 26: [1.528595, 4.678606], 27: [1.551157, 4.459105], 28: [1.573884, 4.026687], 29: [1.596777, 2.152587], 30: [1.619835, 1.236648], 31: [1.643058, 4.474151], 32: [1.666446, 5.511156], 33: [1.69, 4.4965], 34: [1.713719, 2.028161], 35: [1.737603, 1.485915], 36: [1.761653, 7.157924], 37: [1.785868, 7.837927], 38: [1.810248, 6.950842], 39: [1.834793, 2.553779], 40: [1.859504, 2.331585], 41: [1.88438, 5.925741], 42: [1.909421, 4.990758], 43: [1.934628, 6.383049], 44: [1.96, 3.45699], 45: [1.985537, 1.805602], 46: [2.01124, 7.854425], 47: [2.037107, 5.816624], 48: [2.06314, 5.469152], 49: [2.089339, 3.243436], 50: [2.115702, 2.277023], 51: [2.142231, 7.144132], 52: [2.168926, 6.351582], 53: [2.195785, 5.70599], 54: [2.22281, 3.804754], 55: [2.25, 2.208684], 56: [2.277355, 8.050942], 57: [2.304876, 6.613225], 58: [2.332562, 8.348465], 59: [2.360413, 2.920506], 60: [2.38843, 1.909918]}

plot_lab7(packets)
