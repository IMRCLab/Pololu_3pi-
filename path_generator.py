import numpy as np
import yaml
import json
import matplotlib.pyplot as plt

# Define cubic polynomials based on the provided equations
def cubic_polynomials(s, x_i, y_i, x_f, y_f, alpha_x, beta_x, alpha_y, beta_y):
    x              = s**3 * x_f - (s - 1)**3 * x_i + alpha_x * s**2 * (s - 1) + beta_x * s * (s - 1)**2
    x_prime        = 3 * s**2 * x_f - 3 * (s - 1)**2 * x_i  + alpha_x * (2 * s * (s - 1) + s**2) + beta_x * ((s - 1)**2 + 2 * s * (s - 1))
    x_double_prime = 6 * s * x_f - 6 * (s - 1) * x_i  + alpha_x * (6 * s - 2)  + beta_x * (6 * s - 4)
    y = s**3 * y_f - (s - 1)**3 * y_i + alpha_y * s**2 * (s - 1) + beta_y * s * (s - 1)**2
    y_prime = 3 * s**2 * y_f - 3 * (s - 1)**2 * y_i + alpha_y * (2 * s * (s - 1) + s**2) + beta_y * ((s - 1)**2 + 2 * s * (s - 1))
    y_double_prime = 6 * s * y_f - 6 * (s - 1) * y_i  + alpha_y * (6 * s - 2)  + beta_y * (6 * s - 4)



    return x, y, x_prime, y_prime, x_double_prime, y_double_prime

# Parameters
x_i, y_i, theta_i = 0, 0, 0  # Initial state
x_f, y_f, theta_f = 1, 1, 0 # Final state
k = 0.01 # initial speed o
alpha_x, beta_x = k*np.cos(theta_f) - 3*x_f, k*np.cos(theta_i) + 3*x_i  # Coefficients (change as needed)
alpha_y, beta_y = k*np.sin(theta_f) - 3*y_f, k*np.sin(theta_i) + 3*y_i  # Coefficients (change as needed)
t_min, t_max = 0, 10  # Time range for parameterization
t_values = np.linspace(t_min, t_max, 88)  # Discretized time parameter
# one time step 30 ms 
# Compute states and actions
states = []
actions = []

x_values, y_values, v_values, w_values = [], [], [], []


for t in t_values:
    s = (t - t_min) / (t_max - t_min)
    print(s)
    x, y, x_prime, y_prime, x_double_prime, y_double_prime = cubic_polynomials(s, x_i, y_i, x_f, y_f, alpha_x, beta_x, alpha_y, beta_y)
    
    # Compute theta
    theta = np.arctan2(y_prime, x_prime)
    
    # Compute v and w
    v = np.sqrt(x_prime**2 + y_prime**2)
    if v < 1e-4:
        w = 0
    else:
        w = (y_double_prime * x_prime - x_double_prime * y_prime) / (x_prime**2 + y_prime**2)
    
    states.append([float(x), float(y), float(theta)])
    actions.append([float(v), float(w)])
    x_values.append(x)
    y_values.append(y)
    v_values.append(v)
    w_values.append(w)

# Prepare output structure
result = {
    "result": {
        "states": states,
        "actions": actions
    }
}

# Save to YAML
yaml_file_path = "trajectories/unicycle_flatness.yaml"
with open(yaml_file_path, "w") as yaml_file:
    yaml.dump(result, yaml_file, default_flow_style=False)

# Save to JSON
json_file_path = "trajectories/unicycle_flatness.json"
with open(json_file_path, "w") as json_file:
    json.dump(result, json_file, indent=4)

# Plot the x, y trajectory
x_coords = [state[0] for state in states]
y_coords = [state[1] for state in states]
theta_coords = [state[2] for state in states]

plt.figure(figsize=(10, 6))
plt.plot(x_coords, y_coords, label="Trajectory", color="blue")

# Add arrows indicating theta
arrow_frequency = 2  # Plot an arrow for every other theta
for i in range(0, len(x_coords), arrow_frequency):
    x = x_coords[i]
    y = y_coords[i]
    theta = theta_coords[i]
    dx = 0.01 * np.cos(theta)
    dy = 0.01 * np.sin(theta)
    plt.arrow(x, y, dx, dy, head_width=0.05, head_length=0.05, fc='red', ec='red')

# Plot settings
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Trajectory with Theta Arrows")
plt.legend()
plt.grid()
plt.axis("equal")
plt.show()




# Plot x, y, v, and w with respect to t
plt.figure(figsize=(10, 6))
plt.plot(t_values, x_values, label="x(t)", color="blue")
plt.plot(t_values, y_values, label="y(t)", color="green")
plt.xlabel("t")
plt.ylabel("Position")
plt.title("x and y vs t")
plt.legend()
plt.grid()
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(t_values, v_values, label="v(t)", color="purple")
plt.xlabel("t")
plt.ylabel("Linear Velocity (v)")
plt.title("v vs t")
plt.legend()
plt.grid()
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(t_values, w_values, label="w(t)", color="orange")
plt.xlabel("t")
plt.ylabel("Angular Velocity (w)")
plt.title("w vs t")
plt.legend()
plt.grid()
plt.show()

print(f"Files generated:\n- YAML: {yaml_file_path}\n- JSON: {json_file_path}")