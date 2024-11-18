from datetime import datetime, timedelta
import time
from plyer import notification  # Install using `pip install plyer`

# Function to set a reminder
def set_reminder(reminder_type, reminder_time):
    current_time = datetime.now()
    reminder_time = datetime.strptime(reminder_time, "%Y-%m-%d %H:%M:%S")

    # Wait until the reminder time
    while current_time < reminder_time:
        time.sleep(30)  # Check every 30 seconds
        current_time = datetime.now()

    # Trigger the reminder notification
    notification.notify(
        title=f"Reminder: {reminder_type}",
        message=f"Time to {reminder_type.lower()} your crops!",
        timeout=10  # Notification will stay for 10 seconds
    )

# Ask the user for input
reminder_type = input("What type of reminder would you like to set (watering, pesticide, fertilizer)? ")
reminder_time = input("Enter the date and time for the reminder (YYYY-MM-DD HH:MM:SS): ")

# Set the reminder
set_reminder(reminder_type, reminder_time)
