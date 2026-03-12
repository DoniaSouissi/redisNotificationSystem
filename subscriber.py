import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def listen_for_notifications(user_id):
    pubsub = r.pubsub()
    channel = f"alerts:{user_id}"
    
    # Subscribe to the user's channel
    pubsub.subscribe(channel)
    print(f"User {user_id} is waiting for real-time notifications...")
    
    for message in pubsub.listen():
        if message['type'] == 'message':
            print(f"REAL-TIME ALERT: {message['data']}")

if __name__ == "__main__":
    # Simulating student St001 listening for notifications
    listen_for_notifications("St001")