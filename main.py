from flask import Flask, request, Response
import os

app = Flask(__name__)

# Complete structural configuration mapping to satisfy Trout's startup checks
@app.route("/", methods=["GET", "POST"])
def xmpp_bridge_gateway():
    # Force read the raw stream data sent by the phone
    raw_payload = request.data.decode("utf-8", errors="ignore")
    print(f"\n[INCOMING DATA]:\n{raw_payload}")

    # 1. Handle Initial Connection Handshake Stream
    if "stream:stream" in raw_payload:
        response_xml = (
            "<?xml version='1.0'?>"
            "<stream:stream xmlns='jabber:client' "
            "xmlns:stream='http://jabber.org' "
            "id='secure_cloud_bridge_999' version='1.0' xml:lang='en'>"
            "<stream:features>"
            "<mechanisms xmlns='urn:ietf:params:xml:ns:xmpp-sasl'>"
            "<mechanism>PLAIN</mechanism>"
            "</mechanisms>"
            "</stream:features>"
        )
        return Response(response_xml, mimetype="text/xml")

    # 2. Handle Text Authentication Verification Requests
    elif "<auth" in raw_payload:
        # Send instant verification pass and append the next mandatory stream features block
        success_xml = (
            "<success xmlns='urn:ietf:params:xml:ns:xmpp-sasl'/>"
            "<stream:features>"
            "<bind xmlns='urn:ietf:params:xml:ns:xmpp-bind'/>"
            "<session xmlns='urn:ietf:params:xml:ns:xmpp-session'/>"
            "</stream:features>"
        )
        print("[SUCCESS] Trout passed security authentication check!")
        return Response(success_xml, mimetype="text/xml")

    # 3. Handle Resource Binding (Crucial to prevent silent crashes)
    elif "bind" in raw_payload:
        bind_xml = (
            "<iq type='result' id='bind_1'>"
            "<bind xmlns='urn:ietf:params:xml:ns:xmpp-bind'>"
            "<jid>admin@://onrender.com</jid>"
            "</bind>"
            "</iq>"
        )
        print("[SUCCESS] Account profile resource binding bound safely.")
        return Response(bind_xml, mimetype="text/xml")

    # 4. Handle Empty Roster Requests (Fills the dashboard menus smoothly)
    elif "jabber:iq:roster" in raw_payload:
        roster_xml = (
            "<iq type='result' id='roster_1' to='admin@://onrender.com'>"
            "<query xmlns='jabber:iq:roster'/>"
            "</iq>"
        )
        print("[SUCCESS] Fed Trout client an empty database roster profile.")
        return Response(roster_xml, mimetype="text/xml")

    # Catch-all placeholder response for generic profile queries to keep the background running safely
    generic_ok = "<iq type='result' id='default_ok'/>"
    return Response(generic_ok, mimetype="text/xml")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
