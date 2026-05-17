# 👻 Dead Cursor

A modern, lightweight Python desktop application that monitors your inactivity and automatically moves the mouse and performs clicks to keep your system awake.

## Features
- **Global Inactivity Detection:** Monitors physical mouse and keyboard usage system-wide.
- **Customizable Thresholds:** Set exactly how long to wait before jiggling starts.
- **Customizable Duration:** Control how long the jiggle session lasts.
- **Smart Interruption:** Automatically stops jiggling as soon as it detects real human input.
- **Modern UI:** Built with CustomTkinter for a sleek, dark-themed experience.

## Installation
1. Ensure you have Python 3.x installed.
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Run the application:
   ```bash
   python main.py
   ```
2. Set your **Inactivity Threshold** (in seconds).
3. Set your **Jiggle Duration** (in seconds).
4. Click **Start Guard**.
5. The status will update to "Monitoring...". If you don't touch your computer for the threshold time, the "Dead Cursor" will come to life and start jiggling for you!
