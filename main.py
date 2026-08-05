from flask import Flask, request, Response
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def xmpp_bosh_gateway():
    # Capture raw packet stream
    raw_payload = request.data.decode("utf-8", errors="ignore")
    print(f"\n[INCOMING CORE TRAFFIC]: {raw_payload}")

    # 1. Standard Web Browser Check (Bypasses initial connection errors)
    if request.method == "GET" and not raw_payload:
        return "XMPP BOSH Gateway Live", 200

    # 2. Match Stream Initiation Block
    if "stream:stream" in raw_payload or "<body" in raw_payload:
        response_body = (
            "<body xmlns='http://jabber.org' "
            "sid='render_secure_proxy_session' authid='12345' "
            "requests='2' inactivity='30' polling='5' requests='2' hold='1'>"
            "<stream:features xmlns:stream='http://jabber.org'>"
            "<mechanisms xmlns='urn:ietf:params:xml:ns:xmpp-sasl'>"
            "<mechanism>PLAIN</mechanism>"
            "</mechanisms>"
            "<bind xmlns='urn:ietf:params:xml:ns:xmpp-bind'/>"
            "</stream:features>"
            "</body>"
        )
        # Returns application/xml to perfectly satisfy Trout's backend parser
        return Response(response_body, mimetype="application/xml")

    # 3. Intercept Authentication Step and Auto-Approve the Session
    elif "auth" in raw_payload:
        auth_success = (
            "<body xmlns='http://jabber.org'>"
            "<success xmlns='urn:ietf:params:xml:ns:xmpp-sasl'/>"
            "</body>"
        )
        print("[SUCCESS] Trout passed security authentication check via Render BOSH!")
        return Response(auth_success, mimetype="application/xml")

    # 4. Bind Account Profile Layout to prevent the app from closing down
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
        print("[SUCCESS] App interface profile channel bound successfully.")
        return Response(bind_ok, mimetype="application/xml")

    # Catch-all empty layout binder
    empty_body = "<body xmlns='http://jabber.org'><iq type='result' id='default_ok'/></body>"
    return Response(empty_body, mimetype="application/xml")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
