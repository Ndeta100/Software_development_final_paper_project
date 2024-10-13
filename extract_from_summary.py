import xml.etree.ElementTree as ET
import csv

def extract_summary_to_csv(summary_file, output_csv):
    tree = ET.parse(summary_file)
    root = tree.getroot()

    # Extract data and write to CSV
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ["time", "loaded", "inserted", "running", "waiting", "ended", "arrived", "collisions", "teleports", "halting", "stopped", "meanWaitingTime", "meanTravelTime", "meanSpeed", "meanSpeedRelative"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for step in root.findall('step'):
            data = {
                "time": step.get("time"),
                "loaded": step.get("loaded"),
                "inserted": step.get("inserted"),
                "running": step.get("running"),
                "waiting": step.get("waiting"),
                "ended": step.get("ended"),
                "arrived": step.get("arrived"),
                "collisions": step.get("collisions"),
                "teleports": step.get("teleports"),
                "halting": step.get("halting"),
                "stopped": step.get("stopped"),
                "meanWaitingTime": step.get("meanWaitingTime"),
                "meanTravelTime": step.get("meanTravelTime"),
                "meanSpeed": step.get("meanSpeed"),
                "meanSpeedRelative": step.get("meanSpeedRelative"),
            }
            writer.writerow(data)

# Replace with your file paths
summary_file = 'summary.xml'
output_csv = 'summary_data.csv'

extract_summary_to_csv(summary_file, output_csv)
