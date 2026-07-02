import datetime
import pytz
from mcp.server.fastmcp import FastMCP
from typing import Dict, Any

# Initialize FastMCP Server
mcp = FastMCP("TimeAndCalendar")

@mcp.tool()
def get_current_time(timezone_str: str = "UTC") -> Dict[str, Any]:
    """
    Get the current time and date for a specific timezone.
    
    Args:
        timezone_str: The timezone string (e.g., 'America/New_York', 'Asia/Karachi', 'UTC')
    """
    try:
        tz = pytz.timezone(timezone_str)
        now = datetime.datetime.now(tz)
        return {
            "timezone": timezone_str,
            "current_time": now.strftime("%Y-%m-%d %H:%M:%S"),
            "day_of_week": now.strftime("%A"),
            "is_weekend": now.weekday() >= 5
        }
    except pytz.exceptions.UnknownTimeZoneError:
        return {"error": f"Unknown timezone: {timezone_str}"}

@mcp.tool()
def calculate_time_difference(time1: str, time2: str) -> Dict[str, Any]:
    """
    Calculate the difference between two times in hours and minutes.
    Used to determine if there is enough time to reach a destination before it closes.
    
    Args:
        time1: First time string in format 'HH:MM' (24-hour)
        time2: Second time string in format 'HH:MM' (24-hour)
    """
    try:
        t1 = datetime.datetime.strptime(time1, "%H:%M")
        t2 = datetime.datetime.strptime(time2, "%H:%M")
        
        diff = t2 - t1
        # Handle cases where time2 is on the next day
        if diff.total_seconds() < 0:
            diff += datetime.timedelta(days=1)
            
        hours, remainder = divmod(diff.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        return {
            "difference_hours": hours,
            "difference_minutes": minutes,
            "total_minutes": int(diff.total_seconds() / 60)
        }
    except ValueError as e:
        return {"error": f"Invalid time format. Please use HH:MM. Error: {str(e)}"}

if __name__ == "__main__":
    mcp.run()
