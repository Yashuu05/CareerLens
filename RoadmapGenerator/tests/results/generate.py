# this file generates the roadmap to test the quality results of LLM
import os 
import sys 
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from RoadmapGenerator.roadmap_generate import roadmap_generator
import json
DATA_DIR = r"student_data.json"

def load_data(directory=DATA_DIR):
    try:
        with open(directory, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data
         
    except Exception as e:
        return f"{e}"

if __name__ == "__main__":  
    print("loading student data...")
    data = load_data(directory=DATA_DIR)
    
    if data is not None:
        print("generating LLM roadmap...\n")
        roadmap_generator(data_of_student=data)
        print("\n")
    else:
        print("Student Data is None. Failed to load data.")