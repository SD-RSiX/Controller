# Copyright (C) 2016 Nippon Telegraph and Telephone Corporation.
#               2018 [SD]RSiX Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# ------------------------------------------------------------------------------
#
# This file started as a fully commented version of the ExampleSwitch13.py App
# from the Ryu project
# (https://github.com/osrg/ryu/blob/master/ryu/app/simple_switch_13.py), but
# the original version has been modified to make it in a multi-switches learning
# app (the original version does not work with more than one switch).

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types


class LearningSwitch(app_manager.RyuApp):
    """OpenFlow learning switch

    A Ryu application inherits from ryu.base.app_manager that manages OpenFlow
    operations.
    """

    # A list of supported OpenFlow versions for this RyuApp. The default is all
    # versions supported by the framework.
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(LearningSwitch, self).__init__(*args, **kwargs)

        # Initiates a dictionary to store MAC-port mapping
        self.mac_to_port = {}

    # When Ryu receives an OpenFlow message, it generates an event handler with
    # a function and event object. Through a decorator of
    # ryu.controller.handler.set_ev_cls you may write a function to implement
    # your logic to process the event.
    #
    # The event handler specifies event classes for every OpenFlow message.
    # Using ryu.controller.ofp_event.EventOFP + <OpenFlow message name> in the
    # decorator you inform Ryu the message to handle the function it decorates.
    #
    # The decorator also receives one of the following dispatchers:
    #   HANDSHAKE_DISPATCHER: Exchange of HELLO message
    #   CONFIG_DISPATCHER: Waiting to receive SwitchFeatures message
    #   MAIN_DISPATCHER: Normal status
    #   DEAD_DISPATCHER. Disconnection of a connection

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        """Install table-miss flow entry

        When a switch connects, the controller requests the switch features; the
        features reply triggers this function, so the controller installs the
        table-miss entry the switch will use to send PacketIn messages.

        Args:
            ev (ev): instance of the OpenFlow event handler class
        """

        # data path of the connected OpenFlow switch
        datapath = ev.msg.datapath

        # ofproto module that supports the OpenFlow version in use
        ofproto = datapath.ofproto

        # ofproto_parser module
        parser = datapath.ofproto_parser

        # INSTALL THE TABLE-MISS ENTRY

        # create an empty match to match every packet
        match = parser.OFPMatch()

        # create an instance of OFPActionOutput class setting controller as the
        # output port and NO_BUFFER, so that the switch will not buffer the
        # the packets that generate a PacketIn
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]

        # Install the flow-entry
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        """PacketOut - Install a flow entry on a switch

        Args:
            datapath: data path of the switch
            priority: the priority the flow entry must be given
            match: match object the packets must match to this entry be applied
            action: action the switch will perform with the packet when a match
                    occurs
        """

        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Instructions are executed when a packet matches a flow entry; it
        # differs from the actions lists that the switch executes at the end of
        # the processing.
        # Using "ofproto.OFPIT_APPLY_ACTIONS" parameter, the controller informs
        # the switch to run the action list in that very same processing stage.
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]

        # Create the flow mod message
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        """PacketIn handler

        Handle PacketIns sent by switches to the controller. Switches use
        table-miss entry to communicate to the controller.

        Args:
            ev (ev): instance of the OpenFlow event handler class
        """

        # If you hit this you might want to increase
        # the "miss_send_length" of your switch
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug("packet truncated: only %s of %s bytes",
                              ev.msg.msg_len, ev.msg.total_len)

        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Get the in_port from the ev.msg object.
        # Options available for OF 1.3 at https://goo.gl/qwxpaU
        in_port = msg.match['in_port']

        # Analyse the received packets using the packet library
        # Extract MAC addresses (src, dst)
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return
        dst = eth.dst
        src = eth.src

        # Get Datapach ID to identify OpenFlow switches.
        # The setdefault() dictionary method returns the value of the key (dpid)
        # if it exists. If the the key does not exist, it adds the key (dpid)
        # with an empty dictionary as value.
        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        # Log
        self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

        # Learn the MAC to avoid flooding next time
        # The next line associates a source MAC (src) to a port (in_port) for
        # the switch the PacketIn came from.
        self.mac_to_port[dpid][src] = in_port

        # If the controller already has the destination MAC address in its table
        # (mac_to_port dictionary), it takes the out port from there. If not, it
        # sets all ports as the out port.
        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        # Create the action list. Set out port as the only action for matching
        # packets.
        actions = [parser.OFPActionOutput(out_port)]

        # If controller knows the destination MAC, it installs a flow entry to
        # process new packets with the same source and destination MAC.
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
            # verify if we have a valid buffer_id, if yes avoid to send both
            # flow_mod & packet_out
            if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                self.add_flow(datapath, 1, match, actions, msg.buffer_id)
                return
            else:
                self.add_flow(datapath, 1, match, actions)
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        # PacketOut
        # Now the controller process the packet that generated the PacketIn
        # through a PacketOut message. If the destination MAC is known, the
        # switch sends the packet through the port where the destination MAC
        # comes; else the switch floods the packet to all ports.
        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)

        # send packet out
        datapath.send_msg(out)
