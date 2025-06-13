#!/usr/bin/env python3
"""
Nookly Reddit Monitor - Status Check
A user-friendly script to check the system status.
"""

import os
import json
import time
import psutil
from datetime import datetime
from pathlib import Path

def check_running_processes():
    """Check if the Reddit monitor processes are running."""
    running_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            # Check for Python processes running our scripts
            if proc.info['name'] == 'python' and proc.info['cmdline']:
                cmdline = ' '.join(proc.info['cmdline'])
                if 'start.py' in cmdline or 'monitor.py' in cmdline:
                    running_processes.append({
                        'pid': proc.info['pid'],
                        'cmdline': cmdline,
                        'start_time': datetime.fromtimestamp(proc.create_time()).strftime('%Y-%m-%d %H:%M:%S')
                    })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return running_processes

def get_last_email_time():
    """Get the time of the last email sent."""
    try:
        with open('logs/daily.log', 'r') as f:
            for line in reversed(list(f)):
                if "Sent daily digest" in line:
                    return line.split(' - ')[0]
    except FileNotFoundError:
        return "No log file found"

def count_today_threads():
    """Count threads monitored today."""
    try:
        count = 0
        today = datetime.now().strftime('%Y-%m-%d')
        with open('logs/daily.log', 'r') as f:
            for line in f:
                if today in line and "Generated response for thread" in line:
                    count += 1
        return count
    except FileNotFoundError:
        return 0

def check_config_files():
    """Check if configuration files exist and are valid."""
    config_status = {
        '.env': os.path.exists('.env'),
        'config.json': os.path.exists('config.json')
    }
    return config_status

def main():
    """Main function to display system status."""
    print("\n📊 Nookly Reddit Monitor Status\n")
    print("=" * 50)

    # Check running processes
    print("\n🔄 System Status:")
    running_processes = check_running_processes()
    if running_processes:
        print("✅ System is running")
        for proc in running_processes:
            print(f"  • Process ID: {proc['pid']}")
            print(f"  • Started: {proc['start_time']}")
            print(f"  • Command: {proc['cmdline']}")
    else:
        print("❌ System is not running")

    # Check configuration
    print("\n⚙️ Configuration:")
    config_status = check_config_files()
    for file, exists in config_status.items():
        status = "✅" if exists else "❌"
        print(f"{status} {file}")

    # Show monitoring stats
    print("\n📈 Monitoring Stats:")
    threads_today = count_today_threads()
    print(f"📝 Threads monitored today: {threads_today}")
    
    last_email = get_last_email_time()
    print(f"📧 Last email sent: {last_email}")

    # Check log files
    print("\n📋 Log Files:")
    log_files = {
        'daily.log': 'logs/daily.log',
        'error.log': 'logs/error.log'
    }
    for name, path in log_files.items():
        exists = os.path.exists(path)
        status = "✅" if exists else "❌"
        print(f"{status} {name}")

    print("\n" + "=" * 50)
    print("\nNeed help? Check the README.md file or contact support@nookly.com")

if __name__ == "__main__":
    main() 