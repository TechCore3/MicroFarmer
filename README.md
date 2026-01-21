# MicroFarmer
A GUI-based automation tool for Microsoft Edge that performs procedural searches to test session-based browser interactions.
##  Features
- **Graphical User Interface**: Lightweight Tkinter interface for easy configuration.
- **Procedural Query Generation**: Dynamically constructs unique search queries using a mixture of topics, modifiers, and contexts to ensure variety.
- **Human-Like Interaction**: 
  - Simulates character-by-character typing.
  - Implements randomized delays, scrolling, and search patterns.
  - Uses `slow_mo` for realistic browser behavior.
- **Persistent Profile Support**: Runs using your main Microsoft account session (cookies, logins).
- **Auto-Close Integration**: Automatically terminates active Edge processes on start to prevent profile locking.
##  Usage
###  Download (Ready to Run)
For the user-friendly, double-clickable version, check the **[Releases](../../releases)** tab and download the latest `rewards_farmer.exe`.
###  Running from Source
If you prefer running the Python script directly:
1. **Requirements**: Python 3.10+
2. **Setup Dependencies**:
   ```powershell
   pip install playwright
   python -m playwright install msedge
   ```
3. **Run**:
   ```powershell
   python rewards_farmer.py
   ```
## ⚙️ Configuration
The GUI allows you to configure:
- **Number of Searches**: Set your target count (e.g., 30).
- **Delay Range**: Set a Min and Max wait time (seconds) between activities to mimic human rest periods.
##  Important Notes
- **Profile Lock**: The script requires exclusive access to your Edge profile. The "Start Farming" button will force-close any open Edge windows to ensure the automation can launch successfully.
##  Disclaimer
This tool is for educational and testing purposes only. Using automated tools to farm rewards may violate Terms of Service for certain platforms.
