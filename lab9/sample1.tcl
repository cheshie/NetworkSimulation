#Filename: sample1.tcl

#TCL – Tool Command Language

# Simulator Instance Creation
set ns [new Simulator]

# Define options
set val(chan) Channel/WirelessChannel ;# channel type
set val(prop) Propagation/TwoRayGround ;# radio-propagation model

set val(netif) Phy/WirelessPhy ;# network interface type
set val(mac) Mac/802_11 ;# MAC type
set val(ifq) Queue/DropTail/PriQueue ;# interface queue type
set val(ll) LL ;# link layer type
set val(ant) Antenna/OmniAntenna ;# antenna model
set val(ifqlen) 50 ;# max packet in ifq
set val(nn) 2 ;# number of mobilenodes
set val(rp) AODV ;# routing protocol
set val(x) 500 ;# X dimension of topography
set val(y) 400 ;# Y dimension of topography
set val(stop) 10.0 ;# time of simulation end

# set up topography object
set topo [new Topography]
$topo load_flatgrid $val(x) $val(y)

#Nam File Creation nam – network animator
set namfile [open sample1.nam w]

#Tracing all the events and cofiguration
$ns namtrace-all-wireless $namfile $val(x) $val(y)

#Trace File creation
set tracefile [open sample1.tr w]

#Tracing all the events and cofiguration
$ns trace-all $tracefile

# general operational descriptor- storing the hop details in the network
create-god $val(nn)

# configure the nodes
$ns node-config -adhocRouting $val(rp) \
-llType $val(ll) \
-macType $val(mac) \
-ifqType $val(ifq) \
-ifqLen $val(ifqlen) \
-antType $val(ant) \
-propType $val(prop) \
-phyType $val(netif) \
-channelType $val(chan) \
-topoInstance $topo \
-agentTrace ON \
-routerTrace ON \
-macTrace OFF \
-movementTrace ON

#*******************Random Topology Creation*******************#
#Random Location for a two nodes

#***************Dynamic Wireless network **********************#

#******************Random Topology Creation********************#

#Run Time Argument

if {$argc != 1} {
error "\nCommand: ns sample3.tcl <no.of.nodes>\n\n "
}

# number of mobilenodes
set val(nn) [lindex $argv 0];

for {set i 0} {$i < $val(nn)} {incr i} {

# Node Creation
set node_($i) [$ns node]
# Initial color of the node
$node_($i) color black;
$node_($i) set X_ [expr rand()*500];
$node_($i) set Y_ [expr rand()*400];
$node_($i) set Z_ 0;

# Label and coloring
$ns at 0.1 "$node_($i) label Node($i);"
#Size of the node
$ns initial_node_pos $node_($i) 30

# set k 0.2
# while {$k < 1} {
#     $ns at $k "$node_($i) set X_ [expr rand()*500]"
#     $ns at $k "$node_($i) set Y_ [expr rand()*400]"
#     $ns at k "puts \"time: $k\";"
#     set k [expr {$k + 0.1}]
# }

}



# $ns at 0.2 "$node_(1) color blue"
# $ns at 0.2 "$node_(1) set Y_ [expr rand()*400];"

# ending nam and the simulation
$ns at $val(stop) "$ns nam-end-wireless $val(stop)"
$ns at $val(stop) "stop"

#Stopping the scheduler
$ns at 10.01 "puts \"end simulation\" ; $ns halt"
#$ns at 10.01 "$ns halt"
proc stop {} {
global namfile tracefile ns
$ns flush-trace
close $namfile
close $tracefile
#executing nam file
exec nam sample1.nam &
}

#Starting scheduler
$ns run

#############################################################
