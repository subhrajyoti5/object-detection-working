# measurement_analyzer.py
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import glob

def list_measurement_files():
    """List all available measurement log files"""
    try:
        files = glob.glob("measurement_logs/*.xlsx")
        if not files:
            print("No measurement log files found in 'measurement_logs' directory.")
            return []
            
        print(f"Found {len(files)} measurement log files:")
        for i, file in enumerate(files):
            print(f"  {i+1}. {os.path.basename(file)}")
        
        return files
    except Exception as e:
        print(f"Error listing files: {str(e)}")
        return []

def analyze_measurements(file_path):
    """Analyze measurement data from specified Excel file"""
    try:
        # Load the data
        df = pd.read_excel(file_path)
        
        # Basic statistics
        print("\n=== MEASUREMENT ANALYSIS ===")
        print(f"File: {os.path.basename(file_path)}")
        print(f"Total measurements: {len(df)}")
        
        # Calculate averages
        avg_length_error = df['Length_Error_Rel'].mean()
        avg_width_error = df['Width_Error_Rel'].mean()
        avg_mean_error = df['Mean_Error'].mean()
        
        print(f"Average length error: {avg_length_error:.2f}%")
        print(f"Average width error: {avg_width_error:.2f}%")
        print(f"Average mean error: {avg_mean_error:.2f}%")
        
        # Generate plots
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        
        # Length error histogram
        axes[0, 0].hist(df['Length_Error_Rel'], bins=10, color='blue', alpha=0.7)
        axes[0, 0].set_title('Length Error Distribution (%)')
        axes[0, 0].set_xlabel('Error %')
        axes[0, 0].set_ylabel('Frequency')
        
        # Width error histogram
        axes[0, 1].hist(df['Width_Error_Rel'], bins=10, color='green', alpha=0.7)
        axes[0, 1].set_title('Width Error Distribution (%)')
        axes[0, 1].set_xlabel('Error %')
        axes[0, 1].set_ylabel('Frequency')
        
        # Error over time
        if 'Timestamp' in df.columns:
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            df = df.sort_values('Timestamp')
            
            axes[1, 0].plot(range(len(df)), df['Length_Error_Rel'], 'b-', label='Length')
            axes[1, 0].plot(range(len(df)), df['Width_Error_Rel'], 'g-', label='Width')
            axes[1, 0].plot(range(len(df)), df['Mean_Error'], 'r-', label='Mean')
            axes[1, 0].set_title('Error Trends')
            axes[1, 0].set_xlabel('Measurement #')
            axes[1, 0].set_ylabel('Error %')
            axes[1, 0].legend()
        
        # Expected vs Measured
        axes[1, 1].scatter(df['Expected_Length'], df['Measured_Length'], color='blue', alpha=0.7, label='Length')
        axes[1, 1].scatter(df['Expected_Width'], df['Measured_Width'], color='green', alpha=0.7, label='Width')
        
        # Add perfect line for reference
        max_val = max(df['Expected_Length'].max(), df['Expected_Width'].max()) * 1.1
        min_val = min(df['Expected_Length'].min(), df['Expected_Width'].min()) * 0.9
        axes[1, 1].plot([min_val, max_val], [min_val, max_val], 'r--')
        
        axes[1, 1].set_title('Expected vs Measured')
        axes[1, 1].set_xlabel('Expected (mm)')
        axes[1, 1].set_ylabel('Measured (mm)')
        axes[1, 1].legend()
        
        plt.tight_layout()
        
        # Save figure
        output_file = f"measurement_logs/analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(output_file)
        print(f"Analysis plots saved to: {output_file}")
        
        plt.show()
        
        return True
        
    except Exception as e:
        print(f"Analysis error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function for measurement analyzer"""
    print("=== MEASUREMENT DATA ANALYZER ===")
    
    # Make sure logs directory exists
    os.makedirs("measurement_logs", exist_ok=True)
    
    # List available files
    files = list_measurement_files()
    if not files:
        return
        
    # Let user select a file
    try:
        selection = int(input("\nEnter file number to analyze (or 0 to exit): "))
        if selection == 0:
            return
            
        if 1 <= selection <= len(files):
            file_path = files[selection-1]
            analyze_measurements(file_path)
        else:
            print("Invalid selection.")
    except ValueError:
        print("Please enter a valid number.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
