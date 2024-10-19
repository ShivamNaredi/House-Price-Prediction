import pickle
import json
import numpy as np

__locations = None
__data_columns = None
__model = None

# Function to estimate the price
def get_estimated_price(location, sqft, bhk, bath):
    try:
        loc_index = __data_columns.index(location.lower())  # Get the index of the location in data columns
    except ValueError:  # Handle case if location is not found
        loc_index = -1

    # Create a numpy array for prediction
    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk

    if loc_index >= 0:  # If the location is valid, set its value to 1
        x[loc_index] = 1

    return round(__model.predict([x])[0], 2)  # Predict and return rounded value

# Load the saved artifacts (model and columns)
def load_saved_artifacts():
    print("loading saved artifacts...start")
    global __data_columns
    global __locations

    # Load the data columns
    with open("./artifacts/columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]  # first 3 columns are sqft, bath, bhk

    global __model
    if __model is None:
        # Load the trained model
        with open('./artifacts/banglore_home_prices_model.pickle', 'rb') as f:
            __model = pickle.load(f)

    print("loading saved artifacts...done")

# Function to get the location names
def get_location_names():
    return __locations

# Function to get data columns
def get_data_columns():
    return __data_columns

# Testing the utility functions (useful for development)
if __name__ == '__main__':
    load_saved_artifacts()
    print(get_location_names())
    print(get_estimated_price('1st Phase JP Nagar', 1000, 3, 3))
    print(get_estimated_price('1st Phase JP Nagar', 1000, 2, 2))
    print(get_estimated_price('Kalhalli', 1000, 2, 2))  # Other location
    print(get_estimated_price('Ejipura', 1000, 2, 2))   # Other location
