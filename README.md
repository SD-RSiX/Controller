[SD]RSiX project aims, firstly, to automate Layer 2 deployments in an Internet Exchange Point (IXP). In Brazilian IXPs, the connected Autonomous Systems (ASes) exchange traffic multilaterally using two VLANs, one for IPv4 and the other for IPv6, and bilaterally using VLANs defined by the IXP to connect two or more ASes.

Bilateral VLANs creation and MAC filter updates represent about 40% of the total of the tickets open [1]. Add to that connecting or removing an AS requires configuring VLANs (two or more), filters, and the management system. All these operations may be automated reducing manual e repetitive work, and consequently turning the workflow more reliable.

The SDN approach of the Layer 2 enables an SDN approach for the management, integrating OpenFlow counters with traditional monitoring protocols gathered in a fully automated system.

_____________________________________________

[1] Statistics got from the Brazilian IXP tickets system (my.ix.br) database.

Tell about the configurations (IP, Docker network) and link here how to change the OVS operating mode.

# Building and Running

----------------------

This project has been maintained/developed by RSiX team and researchers from the [Informatics Institute](http://www.inf.ufrgs.br/site/) of the [Federal University of Rio Grande do Sul](http://www.ufrgs.br/english/home).
