/*-----------------------------------------------------------------------------
#   ws_test.js
#   Copyright 2011 Jim Storch
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain a
#   copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
-----------------------------------------------------------------------------*/

var websocket = new WebSocket("ws://localhost:7778");

websocket.onopen = function ()
    {
    console.log("WebSocket.onopen");
    $('<H2>').append("WebSocket Connection Established").appendTo('body')
    //$('<img>', {src:'images/skull.png'}).appendTo('body');
    };

websocket.onmessage = function (evt) {
    console.log(evt.data);
    var el = $('<p>');
    el.append(evt.data);
    el.addClass('chatbox');
    el.appendTo('body');
    if ( $('p').size() > 10 ) {
        $('p:first').remove();
        }
    };

websocket.onclose = function() {
    console.log("WebSocket.onclose");
    $('<H2>').append("WebSocket Connection Lost").appendTo('body')
    };

websocket.onerror = function (evt) {
    console.log('Error occured: ' + evt.data);
    $('<H2>').append("WebSocket Error: " + evt.data).appendTo('body')
    }

