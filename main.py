from flask import Flask, request, Response
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def xmpp_stream_initiation():
    print("[CLOUD LOG] Trout scanned the secure proxy gateway.")
    # Feeds Trout a secure XML stream header through the HTTPS payload
    stream_payload = (
        "<?xml version='1.0'?>"
        "<stream:stream xmlns='jabber:client' "
        "xmlns:stream='http://jabber.org' "
        "id='secure_cloud_bridge_777' version='1.0' xml:lang='en'>"
    )
    return Response(stream_payload, mimetype="text/xml")

@app.route("/", methods=["POST"])
def xmpp_data_interceptor():
    raw_payload = request.data.decode("utf-8", errors="ignore")
    print(f"\n[CLOUD CAPTURED RAW TRAFFIC]:\n{raw_payload}\n")
    
    # Auto-approve accounts or mechanisms
    if "stream:stream" in raw_payload or "mechanisms" in raw_payload:
        auth_features = (
            "<stream:features>"
            "<mechanisms xmlns='urn:ietf:params:xml:ns:xmpp-sasl'>"
            "<mechanism>PLAIN</mechanism>"
            "</mechanisms>"
            "</stream:features>"
        )
        return Response(auth_features, mimetype="text/xml")
        
    elif "auth" in raw_payload:
        success_response = "<success xmlns='urn:ietf:params:xml:ns:xmpp-sasl'/>"
        print("[SUCCESS] Trout authentication verified on the cloud endpoint.")
        return Response(success_response, mimetype="text/xml")
        
    return Response("", status=200)

if __name__ == "__main__":
    # Binds to the dynamic environment port provided by Render for zero-cost deployment
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
