import cv2
import numpy as np
import traceback  # Add for better error tracking


def calculate_error(expected, measured):
    """
    Calculate absolute and relative error between expected and measured values.
    """
    absolute_error = abs(expected - measured)
    relative_error = (absolute_error / expected * 100) if expected != 0 else 0
    return {
        'absolute_error': round(absolute_error, 2),
        'relative_error': round(relative_error, 2)
    }


def calculate_2d_error(expected_length, measured_length, expected_width, measured_width):
    """
    Calculate errors for both length and width measurements.
    """
    length_errors = calculate_error(expected_length, measured_length)
    width_errors = calculate_error(expected_width, measured_width)
    
    # Calculate area error
    expected_area = expected_length * expected_width
    measured_area = measured_length * measured_width
    area_errors = calculate_error(expected_area, measured_area)
    
    # Calculate mean error
    mean_relative_error = (length_errors['relative_error'] + width_errors['relative_error']) / 2
    
    return {
        'length': length_errors,
        'width': width_errors,
        'area': area_errors,
        'mean_relative_error': round(mean_relative_error, 2)
    }


def draw_error_box(frame, x, y, expected, measured):
    """
    Draw error values on the image frame.
    """
    try:
        errors = calculate_error(expected, measured)
        text1 = f"Expected: {expected:.2f}"
        text2 = f"Measured: {measured:.2f}"
        text3 = f"Abs Error: {errors['absolute_error']:.2f}"
        text4 = f"Rel Error: {errors['relative_error']:.2f}%"

        cv2.putText(frame, text1, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
        cv2.putText(frame, text2, (x, y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
        cv2.putText(frame, text3, (x, y + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
        cv2.putText(frame, text4, (x, y + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
    except Exception as e:
        print(f"Error in draw_error_box: {e}")
        cv2.putText(frame, "Error calc failed", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)


def draw_2d_error_box(frame, x, y, expected_length, measured_length, 
                     expected_width, measured_width, expected_name="Expected", measured_name="Measured"):
    """
    Draw comprehensive error analysis for 2D measurements.
    """
    try:
        # Print debug info
        print(f"Drawing error box with: {expected_length:.2f}×{expected_width:.2f} vs {measured_length:.2f}×{measured_width:.2f}")
        
        # Safety check for invalid inputs
        if not all(isinstance(val, (int, float)) for val in [expected_length, measured_length, expected_width, measured_width]):
            raise ValueError(f"Invalid measurement values: {expected_length}, {measured_length}, {expected_width}, {measured_width}")
            
        # Calculate errors
        errors = calculate_2d_error(float(expected_length), float(measured_length), 
                                   float(expected_width), float(measured_width))
        
        # Box dimensions
        box_height = 110
        box_width = 280
        
        # Background
        cv2.rectangle(frame, (x-5, y-25), (x+box_width, y+box_height), (40, 40, 40), -1)
        
        # Border - color based on error severity
        border_color = (0, 255, 0)  # Green for low error
        if errors['mean_relative_error'] > 5:
            border_color = (0, 165, 255)  # Orange for medium error
        if errors['mean_relative_error'] > 10:
            border_color = (0, 0, 255)  # Red for high error
            
        cv2.rectangle(frame, (x-5, y-25), (x+box_width, y+box_height), border_color, 2)
        
        # Title
        cv2.putText(frame, "Measurement Error Analysis", (x, y), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Format values safely - handle extreme values gracefully
        def format_value(val):
            if abs(val) > 999:
                return f"{val:.0f}"
            elif abs(val) > 99:
                return f"{val:.1f}"
            else:
                return f"{val:.2f}"
        
        # Length errors
        y_offset = y + 20
        length_text = f"Length: {expected_name}={format_value(expected_length)}, {measured_name}={format_value(measured_length)}"
        cv2.putText(frame, length_text, (x, y_offset), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)
        
        error_text = f"Error: {format_value(errors['length']['absolute_error'])} ({format_value(errors['length']['relative_error'])}%)"
        cv2.putText(frame, error_text, (x, y_offset + 15), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)
        
        # Width errors
        y_offset += 30
        width_text = f"Width: {expected_name}={format_value(expected_width)}, {measured_name}={format_value(measured_width)}"
        cv2.putText(frame, width_text, (x, y_offset), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)
        
        error_text = f"Error: {format_value(errors['width']['absolute_error'])} ({format_value(errors['width']['relative_error'])}%)"
        cv2.putText(frame, error_text, (x, y_offset + 15), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)
        
        # Area and mean errors
        y_offset += 30
        area_text = f"Area Error: {format_value(errors['area']['relative_error'])}%"
        cv2.putText(frame, area_text, (x, y_offset), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)
        
        mean_text = f"Mean Error: {format_value(errors['mean_relative_error'])}%"
        cv2.putText(frame, mean_text, (x, y_offset + 15), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)
        
    except Exception as e:
        # Print detailed error info to console
        print(f"ERROR IN ERROR CALCULATOR: {e}")
        print(traceback.format_exc())
        
        # Show simplified error message on screen
        cv2.rectangle(frame, (x-5, y-25), (x+250, y+50), (0, 0, 255), 2)
        cv2.putText(frame, "Error calculation failed", (x, y), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        try:
            cv2.putText(frame, f"Expected: {expected_length:.1f}×{expected_width:.1f}", (x, y+20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)
            cv2.putText(frame, f"Measured: {measured_length:.1f}×{measured_width:.1f}", (x, y+40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)
        except:
            cv2.putText(frame, "Invalid measurement values", (x, y+20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 0, 0), 1)


# Example usage
if __name__ == '__main__':
    # Test with a blank frame and known values
    frame = np.ones((300, 600, 3), dtype=np.uint8) * 50
    
    # Test with both small and large reference values
    print("Testing with small reference values (50×50):")
    draw_2d_error_box(frame, 20, 50, 50.0, 45.0, 50.0, 48.0)
    
    print("\nTesting with large reference values (145×80):")
    draw_2d_error_box(frame, 20, 180, 145.0, 130.0, 80.0, 75.0)
    
    cv2.imshow('Error Display Test', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
