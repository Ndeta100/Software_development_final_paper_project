import traci
import sumolib

# Paths to SUMO files
sumo_binary = "sumo-gui"
sumo_cfg_file = "tallinn.sumocfg"

# Lower threshold for rerouting and logging intervals
WAIT_TIME_THRESHOLD = 10  # Seconds
LOG_INTERVAL = 50  # Frequency of log outputs

# Initialize SUMO network to load edges for dynamic routing
net = sumolib.net.readNet("tallinn.net.xml")

def run_sumo(is_intervention=False):
    sumo_cmd = [sumo_binary, "-c", sumo_cfg_file, "--verbose", "--message-log", "sumo_log.txt"]
    traci.start(sumo_cmd)
    
    step = 0
    vehicle_waiting_times = {}
    rerouted_vehicles = set()  # Track vehicles rerouted to avoid repetition
    entry_times = {}  # Track entry time of each vehicle
    travel_times = []  # Store travel times for analysis
    results = []  # Store step-by-step results

    try:
        while step < 1000:
            traci.simulationStep()  # Advance the simulation by one step
            vehicles = traci.vehicle.getIDList()
            
            # Calculate average speed and total waiting time
            total_speed = sum(traci.vehicle.getSpeed(v) for v in vehicles)
            avg_speed = total_speed / len(vehicles) if vehicles else 0
            avg_speed_kmh = avg_speed * 3.6
            total_waiting_time = sum(vehicle_waiting_times.get(v, 0) for v in vehicles)
            
            # Update waiting times, track entry times, and handle rerouting
            for vehicle_id in vehicles:
                # Track entry time
                if vehicle_id not in entry_times:
                    entry_times[vehicle_id] = step

                # Update waiting times
                if traci.vehicle.getSpeed(vehicle_id) < 0.1:  # Vehicle is stopped
                    vehicle_waiting_times[vehicle_id] = vehicle_waiting_times.get(vehicle_id, 0) + 1
                else:
                    vehicle_waiting_times[vehicle_id] = 0  # Reset if vehicle starts moving

                # Reroute if waiting time exceeds threshold and it's an intervention
                if is_intervention and vehicle_waiting_times[vehicle_id] >= WAIT_TIME_THRESHOLD:
                    new_route = find_alternate_route(vehicle_id)
                    if new_route and vehicle_id not in rerouted_vehicles:
                        traci.vehicle.setRoute(vehicle_id, new_route)
                        rerouted_vehicles.add(vehicle_id)
                        print(f"Step {step}: Vehicle {vehicle_id} rerouted due to high waiting time.")

            # Check for vehicles that have arrived at their destinations
            arrived_vehicles = traci.simulation.getArrivedIDList()
            for vehicle_id in arrived_vehicles:
                # Calculate travel time and store it
                travel_time = step - entry_times[vehicle_id]
                travel_times.append(travel_time)
                print(f"Vehicle {vehicle_id} completed its route in {travel_time} seconds.")
                # Remove vehicle from tracking dictionaries
                entry_times.pop(vehicle_id, None)
                vehicle_waiting_times.pop(vehicle_id, None)

            # Traffic light management in intervention scenario
            if is_intervention:
                traffic_light_ids = traci.trafficlight.getIDList()
                for tl in traffic_light_ids:
                    manage_traffic_lights(tl)

            # Store metrics for analysis
            results.append({
                "Step": step,
                "Average Speed (km/h)": avg_speed_kmh,
                "Total Waiting Time (s)": total_waiting_time,
                "Rerouted Vehicles": len(rerouted_vehicles)
            })

            # Log outputs at intervals
            if step % LOG_INTERVAL == 0:
                print(f"Step {step}: Avg Speed: {avg_speed_kmh:.2f} km/h, Total Waiting Time: {total_waiting_time}, Rerouted: {len(rerouted_vehicles)}")
            
            step += 1

    finally:
        traci.close()
        print("Simulation completed.")
        # Print final summary of results
        print("\nFinal Summary:")
        for result in results:
            print(result)
        # Display average travel time
        if travel_times:
            avg_travel_time = sum(travel_times) / len(travel_times)
            print(f"\nAverage Travel Time: {avg_travel_time:.2f} seconds")

def find_alternate_route(vehicle_id):
    current_edge = traci.vehicle.getRoadID(vehicle_id)
    if not current_edge:
        return None
    
    # Get the next possible edges connected to the current edge
    next_edges = net.getEdge(current_edge).getOutgoing()
    # Sort edges by congestion level, preferring less congested ones
    next_edges_sorted = sorted(next_edges, key=lambda edge: traci.edge.getLastStepHaltingNumber(edge.getID()))
    # Return the least congested alternative route
    alternate_route = [edge.getID() for edge in next_edges_sorted if edge.getID() != current_edge]
    
    if alternate_route:
        print(f"Alternate route for Vehicle {vehicle_id}: {alternate_route}")
        return alternate_route
    else:
        print(f"No alternate route found for Vehicle {vehicle_id}")
        return None

def manage_traffic_lights(tl_id):
    lane_ids = traci.trafficlight.getControlledLanes(tl_id)
    waiting_vehicles = sum(traci.lane.getLastStepHaltingNumber(lane) for lane in lane_ids)
    
    # Adjust phase if waiting vehicles exceed threshold
    if waiting_vehicles > 10:
        current_phase = traci.trafficlight.getPhase(tl_id)
        if current_phase % 2 == 0:  # Extend green phase for even-numbered phases
            traci.trafficlight.setPhaseDuration(tl_id, traci.trafficlight.getPhaseDuration(tl_id) + 10)
            print(f"Traffic light {tl_id} phase extended due to high waiting vehicles.")

# Run both baseline and intervention scenarios
run_sumo(is_intervention=False)  # Baseline scenario
run_sumo(is_intervention=True)   # Intervention scenario
