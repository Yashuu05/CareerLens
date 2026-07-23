# this file generates the roadmap to test the quality results of LLM
import os 
import sys 
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from dotenv import load_dotenv
from RoadmapGenerator.roadmap_generate import roadmap_generator
from RoadmapGenerator.web_search import search_course
import json
load_dotenv()

tavily_api_key = os.getenv("TAVILY_KEY")
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
    domain = data['domain']
    print(f"searching courses for {domain}...")
    course_lst = search_course(tavily_api=tavily_api_key, query=f"best courses for {domain} in 2026")
    if data is not None:
        print("generating LLM roadmap...\n")
        roadmap_generator(data_of_student=data)
        print(f"Following is the list of courses for {domain} you can persue to learn industry skills.")
        for i in range(len(course_lst)):
            print(f"{i+1}. Title: {course_lst[i]['title']}\nURL: {course_lst[i]['url']}\n\n")
    else:
        print("Student Data is None. Failed to load data.")