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


def mac_from_datapath_id(datapath_id):
        """ Extract the MAC address from the datapath ID.

        The last 48 bits of the datapath ID are taken from the MAC address.
        Ryu provides the datapath ID in decimal format.

        Args:
            datapath_id: Ryu's datapath.id in decimal format

        Returns:
            MAC: String object containing the MAC address in xx:xx:xx:xx:xx:xx
                 format.
        """

    hex_converted = str(hex(datapath_id)[-12:])
    MAC = str()

    start = 0
    end = 2

    while end <= 10:
        MAC += hex_converted[start:end] + ":"
        start = end
        end += 2

    MAC += hex_converted[start:end]

    return MAC
