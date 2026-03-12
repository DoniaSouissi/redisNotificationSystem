import redis
import time

# Connect to the Redis container on localhost
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def send_notification(user_id, notif_type, message):
    timestamp = int(time.time())
    
    # 1. Add Notifications (Streams)
    # Appends notifications as a log of events
    stream_key = f"notification_log:{user_id}"
    r.xadd(stream_key, {"type": notif_type, "message": message, "timestamp": str(timestamp)})
    
    # 2. Notification History (Lists) & 4. Automatic Expiration
    # Stores specific notification key and sets a 24-hour TTL (86400 seconds)
    notif_key = f"notification:{user_id}:{timestamp}"
    r.hset(notif_key, mapping={"type": notif_type, "message": message})
    r.expire(notif_key, 86400) 
    
    # Maintain history using Lists
    history_key = f"history:{user_id}"
    r.lpush(history_key, notif_key)
    
    # 5. Real-Time Analytics
    # Use a Counter to monitor the number of notifications by type
    r.incr(f"analytics:{notif_type}")
    
    # 3. Real-Time Subscription
    # Publish to a user-specific channel
    channel = f"alerts:{user_id}"
    r.publish(channel, f"[{notif_type}] {message}")
    print(f"Notification sent to {user_id}!")

# Example usage
if __name__ == "__main__":
    send_notification("St001", "order_update", "Your order has shipped!")
    send_notification("St001", "message", "You have a new message from Yann.")
    send_notification("St002", "system_alert", "Scheduled maintenance in 1 hour.")