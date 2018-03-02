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

from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types


def discovery_handler(eth_pkt):
    """

    Args:
        pkt (packet.Packet(msg.data)): packet object containing layer 2 data
    """

    # ICMPv6
    #
    # ethernet(dst='33:33:ff:00:00:01', ethertype=34525, src='00:50:79:66:68:01')
    # ipv6(
    #     dst='ff02::1:ff00:1',
    #     ext_hdrs=[],
    #     flow_label=0,
    #     hop_limit=255,
    #     nxt=58,
    #     payload_length=32,
    #     src='2001:db8::4',
    #     traffic_class=0,
    #     version=6)
    # icmpv6(
    #     code=0,
    #     csum=15471,
    #     data=nd_neighbor(
    #         dst='2001:db8::1',
    #         option=nd_option_sla(
    #             data=None, hw_src='00:50:79:66:68:01', length=1),
    #         res=0),
    #     type_=135)


    # print('-' * 80)
    #
    # if eth_pkt.ethertype == ether_types.ETH_TYPE_ARP:
    #     print("ARP")
    # elif eth_pkt.ethertype == ether_types.ETH_TYPE_IPV6:
    #
    #
    #
    # print('-' * 80)


def lldp_handler(llpd_packet):
    pass
