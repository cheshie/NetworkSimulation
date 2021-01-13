#Filename: sample2.tcl

#*******************Random Topology Creation*******************#
#Random Location for a two nodes

for {set i 0} {$i < 2} {incr i} {

$node_($i) set X_ [expr rand()*500]
$node_($i) set Y_ [expr rand()*400]
$node_($i) set Z_ 0

}
