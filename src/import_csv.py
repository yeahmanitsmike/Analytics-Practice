import pandas as pd
import csv
import time
import json

start_time = time.time()
path = '/home/mike-rob/Development/Analytic_Dev/data/Vendor_Payments.csv'
    

def load_csv_to_dict_pd(file_path: str) -> list[dict]:
    df = pd.read_csv(file_path)
    df = df.to_dict(orient="records")
    return df

def print_dict_pd() -> None:
    dict = load_csv_to_dict_pd(path)
    print(dict[:2])

def load_csv_to_dict_csv(file_path: str) -> list[dict]:
    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
        return data

def print_dict_csv() -> None:
    dict = load_csv_to_dict_csv(path)
    print(dict[:2])

def load_csv_to_df(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    df = pd.DataFrame(df)
    return df

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


if __name__ == "__main__": 
    
    # print(load_csv_to_df(path).head(5)) 
    # print_dict_pd()
    # print_dict_csv()
    # load_csv_to_csv(path)
    # csv_to_json_pandas(path)
    csv_to_json_json(path)

    end_time = time.time()
    time_elapse = end_time - start_time
    print(f"Total run time: {time_elapse: .4f} seconds")
    pass        

