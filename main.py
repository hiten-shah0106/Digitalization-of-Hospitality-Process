from flask import Flask, render_template, request, send_file, url_for
import csv
import io
import pandas as pd
import logging

app = Flask(__name__, static_url_path='/static')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_gender_count(gender_str): # Parses the gender string to count boys and girls in a group.
    counts = {'Boys': 0, 'Girls': 0}

    if isinstance(gender_str, str):
        try:
            if '&' in gender_str:
                parts = gender_str.split('&')
                for part in parts:
                    count, gender = part.strip().split(' ', 1)
                    counts[gender] = int(count)
            else:
                count, gender = gender_str.strip().split(' ', 1)
                counts[gender] = int(count)
        except ValueError as e:
            logger.error(f"Error parsing gender count: {e}")
            logger.error(f"Gender string: {gender_str}")
    
    return counts

def allocate_rooms(groups, hostels): # Allocates rooms based on group and hostel data.
    allocations = []
    
    hostels = hostels.sort_values('Capacity', ascending=False)
    
    for _, group in groups.iterrows():
        group_id = group['Group ID']
        members = int(group['Members'])
        gender = group['Gender']
        
        gender_counts = parse_gender_count(gender)
        
        if gender_counts['Boys'] > 0 and gender_counts['Girls'] > 0:
            boys_allocated = allocate_gender(group_id, 'Boys', gender_counts['Boys'], hostels)
            girls_allocated = allocate_gender(group_id, 'Girls', gender_counts['Girls'], hostels)
            allocations.extend(boys_allocated)
            allocations.extend(girls_allocated)
        elif gender == 'Boys' or gender_counts['Boys'] > 0:
            allocations.extend(allocate_gender(group_id, 'Boys', members, hostels))
        elif gender == 'Girls' or gender_counts['Girls'] > 0:
            allocations.extend(allocate_gender(group_id, 'Girls', members, hostels))
        else:
            logger.warning(f"Unrecognized gender format for group {group_id}: {gender}")
    
    return allocations

def allocate_gender(group_id, gender, members, hostels): # Allocates rooms for a specific gender.
    allocations = []
    remaining = int(members)
    
    for _, room in hostels.iterrows():
        if room['Gender'] != gender or room['Capacity'] == 0:
            continue
        
        hostel_name = room['Hostel Name']
        room_number = room['Room Number']
        capacity = room['Capacity']
        
        if remaining <= capacity:
            allocations.append({
                'Group ID': group_id,
                'Hostel Name': hostel_name,
                'Room Number': room_number,
                'Members Allocated': remaining
            })
            room['Capacity'] -= remaining
            break
        else:
            allocations.append({
                'Group ID': group_id,
                'Hostel Name': hostel_name,
                'Room Number': room_number,
                'Members Allocated': capacity
            })
            remaining -= capacity
            room['Capacity'] = 0
    
    return allocations

@app.route('/', methods=['GET', 'POST'])
def index(): # Main route for the application.
    if request.method == 'POST':
        groups_file = request.files['groups']
        hostels_file = request.files['hostels']
        
        try:
            groups = pd.read_csv(groups_file)
            hostels = pd.read_csv(hostels_file)
            
            allocations = allocate_rooms(groups, hostels)
            
            return render_template('result.html', allocations=allocations)
        except Exception as e:
            logger.exception("An error occurred during room allocation")
            error_message = f"An error occurred: {str(e)}"
            return render_template('index.html', error=error_message)
    
    return render_template('index.html')

@app.route('/download')
def download(): # Allowing the user to download the room allocations as a CSV file.
    allocations = eval(request.args.get('allocations'))
    
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=['Group ID', 'Hostel Name', 'Room Number', 'Members Allocated'])
    writer.writeheader()
    writer.writerows(allocations)
    
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name='room_allocations.csv'
    )

if __name__ == '__main__':
    app.run(debug=True)
