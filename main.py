from flask import Flask, request, Response
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def xmpp_stable_bosh_gateway():
    raw_payload = request.data.decode("utf-8", errors="ignore")
    print(f"\n[TROUT INCOMING PACKET]: {raw_payload}")

    # Standard browser baseline
    if request.method == "GET" and not raw_payload:
        return "Secure XMPP Cloud BOSH Gateway Active", 200

    # 1. Handle Core Stream Handshake Invitation
    if "stream:stream" in raw_payload or "<body" in raw_payload and "auth" not in raw_payload and "bind" not in raw_payload and "iq" not in raw_payload:
        init_body = (
            "<body xmlns='http://jabber.org' sid='render_secure_session_xyz' authid='abc777' inactivity='30' polling='5' requests='2' hold='1'>"
            "<stream:features xmlns:stream='http://jabber.org'>"
            "<mechanisms xmlns='urn:ietf:params:xml:ns:xmpp-sasl'><mechanism>PLAIN</mechanism></mechanisms>"
            "<bind xmlns='urn:ietf:params:xml:ns:xmpp-bind'/>"
            "<session xmlns='urn:ietf:params:xml:ns:xmpp-session'/>"
            "</stream:features>"
            "</body>"
        )
        return Response(init_body, mimetype="application/xml")

    # 2. Intercept and Auto-Approve Verification Login
    elif "auth" in raw_payload:
        auth_ok = (
            "<body xmlns='http://jabber.org'>"
            "<success xmlns='urn:ietf:params:xml:ns:xmpp-sasl'/>"
            "</body>"
        )
        print("[SUCCESS] Trout passed credential checks.")
        return Response(auth_ok, mimetype="application/xml")

    # 3. Handle Profile Resource Binding (Crucial to prevent the 3-second thread crash)
    elif "bind" in raw_payload:
        bind_ok = (
            "<body xmlns='http://jabber.org'>"
            "<iq type='result' id='bind_1'>"
            "<bind xmlns='urn:ietf:params:xml:ns:xmpp-bind'>"
            "<jid>admin@://onrender.com</jid>"
            "</bind>"
            "</iq>"
            "</body>"
        )
        print("[SUCCESS] Profile session channel bound smoothly.")
        return Response(bind_ok, mimetype="application/xml")

    # 4. Handle Roster / Contact Queries (Fills the app main layout cleanly)
    elif "jabber:iq:roster" in raw_payload:
        roster_ok = (
            "<body xmlns='http://jabber.org'>"
            "<iq type='result' id='roster_query_1' to='admin@://onrender.com'>"
            "<query xmlns='jabber:iq:roster'>"
            # We inject 1 dummy contact entry so the app's structural visual code doesn't register an empty database crash
            "<item jid='friend@://onrender.com' name='Test Developer' subscription='both'/>"
            "</query>"
            "</iq>"
            "</body>"
        )
        print("[SUCCESS] Injected dummy UI database contact row.")
        return Response(roster_ok, mimetype="application/xml")

    # 5. Handle vCard / Profile Metadata Parsing
    elif "vcard-temp" in raw_payload or "vCard" in raw_payload:
        vcard_ok = (
            "<body xmlns='http://jabber.org'>"
            "<iq type='result' id='vcard_1'>"
            "<vCard xmlns='vcard-temp'>"
            "<FN>Admin User</FN>"
            "<NICKNAME>Localhost Operator</NICKNAME>"
            "</vCard>"
            "</iq>"
            "</body>"
        )
        print("[SUCCESS] Supplied local account profile identities.")
        return Response(vcard_ok, mimetype="application/xml")

    # Catch-all empty element wrap to ensure background tracking loops don't hang
    generic_body = "<body xmlns='http://jabber.org'><iq type='result' id='default_ack'/></body>"
    return Response(generic_body, mimetype="application/xml")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
