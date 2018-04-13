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

import binascii

def mac_from_datapath_id(datapath_id):
    """

    """
    binary = bin(datapath_id)[-48:]

    print(binary)

    MAC = str()
    start = 0
    end = 4
    column_counter = 0

    while end <= 48:
        MAC += hex( int( binary[start:end], 2 ) )[-1:]
        start += 4
        end += 4
        column_counter += 1

        if (column_counter % 2) == 0 and len(MAC) < 15:
            MAC += ':'

    return MAC


print("Output: {}".format(mac_from_datapath_id(10111104338072038465)))
