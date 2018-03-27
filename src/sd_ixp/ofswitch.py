# Copyright (C) 2018 [SD]RSiX Project
#
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ryu.controller import ofp_event
from ryu.ofproto import ofproto_v1_3


class OFSwitch:
    """OpenFlow switches abstraction.

    Objects of this class store a set of information about devices connected to
    the controller. OpenFlow events will update switch objects so that to keep
    it consistent with network status.

    Attributes:
        _datapath (ev.msg.datapath): connections between controller and OFswitch
        _of_version (ev.msg.datapath.ofproto.OFP_VERSION): OpenFlow version
        _ports (dictionary): Maps ports to what is connected to it (AS or
            another IXP's switch)
    """

    def __init__(self, datapath):

        # Initialize the MAC-port-VLAN dictionary mapping
        self._ports = {}

        # TODO(lucas): When a new switch connects,

        self._datapath = datapath
        self._of_version = self._datapath.ofproto.OFP_VERSION

        self._table_miss()

    def _table_miss(self):
        """Install table-miss flow entry

        Table-miss flow entry configures the switch to forward unmatched packets
        to the controller.
        """

        # ofproto module that supports the OpenFlow version in use
        ofproto = self._datapath.ofproto

        # ofproto_parser module
        parser = self._datapath.ofproto_parser

        # create an empty match to match every packet
        match = parser.OFPMatch()

        # create an instance of OFPActionOutput class setting controller as the
        # output port.
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER)]

        # and NO_BUFFER, so that the switch will not buffer the
        # the packets that generate a PacketIn
        # actions = [
        #     parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
        #                            ofproto.OFPCML_NO_BUFFER)
        # ]

        # Instructions are executed when a packet matches a flow entry; it
        # differs from the actions lists that the switch executes at the end of
        # the processing.
        # Using "ofproto.OFPIT_APPLY_ACTIONS" parameter, the controller informs
        # the switch to run the action list in that very same processing stage.
        instructions = [
            parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)
        ]

        self.add_flow(0, match, instructions, actions)

    def add_flow(self, priority, match, instructions, actions, buffer_id=None):
        """ Install a flow mod on the switch

        Args:
            priority (int): the priority the flow entry must be given
            match (OFPMatch): match object the packets must match to this entry
                    be applied
            instructions (OFPInstructionActions): configure the action set or
                    pipeline processing
            action: action the switch will perform with the packet when a match
                    occurs
            buffer_id (default=None): id of the packet buffered at the switch.
                    When there is no buffered packet associated buffer_id must
                    be set to OFP_NO_BUFFER in the flow_mod.
        """

        parser = self._datapath.ofproto_parser

        # Create the flow mod message
        if buffer_id:
            mod = parser.OFPFlowMod(
                datapath=self._datapath,
                buffer_id=buffer_id,
                priority=priority,
                match=match,
                instructions=instructions)
        else:
            mod = parser.OFPFlowMod(
                datapath=self._datapath,
                priority=priority,
                match=match,
                instructions=instructions)

        self._datapath.send_msg(mod)

    def l2_learning(self, msg):
        """ Layer 2 learning feature

        Learn MAC addresses
        """
        pass

    def get_flow_entries(self):
        pass
