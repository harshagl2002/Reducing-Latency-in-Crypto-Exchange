import os
import pandas as pd

def compare_latency_columns(file_path1, file_path2):
    # Read the CSV files into Pandas DataFrames
    df1 = pd.read_csv(file_path1)
    df2 = pd.read_csv(file_path2)
    # Assuming both CSV files have a 'latency' column
    latency_column1 = df1['latency']
    latency_column2 = df2['latency']
    # Compare the latency columns and find the differences
    differences = (latency_column2 - latency_column1) * 1000
    return differences

def is_csv_file(filename):
    return filename.lower().endswith('.csv')

def check_and_save_checked_files(directory, comparison_choice):
    if comparison_choice == 1:
        csv_files = [file for file in os.listdir(directory) if is_csv_file(file)]
        latest_file = max(csv_files, key=lambda x: os.path.getmtime(os.path.join(directory, x)))
        base_file = "i-01675c75c13d2ed7c1701742755.1731575.csv"
        file1_path = os.path.abspath(latest_file)
        file2_path = os.path.abspath(base_file)
        differences = compare_latency_columns(file1_path, file2_path)
        # Display the differences
        print("Differences in Latency Column:")
        print(differences)
        print("Average Latency Reduction:", differences.mean(axis=0), "ms")
    else:
        # Check for CSV files in the directory
        csv_files = [file for file in os.listdir(directory) if is_csv_file(file)]
        latest_file = max(csv_files, key=lambda x: os.path.getmtime(os.path.join(directory, x)))
        csv_files = [file for file in csv_files if file != latest_file]
        second_latest_file = max(csv_files, key=lambda x: os.path.getmtime(os.path.join(directory, x)))
        file1_path = os.path.abspath(latest_file)
        file2_path = os.path.abspath(second_latest_file)
        differences = compare_latency_columns(file1_path, file2_path)
        # Display the differences
        print("Differences in Latency Column:")
        print(differences)
        print("Average Latency Reduction:", differences.mean(axis=0), "ms")

def main():
    comparison_choice = int(input("Press 1 for comparison with the base instance, 2 for comparison with most recent change: "))
    directory_to_check = "/home/ec2-user/group_01_project"
    check_and_save_checked_files(directory_to_check, comparison_choice)

if __name__ == "__main__":
    main()