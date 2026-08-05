from flask import Flask, request, Response
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def xmpp_raw_stream_gateway():
    # Force read raw input data blocks bypassing web server definitions
    raw_payload = request.data.decode("utf-8", errors="ignore")
    print(f"\n[INCOMING STREAM PACKET]: {raw_payload}")

    # 1. Handle Initial Handshake Header Request
    if "stream:stream" in raw_payload:
        stream_init = (
            "<?xml version='1.0'?>"
            "<stream:stream xmlns='jabber:client' "
            "xmlns:stream='http://jabber.org' "
            "id='render_bypass_session_000' version='1.0' xml:lang='en'>"
            "<stream:features>"
            "<mechanisms xmlns='urn:ietf:params:xml:ns:xmpp-sasl'>"
            "<mechanism>PLAIN</mechanism>"
            "</mechanisms>"
            "</stream:features>"
        )
        # Bypasses Flask's web engine and outputs raw data bytes directly into the interface port
        return Response(stream_init, mimetype="text/plain")

    # 2. Bypasses authentication check and injects profile structural features
    elif "auth" in raw_payload or "mechanisms" in raw_payload:
        success_payload = (
            "<success xmlns='urn:ietf:params:xml:ns:xmpp-sasl'/>"
            "<stream:features>"
            "<bind xmlns='urn:ietf:params:xml:ns:xmpp-bind'/>"
            "</stream:features>"
        )
        print("[SUCCESS] Trout passed security authentication checks over the cloud!")
        return Response(success_payload, mimetype="text/plain")

    # 3. Handle Resource Binding to prevent Trout from silently crashing after logging in
    elif "bind" in raw_payload:
        bind_xml = (
            "<iq type='result' id='bind_1'>"
            "<bind xmlns='urn:ietf:params:xml:ns:xmpp-bind'>"
            "<jid>admin@://onrender.com</jid>"
            "</bind>"
            "</iq>"
        )
        print("[SUCCESS] Structural account profile layer bound safely.")
        return Response(bind_xml, mimetype="text/plain")

    return Response("<iq type='result' id='ok'/>", mimetype="text/plain")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
