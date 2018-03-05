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
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types


def discovery_handler(msg):
    """

    Args:
        msg (ev.msg):
    """
    pkt = packet.Packet(msg.data)

    dst_MAC = pkt.get_protocols(ethernet.ethernet)[0].dst
    src_MAC = pkt.get_protocols(ethernet.ethernet)[0].src


def lldp_handler(llpd_packet):
    pass
