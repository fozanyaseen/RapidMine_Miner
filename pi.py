import pandas as pd

def convert_date_format(file_path, output_path):
    # Read the CSV file
    df = pd.read_csv(file_path, delimiter=',')

    # Identifying columns that contain date information
    date_columns = [col for col in df.columns if 'Date' in col]

    # Converting dates in these columns to the desired format
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors='coerce', format='%d-%m-%Y').dt.strftime('%d/%m/%Y')

    # Save the modified dataframe to a new CSV file
    df.to_csv(output_path, index=False, sep=',')

# Specify the path to your CSV file and the output file name
file_path = 'example_input\Converted_Incident_Activity.csv'  # Replace with your CSV file path
output_path = 'example_input\Converted_Incident_Activity.csv'  # Replace with your desired output file path

# Run the conversion
convert_date_format(file_path, output_path)

print("Date format conversion completed. The file has been saved to:", output_path)