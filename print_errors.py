import os
import yaml
import numpy as np
def read_yaml_files_and_calculate_average(directory):
    """
    Reads all YAML files in a directory, extracts 'mean_error' values, and calculates their average.

    :param directory: The directory containing YAML files
    :return: The average of 'mean_error' values or None if no valid values found
    """
    mean_errors = []

    # Iterate through all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".yaml") or filename.endswith(".yml"):
            file_path = os.path.join(directory, filename)

            # Read the YAML file
            with open(file_path, 'r') as yaml_file:
                try:
                    data = yaml.safe_load(yaml_file)
                    # Extract 'mean_error' value if it exists
                    if "mean_error" in data:
                        mean_errors.append(data["mean_error"])
                except yaml.YAMLError as e:
                    print(f"Error reading {file_path}: {e}")

    # Calculate the average
    if mean_errors:
        average = sum(mean_errors) / len(mean_errors)
        std = np.std(mean_errors)
        print(f"Standard deviation {std}")
        return average
    else:
        return None


# Example usage
if __name__ == "__main__":
    directory = "/home/polyblank/Documents/IMRC/Experiments/DBCBS_Experiment_20.01_3Rob"  # Replace with your directory path
    average = read_yaml_files_and_calculate_average(directory)

    if average is not None:
        print(f"The average 'mean_error' is: {average}")
    else:
        print("No 'mean_error' values found in the YAML files.")
