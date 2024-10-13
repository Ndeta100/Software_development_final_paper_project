
## Overview
This project is a comprehensive simulation of urban traffic conditions using [Simulation of Urban Mobility (SUMO)](https://www.eclipse.org/sumo/), a well-known open-source traffic simulation package. The project focuses on modeling the traffic flow in Tallinn, Estonia, to address congestion, optimize traffic control, and evaluate the impact of infrastructure changes. Through multiple simulation scenarios, the project aims to demonstrate the effectiveness of optimized traffic solutions compared to non-optimized road conditions.

## Objectives
- Model traffic conditions in Tallinn, Estonia, using realistic data from sources like TomTom and OSM.
- Evaluate the impact of optimized traffic solutions, such as adaptive signaling and lane expansion, on traffic flow and congestion.
- Generate insights on traffic behavior at critical intersections and arterial roads during different times of the day, using data-driven statistical analysis.

## Project Structure
The project files are organized as follows:

```
SUMO_WORK/
├── add_edges_taz.py
├── afternoon_traffic_2PM.rou.xml
├── edgedata.xml
├── estonia-latest.osm.pbf
├── evening_peak_6PM.rou.xml
├── extract_from_summary.py
├── lanesensors.add.xml
├── morning_peak_8AM.rou.xml
├── off_peak_2AM.rou.xml
├── parse_tom_tom.py
├── random_lane_detector_placer.py
├── routes.rou.xml
├── summary_data.csv
├── summary.xml
├── t-test.py
├── tallinn.net.xml
├── tallinn.osm.xml
├── tallinn.sumocfg
├── travel_times_comparison.png
└── write_edges.py
```

### Key Files
- **tallinn.osm.xml**: The OpenStreetMap data of Tallinn, Estonia, used as the base for generating the traffic network.
- **tallinn.net.xml**: The generated SUMO network file for Tallinn based on the OSM data.
- **tallinn.sumocfg**: The SUMO configuration file that manages the input network, route files, and other configurations for the simulation.
- **lanesensors.add.xml**: Additional sensors (lane detectors) placed on specific road segments to monitor traffic.
- **morning_peak_8AM.rou.xml, evening_peak_6PM.rou.xml, off_peak_2AM.rou.xml, afternoon_traffic_2PM.rou.xml**: Route files representing traffic during different times of the day.
- **parse_tom_tom.py**: Script for processing traffic data obtained from TomTom to be used in the simulation.
- **random_lane_detector_placer.py**: Places lane detectors at random locations to monitor specific intersections.
- **summary.xml**: The output summary containing key statistics about the simulation run.
- **t-test.py**: Python script to conduct statistical analysis, including t-tests on traffic data.
- **travel_times_comparison.png**: Visual representation of the comparison of travel times between optimized and non-optimized traffic scenarios.

## Installation
To set up and run the project, follow these steps:

1. **Clone the Repository**
   ```sh
   git clone https://github.com/YourUsername/SUMO-Traffic-Simulation.git
   cd SUMO_WORK
   ```

2. **Requirements**
   Ensure you have the following software installed:
   - [SUMO](https://www.eclipse.org/sumo/): SUMO Traffic Simulator.
   - [Python 3.x](https://www.python.org/downloads/): Used for preprocessing and analysis.
   - Required Python Packages: Install using pip:
     ```sh
     pip install pandas matplotlib
     ```

3. **Network Generation**
   Convert the OSM data of Tallinn to a SUMO network using the following command:
   ```sh
   netconvert --osm-files estonia-latest.osm.pbf -o tallinn.net.xml
   ```

4. **Route Creation**
   Create route files based on the TomTom traffic data for peak and off-peak hours. The `parse_tom_tom.py` script extracts relevant data for generating routes, which are saved as separate `.rou.xml` files representing different traffic scenarios.

5. **Adding Edges**
   Use the `add_edges_taz.py` and `write_edges.py` scripts to add additional edges to the network as required, to better represent traffic conditions and enhance simulation accuracy.

6. **Run the Simulation**
   To run the SUMO simulation using the configuration file, execute:
   ```sh
   sumo -c tallinn.sumocfg
   ```

## Scenarios
### Simulation Scenarios
- **Morning Peak (8 AM)**: Represents high traffic congestion during commuting hours.
- **Evening Peak (6 PM)**: Models traffic during the return commute period.
- **Off-Peak (2 AM)**: Captures traffic during times of minimal activity.
- **Afternoon Traffic (2 PM)**: Moderate traffic scenario for midday congestion.

Each of these scenarios has corresponding route files to represent vehicle flow, which are loaded into SUMO for detailed simulation.

### Peak Hour Extraction from TomTom Data
The route files were generated based on peak hour data extracted from TomTom. Using the `parse_tom_tom.py` script, we processed traffic data to identify peak travel times and typical congestion periods. The resulting `.rou.xml` files are used in the simulation to represent realistic urban traffic scenarios during these times.

## Analysis and Results
1. **Comparison of Travel Times**
   The project includes a comprehensive comparison of travel times between optimized and non-optimized road conditions. Results from the t-test indicate that the travel times are significantly different, supporting the hypothesis that optimized traffic solutions effectively reduce congestion.

2. **Key Bottlenecks**
   Specific areas, such as the Sikupilli intersection, were identified as bottlenecks where congestion and teleportation of vehicles occurred. These insights highlight the need for targeted infrastructure improvements and better traffic signal management.

3. **Teleportation Events**
   Teleportation events, visible in the `travel_times_comparison.png`, represent severe congestion that causes vehicles to get "stuck" and eventually removed from the network. Addressing these points can greatly improve the robustness of the traffic system.

## Insights Gleaned
- **Urban Bottlenecks**: Congestion frequently occurs at major intersections, especially along arterial routes in Tallinn, such as Peterburi tee and Tartu maantee. The simulation's zoomed-in view of these intersections helps in pinpointing necessary improvements.
- **Benefits of Optimization**: Optimized solutions such as adaptive signaling showed a significant decrease in average travel times, as evidenced by the t-statistics and p-values generated during the analysis.

## Future Work
- **Adaptive Traffic Lights**: Integrating real-time adaptive traffic lights and comparing their effects with pre-programmed signals.
- **Autonomous Vehicles**: Investigate the impact of autonomous vehicles on reducing congestion under optimized road conditions.
- **Public Transportation Integration**: Include buses and evaluate their effect on traffic patterns and congestion.

## Contributing
If you wish to contribute, please fork the repository and submit a pull request. Contributions are welcome to improve simulation models, add new analysis scripts, or enhance documentation.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Acknowledgments
- **SUMO Developers**: For providing an open-source platform for traffic simulation.
- **TomTom**: For the traffic data used in analysis and modeling.
- **OpenStreetMap**: For the detailed map data used to build the road network.

---
Feel free to explore and modify the project to suit specific traffic management problems. Let's make urban mobility smarter together!