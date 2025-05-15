# error_logger.py
import pandas as pd
from datetime import datetime
import traceback
import os
import atexit
from error_calculator import calculate_2d_error, draw_2d_error_box as original_draw_error

# Global store for error measurements
error_log = []

def logged_draw_error(frame, x, y, expected_l, measured_l, expected_w, measured_w, *args, **kwargs):
    """
    Enhanced error box drawer that also logs measurement data for later export
    """
    # Call the original function to draw on screen
    original_draw_error(frame, x, y, expected_l, measured_l, expected_w, measured_w, *args)
    
    try:
        # Calculate error metrics
        errors = calculate_2d_error(expected_l, measured_l, expected_w, measured_w)
        
        # Log detailed data
        error_log.append({
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Expected_Length": expected_l,
            "Measured_Length": measured_l,
            "Length_Error_Abs": errors['length']['absolute_error'],
            "Length_Error_Rel": errors['length']['relative_error'],
            "Expected_Width": expected_w,
            "Measured_Width": measured_w,
            "Width_Error_Abs": errors['width']['absolute_error'],
            "Width_Error_Rel": errors['width']['relative_error'],
            "Area_Error_Rel": errors['area']['relative_error'],
            "Mean_Error": errors['mean_relative_error']
        })
        
        # Debug output so we know logging is working
        print(f"Measurement logged: {len(error_log)} records total")
        
    except Exception as e:
        print(f"LOG ERROR: {str(e)}")
        print(traceback.format_exc())

# Monkey-patch the error calculator's draw function
import error_calculator
error_calculator.draw_2d_error_box = logged_draw_error

def save_log():
    """
    Save collected measurement data to Excel file
    """
    try:
        if not error_log:
            print("No error data to save")
            return False
            
        # Create DataFrame from logged data
        df = pd.DataFrame(error_log)
        
        # Create logs directory if it doesn't exist
        os.makedirs("measurement_logs", exist_ok=True)
        
        # Generate filename with timestamp
        filename = f"measurement_logs/error_log_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.xlsx"
        
        # Save to Excel
        df.to_excel(filename, index=False, engine='openpyxl')
        print(f"Successfully saved {len(error_log)} measurement records to: {filename}")
        
        return True
        
    except Exception as e:
        print(f"SAVE FAILED: {str(e)}")
        print(traceback.format_exc())
        return False

# Register save_log to run at program exit
atexit.register(save_log)