# Code and explanations from
# https://osrg.github.io/ryu-book/en/html/switching_hub.html

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet


class ExampleSwitch13(app_manager.RyuApp):
    """OpenFlow 1.3 learning switch
    A Ryu application inherits from ryu.base.app_manager that manages OpenFlow
    operations.
    """

    ###### OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    def __init__(self, *args, **kwargs):
        super(ExampleSwitch13, self).__init__(*args, **kwargs)
        # Initiates a dictionary to keep MAC port mapping
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
        actions = [
            parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                   ofproto.OFPCML_NO_BUFFER)
        ]

        # PacketOut:
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

        # create a flow_mod message and send it out
        inst = [
            parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)
        ]
        mod = parser.OFPFlowMod(
            datapath=datapath,
            priority=priority,
            match=match,
            instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        """PacketIn handler

        Handle PacketIns sent by switches to the controller. Switches use
        table-miss entry to communicate to the controller.

        Args:
            ev (ev): instance of the OpenFlow event handler class
        """

        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # get Datapach ID to identify OpenFlow switches
        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        # analyse the received packets using the packet library
        pkt = packet.Packet(msg.data)
        eth_pkt = pkt.get_protocol(ethernet.ethernet)
        dst = eth_pkt.dst
        src = eth_pkt.src

        # get the received port number from the PacketIn message
        in_port = msg.match['in_port']

        self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

        # learn a MAC address to avoid FLOOD next time
        self.mac_to_port[dpid][src] = in_port

        # if the destination MAC address is already learned, decide which port
        # to output the packet, otherwise flood it.
        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        # create the action list
        actions = [parser.OFPActionOutput(out_port)]

        # install a flow entry to avoid packet_in next time.
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst)
            self.add_flow(datapath, 1, match, actions)

        # construct packet_out message and send it.
        out = parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=ofproto.OFP_NO_BUFFER,
            in_port=in_port,
            actions=actions,
            data=msg.data)
        datapath.send_msg(out)
