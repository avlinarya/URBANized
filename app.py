from flask import Flask, render_template, redirect,request
# Add Gemini API
from google import genai
import os
from Plot import plot_city_layoutout
import ast


print("Gemini API Key:", os.getenv("GEMINI_API_KEY"))
#configure app
app = Flask(__name__)
# Enable auto-reload
app.config['TEMPLATES_AUTO_RELOAD'] = True
# Create the main route


prompt = input("Enter Your Prompt: ")

getJSON_1 = '''  You are an Urban Planner, so to make a city you need to consider various factors. These are all the Factors you need to consider
Total Area
Unit for grid cells [UNIT = “50mx50m”]
Total Population to accommodate
Distribution preference [DISTRIBUTION = “Smart Scattered”]
Zoning Laws
Height Restrictions [MAX_HEIGHT = “200”]
% Allocations for Schools [SCHOOL = 1]
Keep 1 hospital 
% Allocations for Hospitals [HOSPITAL = 2]
% Allocations for Police Stations [POLICE = 2]
% Allocations for Fire Stations [FIRE = 2]
Public transport stops (bus,metro) [TRANSPORT = 6]
% of area for green space [GREEN_AREA = 21]
Water-bodies [WATER = 10]
Priorities : Rank of whats most important (Maximise housing, Minimise Traffic, Maximise Green Space, Walkability)
Example cities to mimic [CITY = “SINGAPORE”]

Do not output anything except the FINAL JSON that i will tell u at the end.
Now the prompt given by the user is
  '''

getJSON_2 = '''

First you figure out the area that the user requires. It should be in a rowXcolumn state, like, 2kmx5km. Let the Total Area Equal that value as a string. Eg : Area = “2kmx5km”. If the area is not specified, return “Did not receive Area” and ignore the rest of the prompt.

Only continue from here if area was specified:
For point number 3 (Total Population to accommodate) , if its specified in prompt, let POPULATION = The value specified, however if not specified, then find out the average Population for the area specified. And input POPULATION = the calculated average.

Do the ranking of the Priorities (Point 14) based on the prompt received by the user such that PRIORITIES = [RANK #1, RANK #2, RANK #3, RANK#4]

For point 5. Analyze the prompt to see what percentage of the following zones the user wants, if not specified, go with the default value i will provide:
Residential [RESIDENTIAL = 40]
Commercial [COMMERCIAL = 10]
Institutional [INSTITUTE = 5]
Road [ROAD = 15]
Green Spare [GREEN = 20]
Again, if any of the above points was mentioned in the prompt, replace the default value provided in the point with the one in the prompt

Now do the same for all the other points i did not mention (2 , 4, 6-13 , 15). If its mentioned in prompt, replace the default value provided in point with the one in the prompt. 

And now return JUST THE FOLLOWING JSON as your output:

{
  "total_area": AREA calculated in form “Km x Km” or “m x m”, 
  "grid_unit": user input or "50mx50m",
  "population": User input or the average POPULATION calculated ,
  "distribution": User input or DISTRIBUTION default value,
  "zoning_laws": {
    "residential": Auto-calculate or user-defined,
    "commercial": Auto-calculate or user-defined,
    "institutional": Based on allocations below,
    "green_space": 21,
    “Road” : user-defined or default
  },
  "height_restrictions": {
    "max_height": USER INPUT or 200
  },
  "facility_allocations": {
    "schools": 1,
    "hospitals": 4,
    "police_stations": 2,
    "fire_stations": 2
  },
  "public_transport": {
    "stops": 6
  },
  "natural_features": {
    "green_area_percent": 21,
    "water_body_percent": 10
  },
  "priorities": [
	RANK#1,
	RANK#2,
	RANK#3,
	RANK#4
  ],
  "city_template": "SINGAPORE"
}

Again, in this, for any values, if its specified in the User, use that value, otherwise use the default values.



'''


actualprompt = getJSON_1 + prompt + getJSON_2
#actualprompt = "What is 2x6?"


client= genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
response = client.models.generate_content(
    model="gemini-2.5-pro",
    contents=f"{actualprompt}",
)

print(response.text)

JSON1 = response.text




print("\n JSON Created \n")

COORDS_1 = ''' You are an expert urban planner generating a cartoon-style visual layout of a smart city.
Use the specifications below to create a 2D coordinate-based city grid layout '''

COORDS_2 = ''' Zone types to include:
 zone_types = ['residential', 'greenery', 'transit', 'school', 'hospital', 'water', 'roads', 'police_station', 'fire_station', 'commercial']
DESIGN GOALS:
Build a city plan that mimics a clean, modular, and spaced-out layout (like Singapore or well-zoned capital districts).


Do NOT break zone types into small square tiles. Instead, each zone instance should be one large rectangle (e.g., a single building block, office, park, or housing area).
Vary rectangle sizes for different zones. Example:
Residential blocks can be wide (e.g., 200x100 meters).
scatter the greenery into little pieces (around 5-6) around the map

do the same with water (2-3) as you did with greenery.

Schools, hospitals, and institutions can be compact but rectangular.

Roads should be long strips and form a navigable network—include straight lines, T-junctions, and some curves. Avoid checkerboard-style roads completely.


LAYOUT CONSTRAINTS:
Top-left of the canvas is (0,0). Units are in meters. Total canvas size is 2000m x 2000m.

Use 50m x 50m grid cells as a planning reference—but actual zones should combine many grid cells into varied rectangular areas.

Allow roads to use fractional widths like 40x50 or 50x40. You may use decimal coordinates (e.g., 122.5) for road/transit precision.

Transit stops must lie fully inside the road zones—assume they are placed on sidewalks or side-lanes.

Allocate land based on the percentages given in the json for each zone type.

Zones must not overlap. Each coordinate rectangle should be exclusive to one zone.


OUTPUT FORMAT:
Return just a Python dictionary where each key is a zone type and the value is a list of rectangle coordinates for that type.
Each rectangle should be defined as a tuple:
 (x0, y0, x1, y1), where (x0, y0) is the top-left and (x1, y1) is the bottom-right corner.
Only return this final output IN THE SAME FORMAT:
{"residential": [[0, 0, 40, 40], [60, 0, 100, 40], [0, 60, 40, 100], [60, 60, 100, 100]],
"commercial": [[40, 20, 60, 40], [40, 60, 60, 80]], }

I WILL BE SAVING THE OUTPUT TO A VARIABLE CALLED zone_coords
Make sure the output is a valid Python dictionary with the correct structure.
Do not include any additional text or explanations.
'''




actualprompt2 = COORDS_1 + JSON1 + COORDS_2
#actualprompt2 = "What is 2x7?"
client= genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
response2 = client.models.generate_content(
    model="gemini-2.5-pro",
    contents=f"{actualprompt2}",
)

print(response2.text)
raw_res = (response2.text)[:-3]
tup= raw_res.partition('n')
print(tup[2])

res= ast.literal_eval(tup[2])



zone_coords = res


fig = plot_city_layoutout(zone_coords)
fig.show()

