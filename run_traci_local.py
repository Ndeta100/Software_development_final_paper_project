import traci
import sumolib
import numpy as np

# Paths to SUMO files
sumo_binary = "sumo-gui"
sumo_cfg_file = "tallinn.sumocfg"

# Initialize SUMO network to load edges for dynamic routing
net = sumolib.net.readNet("tallinn.net.xml")

# Constants for scenario configuration
WAIT_TIME_THRESHOLD = 10  # Seconds
LOG_INTERVAL = 50  # Frequency of log outputs

def run_sumo(is_intervention=False):
    # Prepare SUMO command
    sumo_cmd = [sumo_binary, "-c", sumo_cfg_file, "--verbose", "--message-log", "sumo_log.txt"]
    traci.start(sumo_cmd)
    
    # Initialize variables
    step = 0
    vehicle_entry_times = {}  # Dictionary to store each vehicle's entry time
    travel_times = []  # List to store calculated travel times
    rerouted_vehicles = set()  # Track vehicles rerouted to avoid repetition

    try:
        while step < 1000:
            traci.simulationStep()  # Advance the simulation by one step
            vehicles = traci.vehicle.getIDList()
            
            # Update entry times for new vehicles
            for vehicle_id in vehicles:
                if vehicle_id not in vehicle_entry_times:
                    vehicle_entry_times[vehicle_id] = step  # Record entry time
                
                # Check if vehicle has reached its destination
                if traci.vehicle.isStopped(vehicle_id):
                    exit_time = step
                    entry_time = vehicle_entry_times.pop(vehicle_id, None)
                    if entry_time is not None:
                        travel_time = exit_time - entry_time
                        travel_times.append(travel_time)
                        print(f"Vehicle {vehicle_id} completed its route with travel time: {travel_time} steps.")
                
                # Reroute vehicles with long waiting times in intervention scenario
                if is_intervention and traci.vehicle.getWaitingTime(vehicle_id) > WAIT_TIME_THRESHOLD and vehicle_id not in rerouted_vehicles:
                    new_route = find_alternate_route(vehicle_id)
                    if new_route:
                        traci.vehicle.setRoute(vehicle_id, new_route)
                        rerouted_vehicles.add(vehicle_id)
                        print(f"Step {step}: Vehicle {vehicle_id} rerouted due to high waiting time.")

            # Traffic light management in intervention scenario
            if is_intervention:
                traffic_light_ids = traci.trafficlight.getIDList()
                for tl in traffic_light_ids:
                    manage_traffic_lights(tl)

            # Log outputs at intervals
            if step % LOG_INTERVAL == 0:
                print(f"Step {step}: Total Vehicles Tracked: {len(travel_times)}")
            
            step += 1

    finally:
        traci.close()
        print("Simulation completed.")
        # Print travel time results summary
        print(f"Average Travel Time: {np.mean(travel_times):.2f} steps")
        print(f"Total Travel Times Collected: {len(travel_times)}")
        return np.array(travel_times)

def find_alternate_route(vehicle_id):
    current_edge = traci.vehicle.getRoadID(vehicle_id)
    if not current_edge:
        return None
    
    # Get next possible edges connected to the current edge
    next_edges = net.getEdge(current_edge).getOutgoing()
    next_edges_sorted = sorted(next_edges, key=lambda edge: traci.edge.getLastStepHaltingNumber(edge.getID()))
    alternate_route = [edge.getID() for edge in next_edges_sorted if edge.getID() != current_edge]
    
    if alternate_route:
        return alternate_route
    return None

def manage_traffic_lights(tl_id):
    lane_ids = traci.trafficlight.getControlledLanes(tl_id)
    waiting_vehicles = sum(traci.lane.getLastStepHaltingNumber(lane) for lane in lane_ids)
    
    if waiting_vehicles > 10:
        current_phase = traci.trafficlight.getPhase(tl_id)
        if current_phase % 2 == 0:  # Extend green phase for even-numbered phases
            traci.trafficlight.setPhaseDuration(tl_id, traci.trafficlight.getPhaseDuration(tl_id) + 10)
            print(f"Traffic light {tl_id} phase extended due to high waiting vehicles.")

# Run baseline and intervention simulations
baseline_travel_times = run_sumo(is_intervention=False)  # Baseline scenario
intervention_travel_times = run_sumo(is_intervention=True)  # Intervention scenario

# Print final summary and calculate differences
print("\nResults Summary:")
print(f"Baseline Average Travel Time: {np.mean(baseline_travel_times):.2f} steps")
print(f"Intervention Average Travel Time: {np.mean(intervention_travel_times):.2f} steps")

# Perform a comparison (e.g., statistical test) between baseline and intervention
from scipy import stats
t_stat, p_value = stats.ttest_ind(baseline_travel_times, intervention_travel_times)
print(f"T-statistic: {t_stat}, P-value: {p_value}")
