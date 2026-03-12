# Real-Time Notification System (Redis + Python)

A robust, real-time notification system built with Python and Redis. This project demonstrates core Redis data structures and paradigms to handle event logging, real-time pub/sub messaging, limited history tracking, auto-expiring keys, and analytics. 

## ✨ Bonus Features: Web UI & Docker Containerization
While the core requirements of this project were met using Python CLI scripts, **I built a fully functional Web Interface and fully containerized the application using Docker** as added bonuses to make the project production-ready and visually accessible.

* **Web Dashboard:** Powered by **Flask** and uses **Server-Sent Events (SSE)** to stream Redis Pub/Sub messages directly to the browser, updating the UI in real-time without refreshing.
* **Docker Compose:** The entire environment (Redis database + Web application) can be spun up seamlessly using a single Docker Compose command.

## 🚀 Core Features & Project Requirements

This system strictly adheres to the 5 project requirements:

### 1. Add Notifications (Redis Hashes & Streams)
When a notification is generated, the system stores the specific payload using Redis Hashes (`HSET`) under the key format `notification:<user_id>:<timestamp>`. Additionally, it leverages Redis Streams (`XADD`) to append every notification into an immutable, chronological log of events.

### 2. Real-Time Subscription (Redis Pub/Sub)
The system uses Redis Pub/Sub to push notifications to active users instantly. 
* **CLI:** The `subscriber.py` script listens to the user's specific channel.
* **Web:** `app.py` yields the Pub/Sub messages to the frontend via an SSE endpoint, creating a live connection.

### 3. Notification History (Redis Lists)
To maintain a limited history of notifications for each user, the system uses Redis Lists. It uses `LPUSH` to add new notification keys to the user's history and strictly caps the list at the 100 most recent items using `LTRIM`. The history can be fetched at any time using `LRANGE`.

### 4. Automatic Expiration (Redis TTL)
Notifications shouldn't live in the database forever. Using Redis's Time-to-Live (TTL) feature via the `EXPIRE` command, every specific notification hash is set to automatically delete itself after 24 hours (86400 seconds). The frontend and history retrievers gracefully handle keys that have expired.

### 5. Real-Time Analytics (Redis Counters)
The system tracks the volume of notifications by type (e.g., `order_update`, `message`). It uses Redis atomic counters (`INCR`) to monitor how many of each notification type have been sent globally across the application.

## 🛠️ Installation & Usage

To run this real-time notification system and web application:

**Clone the repository:**
```bash
git clone https://github.com/YourUsername/redisNotificationSystem.git
cd redisNotificationSystem
```

**Build and run the environment:**
Docker Compose will automatically install all dependencies, configure the network, and start both the Redis database and the Flask web server.
```bash
docker compose up --build
```

## 📂 Project Structure

```text
├── webVersion/
│   ├── templates/
│   │   └── index.html      # The bonus web UI (HTML/CSS/JS)
│   └── app.py              # Flask server handling web endpoints & SSE
├── Dockerfile              # Docker instructions for the Flask app
├── docker-compose.yml      # Conductor for Redis & Web app services
├── requirements.txt        # Python dependencies
├── dashboard.py            # CLI script to view a user's history & analytics
├── publisher.py            # CLI script to simulate sending notifications
└── subscriber.py           # CLI script to simulate a user listening
