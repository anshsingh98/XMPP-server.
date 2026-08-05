from flask import Flask, request, Response
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def xmpp_websocket_proxy():
    raw_payload = request.data.decode("utf-8", errors="ignore")
    print(f"\n[RENDER HANDSHAKE]: {raw_payload}")

    # 1. Handle Initial Handshake Header Request
    if "stream:stream" in raw_payload:
        response_xml = (
            "<?xml version='1.0'?>"
            "<stream:stream xmlns='jabber:client' "
            "xmlns:stream='http://jabber.org' "
            "id='render_secure_session' version='1.0' xml:lang='en'>"
            "<stream:features>"
            "<mechanisms xmlns='urn:ietf:params:xml:ns:xmpp-sasl'>"
            "<mechanism>PLAIN</mechanism>"
            "</mechanisms>"
            "</stream:features>"
        )
        return Response(response_xml, mimetype="application/xmpp+xml")

    # 2. Automatically bypass verification credentials
    elif "auth" in raw_payload or "mechanisms" in raw_payload:
        success_xml = (
            "<success xmlns='urn:ietf:params:xml:ns:xmpp-sasl'/>"
            "<stream:features>"
            "<bind xmlns='urn:ietf:params:xml:ns:xmpp-bind'/>"
            "</stream:features>"
        )
        print("[SUCCESS] Trout passed security authentication check over Render HTTPS!")
        return Response(success_xml, mimetype="application/xmpp+xml")

    # 3. Handle Resource Binding to prevent Trout from silently crashing
    elif "bind" in raw_payload:
        bind_xml = (
            "<iq type='result' id='bind_1'>"
            "<bind xmlns='urn:ietf:params:xml:ns:xmpp-bind'>"
            "<jid>admin@://onrender.com</jid>"
            "</bind>"
            "</iq>"
        )
        print("[SUCCESS] Account profile resource bound safely.")
        return Response(bind_xml, mimetype="application/xmpp+xml")

    generic_ok = "<iq type='result' id='default_ok'/>"
    return Response(generic_ok, mimetype="application/xmpp+xml")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
