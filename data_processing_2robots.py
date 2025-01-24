import os
import sys
import yaml
import numpy as np
import pdb
from scipy.interpolate import interp1d
from typing import List, Tuple, Any
import re
import ast
import json



def parse_file(file_path: str) -> Tuple[List[str], np.ndarray,str]:
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
    trajectory = lines[1].strip()
    column_names = eval(lines[4].strip())  # Assumes column names are on the 4th line
    list_matches = re.findall(r'\[.*?\]', lines[5])
    processed_list = [s[1:] if s.startswith("[[") else s for s in list_matches]
    decoded_lists:List[Any] = [ast.literal_eval(match) for match in processed_list]  # Assumes data starts from the 5th line
    data = np.array(decoded_lists[:-1])
    return column_names, data,trajectory


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
            try:
                last_row = data[np.abs(data[:, time_col_index] - (t_ref-0.2)) <= tolerance]
                next_row = data[np.abs(data[:, time_col_index] - (t_ref+0.2)) <= tolerance]
            except:
                print('last or next value not found')
            alpha = 0.5
            interpolated_row = [(1 - alpha) * a + alpha * b for a, b in zip(last_row[0], next_row[0])]
            aligned_data.append(interpolated_row)

    return np.array(aligned_data)

def read_json_file(file_path:str):
    """
    Reads a JSON file and returns its contents.

    :param file_path: Path to the JSON file
    :return: Parsed JSON data as a dictionary
    """
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        print(f"Error: The file at '{file_path}' was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file at '{file_path}' is not a valid JSON file.")


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
    ref_columns, ref_data, trajectory_name = parse_file(file_paths[0])
    trajectory = read_json_file(trajectory_name)
    reference_time_base = [item[0] for item in ref_data]  # Time column from the first file
    all_data.append((ref_columns, ref_data))
    desired_data=[trajectory]
    # Parse and align data from other files
    aligned_data = [ref_data]

    for file_path in file_paths[1:]:
        columns, data, trajectory_names = parse_file(file_path)
        aligned = align_to_time_base(reference_time_base, data, time_col_index=0, tolerance=tolerance)
        aligned_data.append(aligned)
        desired_data.append(read_json_file(trajectory_names))
        all_data.append((columns, data))

    # Combine data into states and actions
    combined_states = []
    combined_actions = []
    
    for i, t in enumerate(reference_time_base):
        state_row = [float(t)]
        action_row = [float(t)]

        for j, data in enumerate(aligned_data):
            row = data[i]
            state_row.extend([float(np_float) for np_float in row[[1, 2, 3,-1]]])  # X, Y, Z, Theta 
            action_row.extend([float(np_float) for np_float in row[[4,5,-1]]])  # V_ctrl, Omega_ctrl

        combined_states.append(state_row)
        combined_actions.append(action_row)

    combined_desired_states = []
    combined_desired_actions = []
    state_row = []
    action_row = []        
    for j, (values1,values2) in enumerate(zip(desired_data[0]["result"]["states"],desired_data[1]["result"]["states"])):
        state_row.append([j*0.1,values1[0],values1[1],values1[2],values2[0],values2[1],values2[2]])
        
    for k, (values1,values2) in enumerate(zip(desired_data[0]["result"]["actions"],desired_data[1]["result"]["actions"])):
        action_row.append([k*0.1,values1[0],values1[1],values2[0],values2[1]])

    combined_desired_states.append(state_row)
    combined_desired_actions.append(action_row)
    return {"states": combined_states, "actions": combined_actions, "desired_states": combined_desired_states, "desired_actions": combined_desired_actions}

def calculate_error(data:dict):

    referenceTime = [item[0] for item in data["states"]]
    states = data["states"]
    desired_states = data["desired_states"][0]
    error1 = []
    error2 = []
    for state in states:
        desired_state1 = desired_states[int(state[4])]
        error1.append([desired_state1[1]-state[1],desired_state1[2]-state[2],desired_state1[3]-state[3]])
        desired_state2 = desired_states[int(state[-1])]
        error2.append([desired_state2[4]-state[5],desired_state2[5]-state[6],desired_state2[6]-state[7]]) # 567
    data["e1"] = error1
    data["e2"] = error2
    data["mean_error"] = float(np.linalg.norm([np.array(error1),np.array(error2)]))

def save_to_yaml(data: dict, output_file: str) -> None:
    """
    Save the combined data to a YAML file.
    Args:
        data (dict): Data to save.
        output_file (str): Path to the output YAML file.
    """
    with open(output_file, "w") as file:
        yaml.dump(data, file)



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
    calculate_error(combined_data)
    
    save_to_yaml(combined_data, output_yaml)
    print(f"Aligned and combined data saved to {output_yaml}")
    #except Exception as e:
    #    print(f"Error: {e}")
    #    sys.exit(1)
