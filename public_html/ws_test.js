//-----------------------------------------------------------------------------
//      ws_test.js
//      Copyright Jim Storch 2011    
//-----------------------------------------------------------------------------

var ws = new WebSocket("ws://127.0.0.1:7778");

ws.onopen = function ()
    {
    ws.send("CONNECTED");
    };

ws.onmessage = function (evt)
    {
    alert(evt.data);
    };

ws.onclose = function()
    {
    };
