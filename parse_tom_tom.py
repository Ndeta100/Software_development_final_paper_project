import os
import xml.etree.ElementTree as ET

def update_vehicle_speed_and_ids(file_name, speed, vehicle_type_id, id_offset):
    if not os.path.exists(file_name) or os.path.getsize(file_name) == 0:
        raise ValueError(f"The file {file_name} is either missing or empty.")

    tree = ET.parse(file_name)
    root = tree.getroot()

    # Remove existing vType definitions if they exist
    for vtype in root.findall('vType'):
        root.remove(vtype)

    # Add new vehicle type with the specified speed
    vtype = ET.Element('vType', id=vehicle_type_id, maxSpeed=str(speed))
    root.insert(0, vtype)

    # Update each vehicle to reference the correct vehicle type and ensure unique IDs
    for i, vehicle in enumerate(root.findall('vehicle')):
        if 'maxSpeed' in vehicle.attrib:
            del vehicle.attrib['maxSpeed']  # Ensure 'maxSpeed' is completely removed from 'vehicle'
        vehicle.set('type', vehicle_type_id)
        vehicle.set('id', f"{vehicle.attrib['id']}_{id_offset + i}")  # Make ID unique by adding an offset

    tree.write(file_name)
    print(f"Updated {file_name} with type {vehicle_type_id}, maxSpeed {speed} km/h, and unique IDs.")

# Update vehicle speeds and IDs for each .rou.xml file
try:
    update_vehicle_speed_and_ids('morning_peak_8AM.rou.xml', 27, 'morningPeakType', 1000)  # Speed for 8 AM traffic
    update_vehicle_speed_and_ids('evening_peak_6PM.rou.xml', 24, 'eveningPeakType', 2000)  # Speed for 6 PM traffic
    update_vehicle_speed_and_ids('off_peak_2AM.rou.xml', 43, 'offPeakType', 3000)          # Speed for 2 AM traffic
    update_vehicle_speed_and_ids('afternoon_traffic_2PM.rou.xml', 31, 'afternoonType', 4000)  # Speed for 2 PM traffic

except ValueError as e:
    print(e)
