import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def view_history(user_id):
    print(f"--- History for {user_id} ---")
    history_key = f"history:{user_id}"
    
    # Retrieve recent notifications using Redis Lists (LRANGE)
    # Limiting to last 100 notifications (index 0 to 99)
    recent_keys = r.lrange(history_key, 0, 99)
    
    for key in recent_keys:
        if r.exists(key):
            notif_data = r.hgetall(key)
            print(f"Key: {key} -> {notif_data}")
        else:
            print(f"Key: {key} -> (Expired)")

def view_analytics():
    print("\n--- Real-Time Analytics ---")
    types = ["order_update", "message", "system_alert"]
    for t in types:
        count = r.get(f"analytics:{t}")
        if count:
            print(f"{t}: {count} notifications")

if __name__ == "__main__":
    view_history("client1")
    view_analytics()