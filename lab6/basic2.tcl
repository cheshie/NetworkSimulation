# NS basic2 example of two TCPs competing on the same link. 
# The slow link is the second, B--D, link.

#Create a simulator object
set ns [new Simulator]

# Obtain base script name, without extension, eg name="basic2"
# This automatically gives tracefiles the same base name as the script
# Does NOT support path names for scripts, eg ns ../foo.tcl
set name [lindex [split [info script] "."] 0]

# set up tracing (nam tracing commented out here)
set trace [open $name.tr w]
$ns trace-all $trace
#set nf [open $name.nam w]
#$ns namtrace-all $nf

#Define different colors for data flows (only relevant for nam use)
$ns color 0 Red
$ns color 1 Blue

############## some globals (modify as desired) ##############

# queuesize on bottleneck link
set queuesize 20

# default run time, in seconds
set endtime 300

# "overhead" of D>0 introduces a uniformly randomized delay d, 0â¤dâ¤D; 0 turns it off.
set overhead 0

# ADDITIONAL delay on the B--R link second link, in ms
set delayB 0

# estimated no-load RTT for the first flow, in ms
# the following is reasonable for bottleneckBW = 8.0Mb
set RTTNL 220

# bottleneckBW values used are either 8.0 Mbit or 0.8 Mbit
# The version embedded in the book text uses 0.8 Mbit
set bottleneckBW 8.0
set bottleneckBW 0.8

############## command-line parameters ##############

if { $argc >= 1 } {
    set delayB [expr [lindex $argv 0]]
} 
if { $argc >= 2 } {
    set overhead [expr [lindex $argv 1]]
} 

if { $argc >= 3 } {
    set bottleneckBW [expr [lindex $argv 2]]
} 

if { $argc >= 4 } {
    set endtime [expr [lindex $argv 3]]
} 
if { $argc >= 5 } {
    set queuesize [expr [lindex $argv 4]]
} 

############## arrange for output ############## 

set outstr [format "parameters: delayB=%f overhead=%f bottleneckBW=%f" $delayB $overhead $bottleneckBW]
puts stdout $outstr

#Define a 'finish' procedure that prints out progress for each connection

proc finish {} {
        global ns tcp0 tcp1 end0 end1 queuesize trace delayB overhead RTTNL
        set ack0 [$tcp0 set ack_]
        set ack1 [$tcp1 set ack_]
        # counts of packets *received*
        set recv0 [expr round ( [$end0 set bytes_] / 1000.0)] 
        set recv1 [expr round ( [$end1 set bytes_] / 1000.0)] 
        # see numbers below in topology-creation section
        set rttratio [expr (2.0*$delayB+$RTTNL)/$RTTNL] 
        # actual ratio of throughputs fast/slow; the 1.0 forces floating point
        set actualratio [expr 1.0*$recv0/$recv1]
        # theoretical ratio fast/slow with squaring; see text for discussion of ratio1 and ratio2
        set rttratio2 [expr $rttratio*$rttratio]
        set ratio1 [expr $actualratio/$rttratio]
        set ratio2 [expr $actualratio/$rttratio2]
        set outstr [format "delayB=%f actualratio=%f " $delayB $actualratio ]
        puts stdout $outstr
        $ns flush-trace
        close $trace
        exit 0
}

############### create network topology ############## 

# A      
#   \     
#     \   
#      R---D (Destination)
#     /
#   /
# B

#Create four nodes

set A [$ns node]
set B [$ns node]
set R [$ns node]
set D [$ns node]

# bandwidth on the A--R and B--R links, faster
set fastbw [expr $bottleneckBW * 10]

#Create links between the nodes
$ns duplex-link $A $R ${fastbw}Mb 10ms DropTail
$ns duplex-link $B $R ${fastbw}Mb [expr 10 + $delayB]ms DropTail
# this last link is the bottleneck; 1000 bytes at 0.80Mb => 10 ms/packet; at 8.0 Mbps => 1 ms/packet
# At 0.8 Mb R--D one-way delay is thus 100 ms prop + 10 ms bandwidth = 110 ms; A--D one-way is  121, RTT from A is ~231
# At 8.0 Mb, R--D one-way is 101ms; A--D one-way is 111.1 ms, RTT is ~220 ms
# propdelay0 = 125 makes A--D twice as long as B--D (one-way).
# the values 0.8Mb, 100ms are from Floyd & Jacobson

$ns duplex-link $R $D ${bottleneckBW}Mb 100ms DropTail

# nam "orient" attributes are included here
$ns duplex-link-op $A $R orient right-down
$ns duplex-link-op $B $R orient right-up
$ns duplex-link-op $R $D orient right

$ns queue-limit $R $D $queuesize

#Monitor the queue in the nam animation for the link between nodes R and D
$ns duplex-link-op $R $D queuePos 0.5

############## create and connect TCP agents, and start ############## 

Agent/TCP set window_ 65000
Agent/TCP set packetSize_ 960
Agent/TCP set overhead_ $overhead

#Create a TCP agent and attach it to node A, the delayed path
set tcp0 [new Agent/TCP/Reno]
$tcp0 set class_ 0
# set the flowid here, used as field 8 in the tracefile
$tcp0 set fid_ 0
$tcp0 attach $trace
$tcp0 tracevar cwnd_
$tcp0 tracevar ack_
$ns attach-agent $A $tcp0

set tcp1 [new Agent/TCP/Reno]
$tcp1 set class_ 1
$tcp1 set fid_ 1
$tcp1 attach $trace
$tcp1 tracevar cwnd_
$tcp1 tracevar ack_
$ns attach-agent $B $tcp1

set end0 [new Agent/TCPSink]
$ns attach-agent $D $end0

set end1 [new Agent/TCPSink]
$ns attach-agent $D $end1

#Connect the traffic source with the traffic sink
$ns connect $tcp0 $end0  
$ns connect $tcp1 $end1

#Schedule the connection data flow
set ftp0 [new Application/FTP]
$ftp0 attach-agent $tcp0

set ftp1 [new Application/FTP]
$ftp1 attach-agent $tcp1

$ns at 0.0 "$ftp0 start"
$ns at 0.0 "$ftp1 start"
$ns at $endtime "finish"

#Run the simulation
$ns run
