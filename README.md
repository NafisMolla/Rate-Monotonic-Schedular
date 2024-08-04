# Rate Monotonic Scheduling Simulation

This project implements a Rate Monotonic Scheduling (RMS) simulation in Python. RMS is a fixed-priority scheduling algorithm commonly used in real-time systems. The simulation reads task parameters from an input file and determines whether the tasks can be scheduled without missing deadlines. The simulation outputs whether the tasks are schedulable and the number of preemptions for each task.

## Files

- **rms.py**: The main Python script containing the implementation of the RMS simulation.

## How It Works

### Classes

#### `task`
This class represents a task in the system. Each task has the following attributes:
- `release_time`: The time at which the task is released.
- `period_prio`: The period of the task, which also serves as its priority (lower values indicate higher priority).
- `execution_time`: The execution time required by the task.
- `deadline`: The deadline by which the task must complete.
- `id`: A unique identifier for the task.

The `task` class also implements the `__lt__` method to compare tasks based on their priority, ID, and release time, allowing tasks to be easily managed in a heap.

#### `simulate_rms`
This class handles the RMS simulation. It includes methods to read task parameters from an input file, calculate the hyperperiod, generate repeating tasks, and simulate the task execution.

Key methods include:
- `__init__(self, filename)`: Initializes the simulation, reads the input file, and calculates the hyperperiod.
- `lcm(self, a, b)`: Calculates the least common multiple of two numbers.
- `calculate_hyperperiod(self)`: Calculates the hyperperiod of the task set.
- `read_file(self, filename)`: Reads task parameters from the input file.
- `generate_repeating_tasks(self)`: Generates repeating tasks for the entire hyperperiod and sorts them by release time and priority.
- `doing_sim(self)`: Runs the RMS simulation, checking for task preemptions and missed deadlines.
- `run(self)`: Initializes the preemptions list, generates repeating tasks, and runs the simulation.

### Main Function
The `main(filename)` function initializes the `simulate_rms` class with the provided filename, runs the simulation, and prints the execution time.

## Usage

To run the simulation, use the following command:

```bash
python3 ece_455_final.py <input_file>
```

Replace `<input_file>` with the path to your input file containing task parameters. The input file should contain one line per task, with each line specifying the execution time, period, and deadline (in seconds), separated by commas.

### Example Input File

```
0.002,0.010,0.010
0.001,0.020,0.020
0.001,0.040,0.040
```

This example specifies three tasks with the following parameters:
1. Task 1: Execution time = 2ms, Period/Priority = 10ms, Deadline = 10ms
2. Task 2: Execution time = 1ms, Period/Priority = 20ms, Deadline = 20ms
3. Task 3: Execution time = 1ms, Period/Priority = 40ms, Deadline = 40ms

### Output

The program outputs whether the tasks are schedulable (1) or not (0) and the number of preemptions for each task. Additionally, it prints the execution time of the simulation.

## Notes

- The simulation assumes all times are provided in seconds and converts them to milliseconds for internal calculations.
- The `waiting_tasks` queue is implemented as a heap to efficiently manage task priorities and minimize execution time.
- The program prints an execution time summary to help users understand the efficiency of the simulation.

Feel free to modify and extend this implementation to suit your specific needs in real-time systems research and development.
