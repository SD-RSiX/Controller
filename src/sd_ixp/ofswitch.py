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


# from ryu.controller import ofp_event
# from ryu.controller.handler import set_ev_cls
# from ryu.ofproto import *


class Switch:
    """docstring for Switch.
    """

    def __init__(self, datapath_id):
        self._datapath_id = datapath_id

    # def _packet_out(self, arg):
    #
    # def add_flow(self, arg):
    #
    # def del_flow(self, arg):
