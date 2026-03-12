from flask import Flask, render_template, request, jsonify, Response
import redis
import time
import json
import os

app = Flask(__name__)

# Grab host and port from environment variables (set by docker-compose), with defaults for local development
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6380))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

@app.route('/')
def index():
    # Serves the HTML interface
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_notification():
    data = request.json
    user_id = data.get('user_id')
    notif_type = data.get('notif_type')
    message = data.get('message')
    timestamp = int(time.time())

    # 1. Add Notifications (Streams)
    stream_key = f"notification_log:{user_id}"
    r.xadd(stream_key, {"type": notif_type, "message": message, "timestamp": str(timestamp)})
    
    # 2. Notification History & Expiration (Lists & TTL)
    notif_key = f"notification:{user_id}:{timestamp}"
    r.hset(notif_key, mapping={"type": notif_type, "message": message})
    r.expire(notif_key, 86400) # 24 hours
    
    history_key = f"history:{user_id}"
    r.lpush(history_key, notif_key)
    r.ltrim(history_key, 0, 99)
    
    # 3. Real-Time Analytics (Counters)
    r.incr(f"analytics:{notif_type}")
    
    # 4. Real-Time Subscription (Pub/Sub)
    channel = f"alerts:{user_id}"
    # Send as JSON so the frontend can parse it easily
    payload = json.dumps({"type": notif_type, "message": message, "timestamp": timestamp})
    r.publish(channel, payload)
    
    return jsonify({"status": "success", "message": "Notification sent!"})

@app.route('/history/<user_id>')
def history(user_id):
    history_key = f"history:{user_id}"
    recent_keys = r.lrange(history_key, 0, 99)
    history_data = []
    
    for key in recent_keys:
        if r.exists(key):
            history_data.append(r.hgetall(key))
            
    return jsonify(history_data)

@app.route('/analytics')
def analytics():
    keys = r.keys("analytics:*")
    data = {}
    for key in keys:
        notif_type = key.split(":")[1]
        data[notif_type] = r.get(key)
    return jsonify(data)

@app.route('/stream/<user_id>')
def stream(user_id):
    # This is an SSE (Server-Sent Events) endpoint.
    # It keeps an open connection to the browser and yields Pub/Sub messages.
    def event_stream():
        pubsub = r.pubsub()
        pubsub.subscribe(f"alerts:{user_id}")
        for message in pubsub.listen():
            if message['type'] == 'message':
                # Format required for Server-Sent Events
                yield f"data: {message['data']}\n\n"
                
    return Response(event_stream(), mimetype="text/event-stream")

if __name__ == '__main__':
    # Run the web server on port 5000
    app.run(debug=True, host='0.0.0.0', port=5000)