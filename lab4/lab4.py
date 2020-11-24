from sys import path, argv
from os import getcwd
path.append(getcwd() + "/..")
import nstrace
from collections import Counter
from itertools import groupby
from operator import itemgetter
from lab2 import ns_plotter
import matplotlib.pyplot as plt

seq_counter = Counter()

# Get list of all sequence numbers
def dup_counter(filename):
    fhandle = nstrace.nsopen(filename)
    seqlist = []
    global drop_count
    drop_count = 0
    for fline in fhandle.readlines():
        if nstrace.isEvent(fline):
            event = nstrace.getEvent(fline)
            if nstrace.rec_event(event):
                seqlist.append((event.seqno, event.time))
            elif nstrace.drop_event(event):
                drop_count += 1
              
    return seqlist
#


# Add seqlist to Counter so that it will count how many times each sequence appears
seqlist = dup_counter(argv[1])
seq_counter.update([x[0] for x in seqlist])
# Get only duplicate seq numbers
dup_seqs = dict([(x[0], []) for x in seq_counter.most_common() if x[1] > 1])
# Assign timestamps to these duplicates 
for seq in seqlist:
    if seq[0] in dup_seqs.keys():
        dup_seqs[seq[0]].append(seq[1])

print("Duplicated entries (and exact times of their transmission): ")
print(dup_seqs)

print(f"Total packets sent: {len(seqlist)}, losses: {drop_count}, loss rate: {drop_count / len(seqlist)}")


dup_seqs = {43: [0.83536, 1.437824], 45: [0.84536, 1.569056], 47: [0.85536, 1.589056], 49: [0.86536, 1.700288], 51: [0.87536, 1.720288], 53: [0.88536, 1.740288], 55: [0.89536, 1.83152], 57: [0.90536, 1.85152], 58: [0.91536, 1.86152], 59: [1.016592, 1.87152], 60: [1.026592, 1.88152], 61: [1.036592, 1.89152], 62: [1.046592, 1.952752]}

x, y = ns_plotter.prepare_data(argv[1])
plt.plot(x, y, 'r*')

for sq in dup_seqs.keys():
    for tm in dup_seqs[sq]: 
        plt.plot(tm,sq, 'bo')

plt.show()




