import json
import pandas as pd
import time

start_time = time.time()

path = '/home/mike-rob/Development/Analytic_Dev/data/Vendor_List.geojson'

def load_json_to_pd(file_path: str) -> None:
    with open(file_path, mode="r") as file:
        data = json.load(file)
    
    df = pd.json_normalize(data["features"])
    print(df.head())
    # Total run time:  0.0278 seconds

def load_json_with_json(file_path: str) -> None:
    with open(file_path, "r") as file:
        vendor_data = json.load(file)

    features = vendor_data.get("features", [])

    for i, feat in enumerate(features[:5]):
        print(f"feature {1+i}\n")
        print(json.dumps(feat, indent=2))
    # Total run time:  0.0064 seconds

def json_to_csv(file_path: str) -> None:
    with open(file_path, mode="r") as file:
        data = json.load(file)
        data = data["features"]
    df = pd.json_normalize(data)
    # df.to_csv(save_path, index=False)
    print(df)



if __name__ == "__main__":
    # load_json_to_pd(path)
    # load_json_with_json(path)
    json_to_csv(path)
    
    end_time = time.time()
    time_elapse = end_time - start_time
    print(f"Total run time: {time_elapse: .4f} seconds")