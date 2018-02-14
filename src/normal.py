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
# (https://github.com/osrg/ryu/blob/master/ryu/app/example_switch_13.py). It now
# installs the NORMAL flow entry on every switch that connects to the
# controller.
#

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3, ofproto_v1_4, ofproto_v1_5


class LearningSwitch(app_manager.RyuApp):
    """OpenFlow learning switch

    A Ryu application inherits from ryu.base.app_manager that manages OpenFlow
    operations.
    """

    # A list of supported OpenFlow versions for this RyuApp. The default is all
    # versions supported by the framework.
    OFP_VERSIONS = [
        ofproto_v1_3.OFP_VERSION, ofproto_v1_4.OFP_VERSION,
        ofproto_v1_5.OFP_VERSION
    ]

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

        # Create an instance of OFPActionOutput class to set the flow-entry's
        # action as NORMAL, this way the switch will forward every packet as a
        # normal L2 switch without generation PacketIn.
        actions = [
            parser.OFPActionOutput(ofproto.OFPP_NORMAL,
                                   ofproto.OFPCML_NO_BUFFER)
        ]

        self.logger.info("Configuring SW %s with NORMAL flow entry.", datapath.id)

        # PacketOut
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions):
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
        inst = [
            parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)
        ]

        # Create the flow mod message
        mod = parser.OFPFlowMod(
            datapath=datapath,
            priority=priority,
            match=match,
            instructions=inst)

        datapath.send_msg(mod)
