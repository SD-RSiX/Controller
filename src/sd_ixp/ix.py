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

from . import location
from . import ofswitch

class IX:
    """ IX class is an abstraction of the entire SD Internet Exchange.

    Objects of this class hold all the information of an IXP.
    This is the only one interface to the entire SD infrastructure.

    Attributes:
        name (str): unique name the identifies the IXP
    """

    def __init__(self, name):
        self.name = name

        # TODO: An IX must object will be created with only a unique name, all
        #       other data will be retrieved from database.

        self._locations = {}
