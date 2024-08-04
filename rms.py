from functools import reduce
import sys
from math import gcd
import time
from collections import deque
import heapq

#-------------------------------------------------------------------- TASK CLASS BEGIN -------------------------------------------------------------------

class task:
    def __init__(self, release_time, period_prio, execution_time, deadline, id):
        # Initialize the task with its attributes
        self.release_time = release_time
        self.period_prio = period_prio
        self.execution_time = execution_time
        self.deadline = deadline
        self.id = id
        
    def __repr__(self):
        # Define the string representation for the task
        return (f" Id: {self.id} -- Task(Release Time: {self.release_time}, Period/Priority: {self.period_prio}, "
                f"Execution Time: {self.execution_time} "
                f"Deadline: {self.deadline})")
    
    def __lt__(self, other):
        # Define less than for priority comparison in the heap
        return (self.period_prio, self.id, self.release_time) < (other.period_prio, other.id, other.release_time)

#-------------------------------------------------------------------- TASK CLASS END -------------------------------------------------------------------

#-------------------------------------------------------------------- SIMULATE CLASS BEGIN -----------------------------------------------------------

class simulate_rms:
    
    def __init__(self, filename):
        # Initialize the simulation with necessary lists and variables
        self.initial_task_list = []
        self.running_task = None
        self.waiting_tasks = []  # This will be used as a heap
        self.preemptions = []
        self.event_list = []

        # Read the input file immediately
        self.read_file(filename)
        # Calculate the hyperperiod for the given task set
        self.hyperperiod = self.calculate_hyperperiod()

    def lcm(self, a, b):
        # Calculate the least common multiple of two numbers
        return abs(a * b) // gcd(int(a), int(b))

    def calculate_hyperperiod(self):
        # Calculate the hyperperiod by finding the LCM of task periods
        periods = [task.period_prio for task in self.initial_task_list]
        hyperperiod = reduce(self.lcm, periods)
        return hyperperiod

    def read_file(self, filename):
        # Read task parameters from the input file
        counter = 0
        with open(filename, 'r') as f:
            for line in f:
                # Convert values to float first, then multiply by 1000 and convert to int
                exec_time, period, deadline = map(lambda x: int(float(x) * 1000), line.strip().split(','))
                self.initial_task_list.append(task(release_time=0, period_prio=period, execution_time=exec_time, deadline=deadline, id=counter))
                counter += 1
    
    #static task generation
    def generate_repeating_tasks(self):
        # Generate repeating tasks for the entire hyperperiod
        for original_task in self.initial_task_list:
            current_time = 0
            while current_time < self.hyperperiod:
                new_release_time = current_time
                new_deadline = new_release_time + original_task.deadline
                # Create a new task instance with updated times
                new_task = task(release_time=new_release_time,
                                period_prio=original_task.period_prio,
                                execution_time=original_task.execution_time,
                                deadline=new_deadline,
                                id=original_task.id)
                # Add the new task to the event list
                self.event_list.append(new_task)
                # Update the current time to the next release time
                current_time += original_task.period_prio
                
        # Sort the event list based on release time, priority, and ID
        self.event_list.sort(key=lambda x: (x.release_time, x.period_prio, x.id))
        self.event_list = deque(self.event_list)
        
    def doing_sim(self):
        # Run the simulation for the RMS scheduling
        curr_time = 0
        curr_task = None
        while self.event_list or self.waiting_tasks:
            #case when we get to a task after hyper period
            if curr_time >= self.hyperperiod:
                return 0  # Stop simulation and return 0 as task missed its deadline
            
            prempt_flag = False
            
            # Check waiting tasks queue
            if self.waiting_tasks:
                # Pop the highest priority task from the heap
                curr_task = heapq.heappop(self.waiting_tasks)
                # If a task missed its deadline
                if curr_task.deadline < curr_time:
                    return 0 
            else:
                # Grab the top element from the event list
                curr_task = self.event_list.popleft()
                if curr_task.release_time > curr_time:
                    # Update current time to the release time of the next task
                    curr_time = curr_task.release_time  
            
            # Check if the task can be completed within its deadline
            if curr_time + curr_task.execution_time > curr_task.deadline:
                return 0  # Stop simulation and return 0 as task missed its deadline
            
            # Execute the current task
            task_end_time = curr_time + curr_task.execution_time

            # Check for preemption by a higher priority task
            while (self.event_list and self.event_list[0].release_time < task_end_time):
                #condition where preemption happens
                task = self.event_list[0]
                if task.period_prio < curr_task.period_prio:
                    prempt_flag = True
                    #so we dont go back into time
                    if task.release_time > curr_time:
                        self.preemptions[curr_task.id] += 1
                        curr_task.execution_time -= (task.release_time - curr_time)
                        curr_time = task.release_time
                    
                    heapq.heappush(self.waiting_tasks, curr_task)
                    heapq.heappush(self.waiting_tasks, task)
                    self.event_list.popleft()
                    break
                # Since we are using a deque we need to not pop elements from the middle so even if we are not preempting we add to the waiting
                # So we always have O(1) pop from the front
                else:
                    self.event_list.popleft()
                    heapq.heappush(self.waiting_tasks, task)
            
            if not prempt_flag:
                # No preemption occurred, complete the current task
                curr_time = task_end_time
                if curr_time > curr_task.deadline:
                    # print(f"Task {curr_task.id} missed its deadline.")
                    return 0
                
        return 1        
            
    def run(self):
        # Initialize preemptions list and generate repeating tasks
        self.preemptions = [0 for _ in range(len(self.initial_task_list))]
        self.generate_repeating_tasks()  # Populate event_list
        
        # Run the actual simulation
        result = self.doing_sim()

        if(result):
            print(result)
            print(','.join(map(str, self.preemptions)))
        else:
            print(result)

#-------------------------------------------------------------------- SIMULATE CLASS END -------------------------------------------------------------------

#-------------------------------------------------------------------- MAIN BEGIN -------------------------------------------------------------------

def main(filename):
    # Initialize the simulation class with the provided filename
    start_time = time.time()
    rms_simulate = simulate_rms(filename)
    rms_simulate.run()
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Execution time: {elapsed_time:.4f} seconds")
    
#-------------------------------------------------------------------- MAIN END -------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 ece_455_final.py <input_file>")
    else:
        main(sys.argv[1])
