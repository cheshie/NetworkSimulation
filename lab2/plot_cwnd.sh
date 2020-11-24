# first get all variable-trace lines that contain cwnd_ information
grep "cwnd_" basic1.tr | awk '{print $1, $7}' > basic1_cwnd.tr

# Now we should get file that contains two columns: time and value of the traced variable 
# 0.3833	3
# (...)
# To plot: (-P switch is used to plot points, not lines)
xgraph basic1_cwnd.tr -P

