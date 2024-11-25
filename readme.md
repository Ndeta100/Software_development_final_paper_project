## Overview
This project is a comprehensive simulation of urban traffic conditions in Tallinn, Estonia, using [Simulation of Urban Mobility (SUMO)](https://www.eclipse.org/sumo/). By employing open-source tools like SUMO, traCI, and Apache Airflow, the study seeks to explore and recommend cost-effective solutions for improving urban mobility in Tallinn without major infrastructure investments.

## Objectives
- Model traffic conditions in Tallinn using real-time and geospatial data from TomTom, OSM, and mobility surveys.
- Evaluate the impact of traffic optimization strategies, such as adaptive signaling and route management, on congestion and travel times.
- Analyze traffic behavior at critical intersections and congestion hotspots, with a particular focus on areas like Sikupilli, to recommend data-driven improvements.
- Propose scalable and sustainable mobility solutions that enhance existing urban transport strategies without significant physical infrastructure expansion.

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
├── travel_speed_comparison.png
└── write_edges.py
```

### Key Files
- **tallinn.osm.xml**: OpenStreetMap data of Tallinn, used to generate the road network.
- **tallinn.net.xml**: The SUMO network file generated from OSM data.
- **tallinn.sumocfg**: SUMO configuration file managing network, routes, and simulation settings.
- **lanesensors.add.xml**: Additional lane detectors to monitor traffic at specific locations.
- **morning_peak_8AM.rou.xml, evening_peak_6PM.rou.xml, off_peak_2AM.rou.xml, afternoon_traffic_2PM.rou.xml**: Route files for different times of the day to simulate realistic traffic scenarios.
- **parse_tom_tom.py**: Processes TomTom data for use in simulations.
- **random_lane_detector_placer.py**: Places lane detectors at random intersections.
- **summary.xml**: Output summary containing key statistics from simulations.
- **t-test.py**: Conducts statistical analysis, including t-tests, to compare traffic scenarios.
- **travel_speed_comparison.png**: Visual comparison of travel speed between Tom Tom and simulation results.

## Installation
To set up and run the project, follow these steps:

1. **Clone the Repository**
   ```sh
   git clone https://github.com/Ndeta100/Software_development_final_paper_project.git
   cd SUMO_WORK
   ```

2. **Requirements**
   Ensure you have the following software installed:
   - [SUMO](https://www.eclipse.org/sumo/)
   - [Python 3.x](https://www.python.org/downloads/)
   - Required Python Packages:
     ```sh
     pip install pandas matplotlib airflow
     ```

3. **Network Generation**
   Convert OSM data of Tallinn to a SUMO network:
   ```sh
   netconvert --osm-files estonia-latest.osm.pbf -o tallinn.net.xml
   ```

4. **Route Creation**
   Generate route files based on TomTom data:
   ```sh
   python parse_tom_tom.py
   ```

5. **Run the Simulation**
   Use the following command to run the simulation with SUMO:
   ```sh
   sumo -c tallinn.sumocfg
   ```

## Scenarios
### Traffic Scenarios Simulated
- **Morning Peak (8 AM)**: Represents traffic during commuting hours.
- **Evening Peak (6 PM)**: Models traffic during evening commute times.
- **Off-Peak (2 AM)**: Captures traffic flow during low activity periods.
- **Afternoon Traffic (2 PM)**: Represents moderate traffic during midday.

## Analysis and Results
1. **Travel Time Comparison**
   - A t-test conducted on travel times from real-world TomTom data vs simulation results showed a significant improvement in travel times with optimized signal timings and route management.

2. **Congestion Hotspots**
   - The Sikupilli area was identified as a major congestion hotspot. Targeted interventions in this area, including signal adjustments, led to reduced delays and increased average speeds.

3. **Teleportation Events**
   - Teleportation incidents, where vehicles get "stuck" and are removed, were tracked. These events highlighted critical areas needing improvements in traffic flow.

## Future Work
- **Adaptive Traffic Lights**: Implement real-time adaptive traffic signal control.
- **Autonomous Vehicles**: Explore the impact of AVs on urban traffic congestion.
- **Public Transport Integration**: Evaluate the effect of buses and shared mobility on traffic patterns.

## Contributing
Contributions are welcome to enhance simulation accuracy, add new analysis scripts, or improve documentation. Submit a pull request to collaborate.

## License
This project is licensed under the MIT License.

## Acknowledgments
- **SUMO Developers**: For providing an open-source platform for traffic simulation.
- **TomTom**: For traffic data used in the analysis.
- **OpenStreetMap**: For geographic data used in network generation.

---
This README reflects the project's latest iteration, incorporating feedback and advancements made in my thesis work on innovative mobility solutions for Tallinn, Estonia. Feel free to explore and contribute as we aim to make urban mobility smarter together.

