import grpc
import os
import re
import sys
import csv
from concurrent import futures
from tollingvision_scsinfo import TollingVisionServiceStub, EventRequest, SearchRequest, Image

def list_files_recursively(folder):
    file_list = []
    for root, _, files in os.walk(folder):
        for file in files:
            if re.match(r'.*\.(png|jpg|bmp)$', file.lower()):
                file_list.append(os.path.join(root, file))
    return file_list

def group_images(files, group_regex):
    groups = {}
    group_pattern = re.compile(group_regex)
    for file in files:
        match = group_pattern.match(os.path.basename(file))
        if match:
            group = match.group()
            if group not in groups:
                groups[group] = []
            groups[group].append(file)
    return groups

def create_event_request(files, front_regex, rear_regex, overview_regex):
    front_requests = []
    rear_requests = []
    overview_requests = []
    front_pattern = re.compile(front_regex)
    rear_pattern = re.compile(rear_regex)
    overview_pattern = re.compile(overview_regex)

    for file in files:
        with open(file, 'rb') as f:
            image_data = f.read()
        
        search_request = SearchRequest(image=Image(data=image_data))

        if overview_pattern.match(os.path.basename(file)):
            search_request.make_and_model_recognition = True
            overview_requests.append(search_request)
        elif front_pattern.match(os.path.basename(file)):
            front_requests.append(search_request)
        elif rear_pattern.match(os.path.basename(file)):
            rear_requests.append(search_request)
    
    if not front_requests and not rear_requests and not overview_requests:
        return None
    
    return EventRequest(front_request=front_requests, rear_request=rear_requests, overview_request=overview_requests)

def format_plate(plate):
    return f"{plate.text} {plate.country} {plate.state} {plate.category} ({plate.confidence})"

def format_mmr(mmr):
    return f"{mmr.make} {mmr.model} ({mmr.category} {mmr.view_point} {mmr.color})"

def main():
    if len(sys.argv) != 10:
        print("Usage: python3 tollingvision-sample.py <service_url> <secured> <max_parallel_requests> <image_folder_path> <csv_file_path> <group_regex> <front_regex> <rear_regex> <overview_regex>")
        sys.exit(1)

    service_url = sys.argv[1]
    secured = sys.argv[2].lower() == 'true'
    max_parallel_requests = int(sys.argv[3])
    image_folder_path = sys.argv[4]
    csv_file_path = sys.argv[5]
    group_regex = sys.argv[6]
    front_regex = sys.argv[7]
    rear_regex = sys.argv[8]
    overview_regex = sys.argv[9]

    if secured:
        channel = grpc.secure_channel(service_url, grpc.ssl_channel_credentials())
    else:
        channel = grpc.insecure_channel(service_url)
    
    stub = TollingVisionServiceStub(channel)
    image_files = list_files_recursively(image_folder_path)
    grouped_images = group_images(image_files, group_regex)

    print("Total analyze service calls:", len(grouped_images))

    with open(csv_file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Front Image", "Rear Image", "Overview Image", "Node", "Front Plate", "Front Plate Alternative", "Rear Plate", "Rear Plate Alternative", "MMR", "MMR Alternative"])

        def analyze_group(group, files):
            print("Processing group:", group)
            event_request = create_event_request(files, front_regex, rear_regex, overview_regex)
            if event_request is None:
                return

            responses = stub.analyze(event_request)
            for response in responses:
                if response.HasField('event_result'):
                    result = response.event_result
                    overview_files_list = [f for f in files if re.match(overview_regex, os.path.basename(f))]
                    front_files_list = [f for f in files if re.match(front_regex, os.path.basename(f)) and f not in overview_files_list]
                    rear_files_list = [f for f in files if re.match(rear_regex, os.path.basename(f)) and f not in overview_files_list]

                    front_files = "|".join(front_files_list)
                    rear_files = "|".join(rear_files_list)
                    overview_files = "|".join(overview_files_list)

                    front_plate = format_plate(result.front_plate) if result.HasField('front_plate') else ""
                    front_plate_alt = "|".join(format_plate(p) for p in result.front_plate_alternative)
                    rear_plate = format_plate(result.rear_plate) if result.HasField('rear_plate') else ""
                    rear_plate_alt = "|".join(format_plate(p) for p in result.rear_plate_alternative)
                    mmr = format_mmr(result.mmr) if result.HasField('mmr') else ""
                    mmr_alt = "|".join(format_mmr(m) for m in result.mmr_alternative)

                    csv_writer.writerow([front_files, rear_files, overview_files, result.node, front_plate, front_plate_alt, rear_plate, rear_plate_alt, mmr, mmr_alt])

        with futures.ThreadPoolExecutor(max_workers=max_parallel_requests) as executor:
            future_to_group = {executor.submit(analyze_group, group, files): group for group, files in grouped_images.items()}
            for future in futures.as_completed(future_to_group):
                group = future_to_group[future]
                try:
                    future.result()
                except Exception as e:
                    print(f"Group {group} generated an exception: {e}")

    channel.close()

if __name__ == '__main__':
    main()
