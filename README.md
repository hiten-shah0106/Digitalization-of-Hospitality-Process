# Digitalization-of-Hospitality-Process

This project is about the digitalization of the hospitality process, focusing on room allocation using Flask. The code includes functionality for parsing CSV files, processing room allocations based on group and hostel data, and generating downloadable results. Below is an overview and some key details about the implementation:

# Project Structure

- main.py: The main Flask application file.
- templates/index.html: HTML template for the upload form.
- templates/result.html: HTML template for displaying results.
- static/style.css: CSS file for styling the HTML pages.

# - main.py

# Imports and Setup:

Imports necessary libraries such as Flask, Pandas, CSV, and logging.
Configures logging to log information and errors.
Defines the Flask app.

# Helper Functions:

parse_gender_count(gender_str): Parses the gender string to count boys and girls in a group.

allocate_rooms(groups, hostels): Allocates rooms based on group and hostel data.

allocate_gender(group_id, gender, members, hostels): Allocates rooms for a specific gender.

# Flask Routes:

/ (index route): Handles the GET and POST requests for the main page. On POST, it processes the uploaded CSV files and allocates rooms.
/download: Generates and sends a CSV file of the room allocations.

# HTML Templates

- index.html:
  Contains a form for uploading the group and hostel CSV files.
  Displays any error messages if room allocation fails.

- result.html:
  Displays the room allocation results in a table format.

Provides a link to download the results as a CSV file.
Styling (style.css)
Styles the body, form, table, and other elements to create a clean and user-friendly interface.

# Example Usage

Upload CSV Files: Users upload the group and hostel information CSV files via the form on the main page.

Room Allocation: The backend processes the CSV files and allocates rooms based on the given logic.

View Results: The results are displayed on a new page, and users can download the results as a CSV file.

# Conclusion

This project showcases a practical application of Flask in managing hospitality processes and can be extended to include more features such as user authentication, advanced reporting, and integration with other services.
