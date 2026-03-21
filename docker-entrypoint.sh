#!/bin/bash

# Function to wait for MySQL to be ready
function wait_for_mysql() {
    echo "Waiting for MySQL to be ready..."
    while ! python -c "import socket; s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.connect(('db', 3306))" > /dev/null 2>&1; do
        sleep 1
    done
    echo "MySQL is ready!"
}

# Wait for MySQL
wait_for_mysql

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Load initial data if present (hospital_data.json)
if [ -f "hospital_data.json" ]; then
    echo "Loading hospital data from JSON..."
    python manage.py loaddata hospital_data.json
else
    echo "No hospital_data.json found. Skipping data load."
fi

# Execute the main command (from docker-compose)
exec "$@"
