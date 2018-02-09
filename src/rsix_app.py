from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3, ofproto_v1_4, ofproto_v1_5
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet


class SD_RSiX(app_manager.RyuApp):
    """SD_RSiX main file.

    Large explanation...
    """

    # Supported OpenFlow versions
    OFP_VERSIONS = [
        ofproto_v1_3.OFP_VERSION, ofproto_v1_4.OFP_VERSION,
        ofproto_v1_5.OFP_VERSION
    ]

    def __init__(self, *args, **kwargs):
        super(SD_RSiX, self).__init__(*args, **kwargs)


    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        """PacketIn handler

        Handle PacketIns sent by switches to the controller. Switches use
        table-miss entry to communicate to the controller.

        Args:
            ev (ev): instance of the OpenFlow event handler class
        """
