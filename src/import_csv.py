import pandas as pd
import csv
import time
import json
import xml.etree.ElementTree as ET

start_time = time.time()
path = '/home/mike-rob/Development/Analytic_Dev/data/Vendor_Payments.csv'
    

def load_csv_to_dict_pd(file_path: str) -> None:
    df = pd.read_csv(file_path)
    df = df.to_dict(orient="records")
    print(df[:2])

def load_csv_to_dict_csv(file_path: str) -> None:
    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        data = [row for _, row in zip(range(5), reader)]
        print(data[:2])

def load_csv_to_df(file_path: str) -> None:
    df = pd.read_csv(file_path)
    df = pd.DataFrame(df)
    print(df.head(5))

def load_manual_csv_to_dict(file_path: str) -> None:
    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        headers = next(reader)
        data = [dict(zip(headers, row)) for row in reader]
        print(data[:2])
        # Total run time:  0.7601 seconds

# loads a csv using csv module
def load_csv_to_csv(file_path: str) -> None:
    print("running load_csv_to_csv func: \n")
    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i < 6:
                print(row)
            elif i > 6:
                break
    # 0.0002 sec runtime

# loads a csv into a dictionary/json obj
def csv_to_json_pandas(file_path: str) -> None:
    df = pd.read_csv(file_path)
    df = df.to_dict(orient="records")
    print(df[:2])
    # 2.04 sec runtime

# csv to json using json dumps
def csv_to_json_json(file_path: str) -> None:
    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        data = [row for _, row in zip(range(5), reader)]
        jobj = json.dumps(data, indent=4)
        print(jobj)
    # 0.0003 runtime

def csv_to_xml(file_path: str, root_element: str = "root", row_element: str = "row") -> None:
    root = ET.Element(root_element)

    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader):
            if i > 5:
                break
            row_ele = ET.SubElement(root, row_element)
            for key, value in row.items():
                child = ET.SubElement(row_ele, key)
                child.text = value

    xml = ET.tostring(root, encoding="utf-8", method="xml").decode()
    print(xml)
# Total run time:  0.0006 seconds


if __name__ == "__main__": 
    
    # csv_to_xml(path)
    # load_manual_csv_to_dict(path)
    # load_csv_to_dict_csv(path)
    # load_csv_to_df(path)
    # load_csv_to_csv(path)
    csv_to_json_pandas(path)
    # csv_to_json_json(path)

    end_time = time.time()
    time_elapse = end_time - start_time
    print(f"Total run time: {time_elapse: .4f} seconds")
    pass        

