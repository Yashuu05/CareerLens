from dotenv import load_dotenv
import os 
import json
from tavily import TavilyClient

load_dotenv()
tavily_api_key = os.getenv("TAVILY_KEY")

if tavily_api_key is None:
    print("no api key found.")

def search_course(tavily_api, query: str, output_file="courses.json"):
    tavily_client = TavilyClient(api_key=tavily_api)   
    response = tavily_client.search(query)
    
    extracted_courses = []
    for result in response.get('results', []):
        course_info = {
            "title": result.get("title"),
            "url": result.get("url")
        }
        extracted_courses.append(course_info)
        
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(extracted_courses, f, indent=4)
        
    print(f"Saved {len(extracted_courses)} courses to {output_file}")
    return extracted_courses

if __name__ == "__main__":
    if tavily_api_key:
        domain = "Data Science"
        search_course(tavily_api=tavily_api_key, query=f"best {domain} courses in 2026.")