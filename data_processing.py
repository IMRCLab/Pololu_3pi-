import os
import sys
import yaml
import numpy as np
import pdb
from scipy.interpolate import interp1d
from typing import List, Tuple


def parse_file(file_path: str) -> Tuple[List[str], np.ndarray]:
    """
    Parse the given file and extract header and data.
    Args:
        file_path (str): Path to the file.
    Returns:
        tuple: (columns, data), where columns is a list of headers and data is a NumPy array.
    """
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Parse header
    column_names = eval(lines[4].strip())  # Assumes column names are on the 4th line
    data = eval(lines[5].strip())
    data = np.array(eval("".join(lines[4:]).strip()))  # Assumes data starts from the 5th line

    return column_names, data


def align_to_time_base(reference_time_base: np.ndarray, data: np.ndarray, time_col_index: int, tolerance: float) -> np.ndarray:
    """
    Align data to the reference time base, tolerating a difference of up to `tolerance`.
    Args:
        reference_time_base (np.ndarray): Time base from the first file.
        data (np.ndarray): Data from the current file.
        time_col_index (int): Index of the time column in the data.
        tolerance (float): Maximum allowed time difference for alignment.
    Returns:
        np.ndarray: Aligned data.
    """
    aligned_data = []

    for t_ref in reference_time_base:
        # Find the closest time point in the data within the tolerance
        matching_rows = data[np.abs(data[:, time_col_index] - t_ref) <= tolerance]

        if matching_rows.size > 0:
            aligned_data.append(matching_rows[0])  # Take the first matching row
        else:
            # No matching row; interpolate linearly
            interpolator = interp1d(
                data[:, time_col_index],
                data[:, 1:],  # Exclude the time column for interpolation
                kind="linear",
                bounds_error=False,
                fill_value="extrapolate",
            )
            interpolated_row = [t_ref] + interpolator(t_ref).tolist()
            aligned_data.append(interpolated_row)

    return np.array(aligned_data)


def combine_data(folder_path: str, tolerance: float) -> dict:
    """
    Combine data from all files, using the time base from the first file.
    Args:
        folder_path (str): Path to the folder containing trajectory files.
        tolerance (float): Maximum allowed time difference for alignment.
    Returns:
        dict: Combined data for states and actions.
    """
    all_data = []
    file_paths = [
        os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".txt") or f.endswith(".json")
    ]

    if not file_paths:
        raise ValueError(f"No valid trajectory files found in the folder: {folder_path}")

    # Parse the first file to determine the reference time base
    ref_columns, ref_data = parse_file(file_paths[0])
    reference_time_base = ref_data[:, 0]  # Time column from the first file
    all_data.append((ref_columns, ref_data))

    # Parse and align data from other files
    aligned_data = [ref_data]

    for file_path in file_paths[1:]:
        columns, data = parse_file(file_path)
        aligned = align_to_time_base(reference_time_base, data, time_col_index=0, tolerance=tolerance)
        aligned_data.append(aligned)
        all_data.append((columns, data))

    # Combine data into states and actions
    combined_states = []
    combined_actions = []

    for i, t in enumerate(reference_time_base):
        state_row = [t]
        action_row = [t]

        for j, data in enumerate(aligned_data):
            row = data[i]
            state_row.extend(row[[1, 2, 3, 4]])  # X, Y, Z, Theta
            action_row.extend(row[[4, 5]])  # V_ctrl, Omega_ctrl

        combined_states.append({"states": state_row})
        combined_actions.append({"actions": action_row})

    return {"states": combined_states, "actions": combined_actions}


def save_to_yaml(data: dict, output_file: str) -> None:
    """
    Save the combined data to a YAML file.
    Args:
        data (dict): Data to save.
        output_file (str): Path to the output YAML file.
    """
    with open(output_file, "w") as file:
        yaml.dump(data, file, default_flow_style=False)


# Main execution
if __name__ == "__main__":
    # Parse command-line arguments
    if len(sys.argv) < 2:
        print("Usage: python script.py <folder_path> [tolerance]")
        sys.exit(1)
    folder = sys.argv[1]
    tolerance = float(sys.argv[2]) if len(sys.argv) > 2 else 0.02  # Default tolerance is 0.02

    # Determine output file name from folder name
    folder_name = os.path.basename(os.path.normpath(folder))
    output_yaml = f"{folder_name}.yaml"

    #try:
    combined_data = combine_data(folder, tolerance)
    save_to_yaml(combined_data, output_yaml)
    print(f"Aligned and combined data saved to {output_yaml}")
    #except Exception as e:
    #    print(f"Error: {e}")
    #    sys.exit(1)
