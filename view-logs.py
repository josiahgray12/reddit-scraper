#!/usr/bin/env python3
"""
Nookly Reddit Monitor - Log Viewer
A user-friendly script to view and filter log files.
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

def get_log_files():
    """Get available log files."""
    log_dir = Path('logs')
    if not log_dir.exists():
        print("❌ Logs directory not found!")
        return []
    
    return [f for f in log_dir.glob('*.log')]

def read_log_file(file_path, num_lines=50, level=None, search=None):
    """Read and filter log file."""
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            
        # Filter by level if specified
        if level:
            lines = [l for l in lines if f" - {level.upper()} - " in l]
            
        # Filter by search term if specified
        if search:
            lines = [l for l in lines if search.lower() in l.lower()]
            
        # Get last N lines
        return lines[-num_lines:]
    except FileNotFoundError:
        return []

def format_log_entry(line):
    """Format a log entry for display."""
    try:
        # Split the line into components
        parts = line.strip().split(' - ')
        if len(parts) >= 3:
            timestamp = parts[0]
            level = parts[1]
            message = ' - '.join(parts[2:])
            
            # Add color based on level
            if level == 'ERROR':
                level = f"\033[91m{level}\033[0m"  # Red
            elif level == 'WARNING':
                level = f"\033[93m{level}\033[0m"  # Yellow
            elif level == 'INFO':
                level = f"\033[92m{level}\033[0m"  # Green
                
            return f"{timestamp} | {level} | {message}"
        return line.strip()
    except:
        return line.strip()

def main():
    """Main function to display logs."""
    print("\n📋 Nookly Reddit Monitor - Log Viewer\n")
    print("=" * 80)

    # Get available log files
    log_files = get_log_files()
    if not log_files:
        print("No log files found. The system may not be running.")
        return

    # Show log file options
    print("\nAvailable log files:")
    for i, file in enumerate(log_files, 1):
        print(f"{i}. {file.name}")

    # Get user selection
    try:
        choice = int(input("\nSelect log file (number): "))
        if choice < 1 or choice > len(log_files):
            print("❌ Invalid selection!")
            return
        selected_file = log_files[choice - 1]
    except ValueError:
        print("❌ Please enter a number!")
        return

    # Get filter options
    print("\nFilter options:")
    print("1. Show all entries")
    print("2. Show errors only")
    print("3. Show warnings and errors")
    print("4. Search for specific text")
    
    try:
        filter_choice = int(input("\nSelect filter (number): "))
        level = None
        search = None
        
        if filter_choice == 2:
            level = "ERROR"
        elif filter_choice == 3:
            level = "WARNING"
        elif filter_choice == 4:
            search = input("Enter search text: ")
    except ValueError:
        print("❌ Please enter a number!")
        return

    # Get number of lines to show
    try:
        lines = int(input("\nNumber of lines to show (default 50): ") or "50")
    except ValueError:
        lines = 50

    # Read and display logs
    print(f"\n📄 Showing last {lines} lines from {selected_file.name}")
    print("=" * 80)
    
    log_entries = read_log_file(selected_file, lines, level, search)
    if not log_entries:
        print("No matching log entries found.")
    else:
        for entry in log_entries:
            print(format_log_entry(entry))

    print("\n" + "=" * 80)
    print("\nNeed help? Check the README.md file or contact support@nookly.com")

if __name__ == "__main__":
    main() 