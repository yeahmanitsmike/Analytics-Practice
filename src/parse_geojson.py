import json
import csv
import os

def topojson_properties_to_csv(topojson_filepath, output_csv_filepath):
    """
    Parses a TopoJSON file to extract properties from its geometries
    and writes them to a CSV file.

    Args:
        topojson_filepath (str): The path to the input TopoJSON file.
        output_csv_filepath (str): The path where the output CSV file will be saved.
    """
    try:
        with open(topojson_filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{topojson_filepath}' was not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from the file '{topojson_filepath}'. Make sure it's a valid JSON file.")
        return
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")
        return

    # Navigate to the geometries array based on the typical TopoJSON structure
    # and the user's screenshot.
    # The key for the main object collection might vary, but "Election_Precincts"
    # was shown in the screenshot. If it's different, this key needs to be adjusted.
    try:
        # It's common for TopoJSON to have a primary named object.
        # We'll try to find it or assume a common structure.
        if 'objects' in data and isinstance(data['objects'], dict):
            # Assuming the relevant object is the first one if multiple exist,
            # or specifically named 'Election_Precincts' as per screenshot.
            object_key = 'Election_Precincts' # From user's screenshot
            if object_key not in data['objects']:
                # Fallback if 'Election_Precincts' isn't the direct key
                if data['objects']:
                    object_key = list(data['objects'].keys())[0]
                    print(f"Warning: '{object_key}' not found in objects. Using the first object key: '{object_key}'")
                else:
                    print("Error: No objects found in the TopoJSON file.")
                    return

            if 'geometries' in data['objects'][object_key] and \
               isinstance(data['objects'][object_key]['geometries'], list):
                geometries = data['objects'][object_key]['geometries']
            else:
                print(f"Error: 'geometries' array not found in data['objects']['{object_key}'].")
                return
        else:
            print("Error: TopoJSON structure not as expected. Missing 'objects' dictionary.")
            return

        if not geometries:
            print("No geometries found in the TopoJSON file.")
            return

        # Extract all properties from each geometry
        all_properties_list = []
        for geom in geometries:
            if 'properties' in geom and isinstance(geom['properties'], dict):
                all_properties_list.append(geom['properties'])
            else:
                # Handle cases where a geometry might not have properties or it's not a dict
                print(f"Warning: Geometry found without valid 'properties'. Skipping. Geometry: {str(geom)[:100]}")
                all_properties_list.append({}) # Add an empty dict to maintain row count if needed, or skip

        if not all_properties_list:
            print("No properties found in any of the geometries.")
            return

        # Determine the headers from the keys of the first geometry's properties
        # To be robust, collect all possible headers from all geometries
        all_headers = set()
        for props in all_properties_list:
            all_headers.update(props.keys())
        
        # Maintain a consistent order for headers if possible, e.g., from the first item
        # or sort them alphabetically for consistency if order isn't critical.
        if all_properties_list[0]:
             ordered_headers = list(all_properties_list[0].keys())
             # Add any headers not in the first item but present in others
             for header in sorted(list(all_headers)): # Sort for consistent order of extra headers
                 if header not in ordered_headers:
                     ordered_headers.append(header)
        else: # Fallback if the first item had no properties
            ordered_headers = sorted(list(all_headers))


        # Write to CSV
        with open(output_csv_filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=ordered_headers)
            writer.writeheader()
            for props in all_properties_list:
                # Ensure all rows have all header keys, filling with empty string if a key is missing
                row_to_write = {header: props.get(header, "") for header in ordered_headers}
                writer.writerow(row_to_write)

        print(f"Successfully converted properties to '{output_csv_filepath}'")

    except KeyError as e:
        print(f"Error: A key was not found in the JSON structure: {e}. Please check the TopoJSON format.")
    except Exception as e:
        print(f"An unexpected error occurred during processing: {e}")

# --- How to use ---
# 1. Save this code as a Python file (e.g., topojson_parser.py).
# 2. Make sure your 'Election_Precincts.json' file is in the same directory,
#    or provide the full path to it.
# 3. Run the script from your terminal: python topojson_parser.py

# Example usage:
input_file = os.path.join('/home/mike-rob/Development/Analytic_Dev/data','Election_Precincts.json') # Replace with your TopoJSON file path
output_file = 'election_precincts_properties.csv'
topojson_properties_to_csv(input_file, output_file)
