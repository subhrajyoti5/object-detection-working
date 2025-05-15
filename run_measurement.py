# run_measurement.py (improved)
import sys
import signal
import traceback
from datetime import datetime
import os

# Import the enhanced error logger first (to ensure monkey patching happens early)
import error_logger

# Then import camruler which will use the patched functions
import camruler

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\nProgram interrupted by user. Saving measurement data...")
    error_logger.save_log()
    sys.exit(0)

def main():
    """Main entry point for the measurement application"""
    print(f"Starting measurement application at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Press Q to quit and save measurement data.")
    
    try:
        # Register signal handler for clean shutdown
        signal.signal(signal.SIGINT, signal_handler)
        
        # Run camruler's main function
        camruler.main()
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        print(traceback.format_exc())
    finally:
        # Always save logs when exiting, whether normally or due to error
        print("Measurement session ended. Saving data...")
        saved = error_logger.save_log()

        if saved:
            print(f"Data saved successfully in 'measurement_logs' directory.")
        else:
            print("No measurement data was collected or saving failed.")

if __name__ == "__main__":
    main()