from sys import path, argv
import matplotlib.pyplot as plt
from os import getcwd, system
from subprocess import PIPE, Popen
path.append(getcwd() + "/..")
import nstrace

# DelayB values:
# lab6 => 0,5,23,24,25,26,35,36,40,41,45,60,61,85,110]
# lab7 => range(60 + 1)
delayB=list(range(25, 55))
overhead_lab8 = [0, 0.005, 0.01, 0.02]

def prepare_testfiles_lab6():
    for sz in delayB:
        system(f'ns basic2.tcl {sz}')
#

def prepare_testfiles_lab7():
    packets = {}
    for sz in delayB:
        cmd = Popen(['ns', 'basic2.tcl', f'{sz}'], stdout=PIPE)
        res = [y for x in list(cmd.stdout)[0].decode().rstrip('\n').split('=') 
                    for y in x.split()]
        packets[int(float(res[1]))] = [float(res[3]), float(res[5])]
        
    return packets
#

def prepare_testfiles_lab8():
    packets = {}
    for sz in delayB:
        overhead_res = []
        for ov in overhead_lab8:
            cmd = Popen(['ns', 'basic2.tcl', f'{sz}', f'{ov}'], stdout=PIPE)
            res = [y for x in list(cmd.stdout)[0].decode().rstrip('\n').split('=') 
                        for y in x.split()]
            # add goodput to the list
            overhead_res.append(float(res[-1]))
            
        packets[int(float(res[1]))] = overhead_res
        
    return packets
#

def plot_lab6(packets):
    x = list(packets.keys())
    y = list(packets.values())
    plt.plot(x,y)
    for btt_size in packets:
        plt.plot(btt_size, packets[btt_size][0], 'r*')
    plt.show()
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
#

def plot_lab8(packets):
    # plot goodput
    for i in range(4):
        plt.plot(packets.keys(), [x[i] for x in packets.values()], markerfacecolor='#333399', markeredgecolor='k')
    
    # TODO dorobic oznaczenia (legende) kolorow pozamieniac kolory zeby byly jak w dokumencie
    
    # plot points for goodput
    for btt_size in packets:
        plt.plot(btt_size, packets[btt_size][0], markerfacecolor='k', markeredgecolor='#333399', marker='o')
        plt.plot(btt_size, packets[btt_size][1], markerfacecolor='k', markeredgecolor='#333399', marker='o')
        plt.plot(btt_size, packets[btt_size][2], markerfacecolor='k', markeredgecolor='#333399', marker='o')
        plt.plot(btt_size, packets[btt_size][3], markerfacecolor='k', markeredgecolor='#333399', marker='o')
    plt.show()
#

#lab8:

#packets = prepare_testfiles_lab8()
packets = {25: [1.087538, 1.279239, 0.84442, 0.776934], 26: [4.678606, 2.224903, 1.206348, 1.059718], 27: [4.459105, 2.514159, 1.175821, 1.10542], 28: [4.026687, 1.329931, 1.190774, 1.100906], 29: [2.152587, 0.779006, 0.924735, 1.011537], 30: [1.236648, 1.145746, 0.944994, 1.127214], 31: [4.474151, 3.049204, 1.360336, 1.135683], 32: [5.511156, 2.767513, 0.886674, 1.423705], 33: [4.4965, 1.772918, 1.229185, 1.341612], 34: [2.028161, 0.705642, 1.28179, 0.991728], 35: [1.485915, 1.430919, 1.037734, 1.170589], 36: [7.157924, 2.551176, 1.351497, 1.117802], 37: [7.837927, 3.18313, 1.325205, 1.359482], 38: [6.950842, 1.754909, 1.340818, 1.109714], 39: [2.553779, 0.891728, 1.156018, 0.893778], 40: [2.331585, 1.161037, 1.33161, 1.248477], 41: [5.925741, 2.42605, 1.457529, 1.218348], 42: [4.990758, 3.226812, 1.24784, 1.275391], 43: [6.383049, 1.683992, 1.766684, 1.246297], 44: [3.45699, 0.875761, 1.430875, 1.263222], 45: [1.805602, 1.295909, 1.647847, 1.094549], 46: [7.854425, 4.77963, 1.536617, 1.231397], 47: [5.816624, 4.249578, 1.726152, 1.57288], 48: [5.469152, 1.787758, 1.785536, 1.491521], 49: [3.243436, 0.808178, 1.405078, 1.23011], 50: [2.277023, 1.411044, 1.028596, 1.451664], 51: [7.144132, 3.342694, 1.731472, 1.397369], 52: [6.351582, 3.475037, 2.114724, 1.735202], 53: [5.70599, 2.048224, 1.269751, 1.418978], 54: [3.804754, 1.34287, 1.353657, 1.045371]}

plot_lab8(packets)

"""
#lab6:

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
"""
"""
#lab7:

packets  = {0: [1.0, 1.006228], 1: [1.018264, 1.011139], 2: [1.036694, 1.011964], 3: [1.055289, 1.011905], 4: [1.07405, 1.01103], 5: [1.092975, 0.172296], 6: [1.112066, 1.273773], 7: [1.131322, 1.250254], 8: [1.150744, 1.150193], 9: [1.170331, 0.902664], 10: [1.190083, 0.286836], 11: [1.21, 2.268141], 12: [1.230083, 2.191325], 13: [1.250331, 1.256758], 14: [1.270744, 1.212483], 15: [1.291322, 1.121637], 16: [1.312066, 4.037981], 17: [1.332975, 3.733443], 18: [1.35405, 3.61885], 19: [1.375289, 2.309711], 20: [1.396694, 0.962498], 21: [1.418264, 4.165131], 22: [1.44, 4.3112], 23: [1.461901, 3.218782], 24: [1.483967, 1.796688], 25: [1.506198, 1.087538], 26: [1.528595, 4.678606], 27: [1.551157, 4.459105], 28: [1.573884, 4.026687], 29: [1.596777, 2.152587], 30: [1.619835, 1.236648], 31: [1.643058, 4.474151], 32: [1.666446, 5.511156], 33: [1.69, 4.4965], 34: [1.713719, 2.028161], 35: [1.737603, 1.485915], 36: [1.761653, 7.157924], 37: [1.785868, 7.837927], 38: [1.810248, 6.950842], 39: [1.834793, 2.553779], 40: [1.859504, 2.331585], 41: [1.88438, 5.925741], 42: [1.909421, 4.990758], 43: [1.934628, 6.383049], 44: [1.96, 3.45699], 45: [1.985537, 1.805602], 46: [2.01124, 7.854425], 47: [2.037107, 5.816624], 48: [2.06314, 5.469152], 49: [2.089339, 3.243436], 50: [2.115702, 2.277023], 51: [2.142231, 7.144132], 52: [2.168926, 6.351582], 53: [2.195785, 5.70599], 54: [2.22281, 3.804754], 55: [2.25, 2.208684], 56: [2.277355, 8.050942], 57: [2.304876, 6.613225], 58: [2.332562, 8.348465], 59: [2.360413, 2.920506], 60: [2.38843, 1.909918]}
plot_lab7(packets)
"""
