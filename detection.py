import os
import psutil

def check_suspicious_files():
    # Check if typical log files are created
    suspicious_files = ["log.txt", "keylog.txt", "keystrokes.txt"]
    found_files = False
    for file in suspicious_files:
        if os.path.exists(file):
            print(f"[ALERT] Suspicious file detected: {file}")
            found_files = True
    return found_files

def check_suspicious_processes():
    # Check if suspicious processes are running
    suspicious_keywords = ["keylogger", "pynput", "listener", "keyboard"]
    found_processes = False
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info.get('cmdline')
            if cmdline:  # Only proceed if cmdline is not None
                # Ignore your own detection script
                if proc.info['name'] == 'python.exe' and 'detection.py' in str(cmdline):
                    continue  # Skip self
                
                for keyword in suspicious_keywords:
                    if any(keyword.lower() in str(cmd).lower() for cmd in cmdline):
                        print(f"[ALERT] Suspicious process detected: {proc.info['name']} (PID: {proc.info['pid']})")
                        found_processes = True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    
    return found_processes

def main():
    print("Running Keylogger Detection Tool...\n")
    found_files = check_suspicious_files()
    found_processes = check_suspicious_processes()
    
    # If nothing suspicious was found, print a safe message
    if not found_files and not found_processes:
        print("[INFO] No suspicious files or processes detected. The system appears to be safe.\n")
    else:
        print("\nDetection Completed.")

if __name__ == "__main__":
    main()
