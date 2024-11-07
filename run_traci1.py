import os
import traci
import sumolib

# Paths to SUMO files
sumo_binary = "sumo-gui"  # Use "sumo" for command-line interface
sumo_cfg_file = "tallinn.sumocfg"

# Function to start SUMO with TraCI
def run_sumo(output_file_path):
    sumo_cmd = [sumo_binary, "-c", sumo_cfg_file]
    traci.start(sumo_cmd)

    step = 0

    try:
        with open(output_file_path, "a") as f:
            # Run the simulation step-by-step
            while step < 1000:
                traci.simulationStep()  # Advance the simulation by one step
                
                if step % 10 == 0:
                    traffic_light_ids = traci.trafficlight.getIDList()
                    for tl in traffic_light_ids:
                        traci.trafficlight.setPhase(tl, (step // 10) % 4)

                vehicles = traci.vehicle.getIDList()
                avg_speed = sum(traci.vehicle.getSpeed(v) for v in vehicles) / len(vehicles) if vehicles else 0
                
                # Save results to file
                f.write(f"Step {step}: Average Speed: {avg_speed:.2f} km/h\n")
                step += 1
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        traci.close()
        print("Simulation finished successfully.")

if __name__ == "__main__":
    run_sumo("/opt/airflow/sumo_work/simulation_output.txt")
