###Author:Mohamed Basim
###Date:08/12/2024
###Student ID:20241628

import csv
import os

# Purpose: This function checks if a given date is valid based on the specified format.
def validate_date_input():#A function to validate a date.
#The validation is done using three separate while loops for the day, month, and year.

    while True:
        try:
#The user is prompted to input values for the date within the valid range.
            dd = int(input("Please enter the day of the survey in the format dd (1-31): "))
            if 1 <= dd <= 31:
                break
            else:
                print("Error: Day must be in the range 1 to 31.")#If the input is invalid, an error message is displayed to notify the user.

#If the user inputs a value other than an integer, the error handling mechanism will address it appropriately.
        except ValueError:
            print("Error: Input must be an integer. Please try again.")


    while True:
        try:
#The user is prompted to input values for the date within the valid range.
            mm = int(input("Please enter the month of the survey in the format MM (1-12): "))
            if 1 <= mm <= 12:
                break
            else:
                print("Error: Month must be in the range 1 to 12.")#If the input is invalid, an error message is displayed to notify the user.

#If the user inputs a value other than an integer, the error handling mechanism will address it appropriately.
        except ValueError:
            print("Error: Input must be an integer. Please try again.")



    while True:
        try:
#The user is prompted to input values for the date within the valid range.
            yyyy = int(input("Please enter the year of the survey in the format yyyy (2000-2024): "))
            if 2000 <= yyyy <= 2024:
                break
            else:
                print("Error: Year must be in the range 2000 to 2024.")#If the input is invalid, an error message is displayed to notify the user.


#If the user inputs a value other than an integer, the error handling mechanism will address it appropriately.
        except ValueError:
            print("Error: Input must be an integer. Please try again.")


#Format the day and month to always have two digits and convert the year to a string
    formatted_date = [f"{dd:02d}", f"{mm:02d}", str(yyyy)]

#Print a success message showing the formatted date in dd/mm/yyyy format
    print(f"Date added successfully: {'/'.join(formatted_date)}")

#Return the day, month, and year as individual values
    return dd, mm, yyyy


def process_csv_data(file_path):
    try:
        #Check if the specified file path exists
        if os.path.exists(file_path):
        #Open the file moode in read mode.
            with open(file_path, "r") as file:
        #Create a DictReader object to read the csv file as a list of dictionaries
        #Reads a csv file and maps the rows to dictionaries.
                file_reader = csv.DictReader(file)
                return list(file_reader)#Return the content of the file as a list of dictionaries
        else:
        #If the file path does not exist, handle the case
            print(f"No file found with the name {file_path}")#Printing massage that file is not found
            return None #Return None to indicate the absence of the file

#Handle any exceptions that occur during file processing
    except Exception as e:
        print(f"An error occurred while processing the file: {e}")#Print the error type as "e"
        return None




def display_outcomes(outcomes):
    
    #Calculate the total number of vehicles
    total_vehcls = len(outcomes)


    #Calculate the total number of trucks
    total_trks = 0
    for row in outcomes:
        if row.get('VehicleType') == 'Truck':
            total_trks += 1


    #Calculate the total number of electric/hybrid vehicles
    total_elc_vehcls = 0
    for row in outcomes:
        if row.get('elctricHybrid') == 'True':
            total_elc_vehcls += 1

    #Calculate the total number of two-wheeled vehicles
    total_two_wheeld = 0
    for row in outcomes:
        if row.get('VehicleType') in ['Bicycle', 'Motorcycle', 'Scooter']:
            total_two_wheeld += 1


    #Count the number of buses heading north from Elm Avenue/Rabbit Road junction
    bus_north = 0
    for row in outcomes:
        if row.get("VehicleType") == "Buss" and row.get("JunctionName") == "Elm Avenue/Rabbit Road" and row.get("travel_Direction_out") == "N":
            bus_north += 1

    #Count vehicles passing straight through both junctions
    total_vehicles_straight = 0
    for row in outcomes:
        if row.get("travel_Direction_in") == row.get("travel_Direction_out"):
            total_vehicles_straight += 1

    #Calculate the percentage of trucks
    trucks_percentage = 0
    if total_vehcls > 0:
        trucks_percentage = f"{round((total_trks / total_vehcls) * 100)}%"


    #Count the total number of bicycles
    total_bicycles = 0
    for row in outcomes:
        if row.get('VehicleType') == 'Bicycle':
            total_bicycles += 1

    #Calculate the average number of bicycles per hour
    total_hours = 24  #Assuming data for one full day
    avg_bicycles_per_hour = round(total_bicycles / total_hours) if total_hours > 0 else 0


    #Count vehicles that exceeded the speed limit
    over_speed = 0
    for row in outcomes:
        try:
            vehicle_speed = int(row.get("VehicleSpeed", 0))
            speed_limit = int(row.get("JunctionSpeedLimit", 0))
            if vehicle_speed > speed_limit > 0:
                over_speed += 1
        except ValueError:
            #Skip rows with invalid speed data
            continue


    #Count total vehicles and scooters at a specific junction Elm Avenue/Rabbit Road
    total_elm_rabbit_vehicles = 0
    total_scooters_elm_ave = 0
    for row in outcomes:
        if row.get("JunctionName") == "Elm Avenue/Rabbit Road":
            total_elm_rabbit_vehicles += 1
            if row.get("VehicleType") == "Scooter":
                total_scooters_elm_ave += 1

    #Calculate the percentage of scooters at Elm Avenue/Rabbit Road
    scooters_percentage_elm_ave = 0
    if total_elm_rabbit_vehicles > 0:
        scooters_percentage_elm_ave = int((total_scooters_elm_ave / total_elm_rabbit_vehicles) * 100)


    #Analyze peak traffic data for a specific junction Hanley Highway/Westway
    peak_traffic_data = {}
    total_hanley_vehicles = 0  # Total vehicles at Hanley Highway/Westway
    for row in outcomes:
        if row.get("JunctionName") == "Hanley Highway/Westway":
            total_hanley_vehicles += 1  # Increment the total count
            time_of_day = row.get("timeOfDay", "00:00")
            if ":" in time_of_day:
                hour = time_of_day.split(":")[0]
                peak_traffic_data[hour] = peak_traffic_data.get(hour, 0) + 1

    #Busiest hour at the junction
    max_vehicles_hnl_west = max(peak_traffic_data.values(), default=0)
    busiest_hours_hnl_west = [
        hour for hour, count in peak_traffic_data.items() if count == max_vehicles_hnl_west
    ]


   #Formating the busiest hour ranges for print
    busiest_hour_ranges_hnl_west = ", ".join(
        [f"Between {hour}:00 and {int(hour) + 1:02d}:00" for hour in sorted(busiest_hours_hnl_west)]
    ) if busiest_hours_hnl_west else "No Data"



    #Count the total hours with light rain
    # Track hours with rain
    total_rain_hrs = 0
    rainfall_hour = set()  # To store unique hours with rain

    for row in outcomes:
        weather = row.get("Weather_Conditions", "")  # Assuming "weather" is a key in each row
        time_day = row.get("timeOfDay", "")  # Assuming "timeOfDay" is a key in each row
        
        if "Rain" in weather:  # Checks if the weather includes rain
            rain_time_components = time_day.split(":")  # Split time into hours and minutes
            rain_hour_string = rain_time_components[0]  # Get the hour portion
            rainfall_hour.add(rain_hour_string)  # Add the hour to the set

    # Calculate total hours of rain
    total_rain_hrs = len(rainfall_hour)



    #Compile results into a dictionary as keys and values
    results = {
        "The Total Number of Vehicles": total_vehcls,
        "The Total Number of Trucks": total_trks,
        "The Total Number of Electric Vehicles": total_elc_vehcls,
        "The Number of Two Wheeled Vehicles": total_two_wheeld,
        "Number of Buses Leaving Elm Avenue/Rabbit Road Junction Heading North": bus_north,
        "Number of Vehicles Passing Straight Through Both Junctions": total_vehicles_straight,
        "The Percentage of Trucks": trucks_percentage,
        "The Average Number of Bicycles Per Hour": avg_bicycles_per_hour,
        "The Number of Vehicles Over the Speed Limit": over_speed,
        "Total Vehicles at Elm Avenue/Rabbit Road": total_elm_rabbit_vehicles,
        "Percentage of Scooters at Elm Avenue/Rabbit Road": scooters_percentage_elm_ave,
        "The Highest Number of Vehicles in an Hour on Hanley Highway/Westway": max_vehicles_hnl_west,
        "Total Vehicles at Hanley Highway/Westway": total_hanley_vehicles,  
        "Busiest Traffic Hour Ranges on Hanley Highway/Westway": busiest_hour_ranges_hnl_west,
        "Total Rainy Hours": total_rain_hrs,
        
    }
    return results #Return the results dictionary

def save_results_to_file(results_list, file_name="results.txt"):
    with open(file_name, mode='a') as file:  #Use 'a' to append the file
        #Write a title for the results in the file
        file.write("Traffic Analysis Results:\n")
        #Iterate through the list of results and filenames
        for results, filename in results_list:
            file.write(f"\n--- Results from {filename} ---\n")  #Print the filename
            #Write each key-value pair from the results dictionary
            for key, value in results.items():
                file.write(f"{key}: {value}\n")
        file.write("\n")#Add a blank line at the end of the file" what the reason for this 

"""By adding a blank line at the end,
the last section of the content is clearly
separated from any future content""" 


# Task D: Histogram Display

import tkinter as tk

class HistogramApp:
    def __init__(self, traffic_data, date):# __init__ is a inbuilt function called by default
        """
        Initializes the histogram application with the traffic data and selected date.
        """
        self.traffic_data = traffic_data  # Allocating a variable for store the traffic data for histogram
        self.date = date # Alocating a variable to store the selected date for display as histogram title
        self.root = tk.Tk() # By imported module tkinter creates the main application window
        self.root.title(f"Traffic Data Histogram - {date}") # Setting the title
        self.canvas = None # Assign canvas to draw histogram 
        self.bar_width = 15 # Set the width of each bar in the histogram
        self.padding_x = 30 # Set horizontal padding for the histogram layout
        self.padding_y = 80 # Set vertical padding for the histogram layout
        self.x_label_offset = 25 # Set the offset for positioning labels on the x-axis
        self.y_label_offset = 20 # Set the offset for positioning labels on the y-axis
        self.colors = ['lightgreen', 'lightpink'] # Assign color for for the histogram bars
        self.histogram_data = {} # An empty dictionary to store histogram data
        self.max_count = 0 # Maximum count value for scaling the histogram
        self.prepare_histogram_data() # Process and prepare the data for the histogram

    def setup_window(self):
        """
        Sets up the Tkinter window and canvas for the histogram.
        """
        self.root.geometry("1200x600")
        self.canvas = tk.Canvas(self.root, bg="white") # Setting a background color for hsitogram 
        self.canvas.pack(fill=tk.BOTH, expand=True) # Add canvas to the window and make it resize to fill empty space

    def prepare_histogram_data(self):
        """
        Prepares the data for the histogram by counting vehicles per hour for each junction.
        """
        # Define the junctions to be included in the histogram
        junctions = ["Elm Avenue/Rabbit Road", "Hanley Highway/Westway"]

        # Allocate a dictionary to store hourly vehicle counts for each junction
        hourly_counts = {junction: [0 for _ in range(24)] for junction in junctions} # "_" loop variable is intentionally ignored

        # Loop through the traffic data to generate hourly vehicle counts
        for row in self.traffic_data:
            junction = row.get("JunctionName")
            time_of_day = row.get("timeOfDay", "00:00")
            # Check if the time is valid and the junction is in the hourly counts dictionary
            if ":" in time_of_day and junction in hourly_counts:
                hour = int(time_of_day.split(":")[0])
                hourly_counts[junction][hour] += 1

        self.histogram_data = hourly_counts #Store the processed data in the histogram_data attribute

        # Finding the maximum vehicle count among all hours and junctions for scaling purpos
        self.max_count = max(max(counts) for counts in hourly_counts.values())



    def draw_histogram(self):
        """
        Draws the histogram with axes, labels, and bars on a tkinter canvas
        """
        if not self.traffic_data:
            print("No data to display")
            return

        junctions = list(self.histogram_data.keys())
        canvas_width = 1200
        canvas_height = 600
        bar_chart_height = canvas_height - self.padding_y * 2
        self.canvas.config(width=canvas_width, height=canvas_height)

        start_x = self.padding_x
        axis_bottom = canvas_height - self.padding_y

        # Calculate the end of the x-axis based on the last bar
        end_x = start_x + 24 * (self.bar_width * 2 + self.padding_x) - self.padding_x + self.bar_width

        # Draw X-axis (extending to the end of the bars)
        self.canvas.create_line(start_x, axis_bottom, end_x, axis_bottom, fill="black", width=2)

        # Draw bars and X-axis labels
        for hour in range(24):
            x1 = start_x + hour * (self.bar_width * 2 + self.padding_x)

            for i, junction in enumerate(junctions):
                count = self.histogram_data[junction][hour]
                x2 = x1 + self.bar_width
                y1 = axis_bottom
                y2 = y1 - (count / self.max_count) * bar_chart_height

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.colors[i], outline="black")

                # Display the count above the bar
                self.canvas.create_text((x1 + x2) / 2, y2 - 10, text=str(count), font=("Arial", 9), anchor=tk.S)

                x1 += self.bar_width

            # Draw hour label
            self.canvas.create_text(start_x + hour * (self.bar_width * 2 + self.padding_x) + self.bar_width / 2,
                                    axis_bottom + self.x_label_offset, text=f"{hour:02d}", anchor=tk.N)

        # Add main title (with extra space above histogram)
        title_y = self.padding_y / 2  # Position the title in the first top 20% of the Canvas 
        self.canvas.create_text(canvas_width / 2, title_y ,
                                text=f"Histogram of Vehicle Frequency per Hour ({self.date})",
                                font=("Arial", 16, "bold"), anchor=tk.CENTER)

        # Add "Hours" heading below the x-axis
        hours_y = axis_bottom + self.padding_y + 20  # Adjusted position below the axis
        self.canvas.create_text(canvas_width / 2, hours_y,
                                text="Hours 00:00 to 24:00",
                                font=("Arial", 12), anchor=tk.CENTER)


  
    def add_legend(self):
        """
        Adds a legend to the histogram to indicate which bar corresponds to which junction.
        """
        junctions = list(self.histogram_data.keys()) # Get the list of junction names
        legend_start_x = 50
        legend_start_y = self.padding_y / 2

        # Loop through each junction to create the legend
        for i, junction in enumerate(junctions):
            self.canvas.create_rectangle(legend_start_x, legend_start_y, legend_start_x + 15, legend_start_y + 15, fill=self.colors[i])
            self.canvas.create_text(legend_start_x + 20, legend_start_y + 8, text=junction, anchor=tk.W)
            legend_start_y += 20

    def run(self):
        """
        Runs the Tkinter main loop to display the histogram.
        """
        self.setup_window() # Set up the application window
        self.draw_histogram() # Draw the histogram on the canvas
        self.add_legend()  #Add the legend to the histogram
        self.root.mainloop() # Start the Tkinter main loop to display the window and handle
        



# Task E: Code Loops to Handle Multiple CSV Files
class MultiCSVProcessor:
    def __init__(self):
        """
        Initializes the application for processing multiple CSV files.
        """
        self.collected_results = [] # List to store results from processed CSV files
        self.current_data = None # Variable to store the data currently being processed

    def load_csv_file(self, file_path):
        """
        Loads a CSV file and processes its data.
        """
        self.current_data = process_csv_data(file_path) # Calls a function to process data from the given file path
        return self.current_data #Return data
       

    def clear_previous_data(self):
        """
        Clears data from the previous run to process a new dataset.
        """
        self.current_data = None # Resets the current_data variable to prepare for new input
        
    def handle_user_interaction(self):
        """
        Handles user input for processing multiple files.
        """
        while True:
            # Validate date input from the user
            dd, mm, yyyy = validate_date_input()
            print(f"Searching In Progress {dd}/{mm}/{yyyy}")

            # Generate the CSV filename and display it
            csv_filename = f"traffic_data{dd:02d}{mm:02d}{yyyy}.csv"
            print(f"CSV Filename: {csv_filename}")

            try:
                # Load and process the CSV file
                data_frame = self.load_csv_file(csv_filename)
                if data_frame:
                    # Perform analysis and store results
                    results = display_outcomes(data_frame)
                    self.collected_results.append((results, csv_filename))
                    print("\nAnalysis Results:")
                    for key, value in results.items():
                        print(f"{key}: {value}")

                    # Display a histogram
                    histogram_app = HistogramApp(data_frame, f"{dd}/{mm}/{yyyy}")
                    histogram_app.run()

                else:
                    print(f"No data found for {csv_filename}")

            except FileNotFoundError as f:
                print(f"Error: {f}")

            except Exception as a:
                print(f"An error occurred: {a}")

            # Prompt user to decide whether to analyze another file
            user_input = input("Do you want to run the analysis again? (yes/no): ").strip().lower()
            if user_input != 'yes':
                # Save results and exit
                print("Saving all results to 'results.txt'")
                save_results_to_file(self.collected_results, "results.txt")
                print("All results saved successfully. Exiting the program.")
                break
            else:
                # Clear previous data for new analysis
                self.clear_previous_data()



    def process_files(self):
        """
        Main loop for handling multiple CSV files until the user decides to quit.
        """
        self.handle_user_interaction()


processor = MultiCSVProcessor()
processor.process_files()



"""
References:
1. Lott, S. F. (2015). *Mastering Object-Oriented Programming.
   Chapter 9: CSV Basics and Chapter 16: OS Basics.
   
2. Miller David L. Ranum Anderson (2019). *Python Programming in Context, 3rd Edition.
   Chapter 5: CSV File Reading and Opening, Chapter 7: File Processing.

3. ChatGPT. (2024). ChatGPT - Basics of OOP
   [online] Available at : https://chatgpt.com/share/675726cd-484c-8012-bcb5-ed659a0e29ce
   [Acccessed 29 November 2024]. 
   
4. Agnel Jhon, 2024. Error Makes Clever. YouTube video, added 16 august 2023.
   Available at: https://youtu.be/rltSHY2Y7-c [Accessed 17 December 2024].

5. Agnel Jhon, 2024. Error Makes Clever. YouTube video, added 25 august 2023.
   Available at: https://youtu.be/K3HD0gJXJYQ?feature=shared [Accessed 18 December 2024].

6. Agnel Jhon, 2024. Error Makes Clever. YouTube video, added 30 august 2023.
   Available at: https://youtu.be/PJxwAJdWpVY?feature=shared [Accessed 21 December 2024].

7. Bro Code, n.d. Python Programming Tutorials. YouTube playlist.
   Available at: https://youtube.com/playlist?list=PLZPZq0r_RZOOeQBaP5SeMjl2nwDcJaV0T [Accessed 18 December 2024].
"""
