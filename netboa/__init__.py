#------------------------------------------------------------------------------
#   netboa/__init__.py
#   Copyright 2011 Jim Storch
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain a
#   copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#------------------------------------------------------------------------------

import sys

if sys.platform == 'linux2':
    from netboa.tcp.epoll_server import EpollServer as Server
else:
    from netboa.tcp.select_server import SelectServer as Server

if sys.version_info[0] >= 3:
    from netboa.compat import str_to_bytes_python3 as str_to_bytes
    from netboa.compat import bytes_to_str_python3 as bytes_to_str
else:
    from netboa.compat import str_to_bytes_python2 as str_to_bytes
    from netboa.compat import bytes_to_str_python2 as bytes_to_str

from netboa.service import Service
