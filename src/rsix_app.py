# Copyright (C) 2018 [SD]RSiX Project
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

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.lib.packet import icmpv6

from sd_ixp.ofswitch import Switch
from sd_ixp import neighbor

import array


class SD_RSiX(app_manager.RyuApp):
    """OpenFlow learning switch

    A Ryu application inherits from ryu.base.app_manager that manages OpenFlow
    operations.
    """

    # A list of supported OpenFlow versions for this RyuApp. The default is all
    # versions supported by the framework.
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SD_RSiX, self).__init__(*args, **kwargs)

        # Initiates a dictionary to store switch objects
        # Structure:
        #       { datapath_id, Switch }
        self.switches = {}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_up(self, ev):
        """Install table-miss flow entry

        When a switch connects, the controller requests the switch features; the
        features reply triggers this function, so the controller installs the
        table-miss entry the switch will use to send PacketIn messages.

        Args:
            ev (ev): instance of the OpenFlow event handler class
        """

        self.switches[ev.msg.datapath.id] = Switch(ev.msg.datapath)

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

        #pkt = packet.Packet(ev.msg.data)
        eth = packet.Packet(ev.msg.data).get_protocols(ethernet.ethernet)[0]

        if eth.ethertype == ether_types.ETH_TYPE_ARP:
            neighbor.discovery_handler(ev.msg)

        if eth.ethertype == ether_types.ETH_TYPE_IPV6:
            for p in pkt.protocols:
                if p.protocol_name == 'icmpv6' and (p.type_ == 135 or
                                                    p.type_ == 136):
                    neighbor.discovery_handler(ev.msg)
