# integrates skill gap analyzer, placement prediction, and Roadmap generator
import os 
import sys
import json
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_path not in sys.path:
    sys.path.insert(0, root_path)
from RoadmapGenerator.roadmap_generate import roadmap_generator
from RoadmapGenerator.web_search import search_course
from PlacementPrediction.prediction import predict_placement, load_model
from SkillGap.main_calculation import calculate_skill_gap_for_student
from dotenv import load_dotenv
load_dotenv()

TAVILY_API_KEY = os.getenv(key="TAVILY_KEY")
MODEL_DIR = r"D:\projects\Student\PlacementPrediction\models\logistic_regression.joblib"


if __name__ == "__main__":

    while True:
        print("Enter number of your choice :\nplacement prediction: 1\nskill gap analyse: 2\nRoadmap generator: 3\nExit: 0")
        choice = int(input("enter choice= "))

        if choice == 0:
            print(f"===== program terminated =====")
            break

        if choice == 1:
        # student placement prediction input
            print("You selected 'Placement Prediction'")

            branch = str(input("Branch(ECE,CSE,IT,CE,Chemical) = "))
            college_tier = str(input("college tier (e.g Tier-1) = "))
            cgpa = float(input("CGPA = "))
            backlogs = int(input("Backlogs = "))
            coding_skills = float(input("coding skills score (0-5)= "))
            dsa_score = float(input("dsa score (0-5)="))
            aptitude_score = float(input("aptitude score (0-100)= "))
            communication_score = float(input("Communication score (0-10)= "))
            ml_score = float(input("ML score (0-10)= "))
            system_design = float(input("System Design score (0-10)= "))
            internships = int(input("Internships = "))
            project_score = int(input("Project Count = "))
            certifcate = int(input("Certification = "))
            hackathon = int(input("Hackathons = "))
            open_source = int(input("Open Source Contributions = "))
            extracurricular = int(input("Extracurriculars = "))

            input = {
                "branch":branch,
                "college_tier":college_tier,
                "cgpa":cgpa,
                "backlogs":backlogs,
                "coding_skills":coding_skills,
                "dsa_score":dsa_score,
                "aptitude_score":aptitude_score,
                "communication_skills":communication_score,
                "ml_knowledge":ml_score,
                "system_design":system_design,
                "internships":internships,
                "projects_count":project_score,
                "certifications":certifcate,
                "hackathons":hackathon,
                "open_source_contributions":open_source,
                "extracurriculars":extracurricular,
            }

            # placement prediction
            print("loading model...")
            model = load_model(file_path=MODEL_DIR)
            print("predicting...")
            output, probability=predict_placement(model=model, input_data=input)
            print(f"result : {output}\nprobability: {probability:.2f}")

        elif choice == 2:
            print("You selected Skill Gap Analyse")    

            # Stundent score data
            domain = str(input("enter domain = "))
            python = int(input("enter python score(1-5) = "))
            java = int(input("enter java score(1-5) = "))
            javascript = int(input("enter javascript score(1-5) = "))
            html_css = int(input("enter html-css score(1-5) = "))
            react = int(input("enter Reactjs score(1-5) = "))
            node = int(input("enter nodejs score(1-5) = "))
            sql = int(input("enter sql score(1-5) = "))
            ml = int(input("enter ML score(1-5) = "))
            dl = int(input("enter DL score(1-5) = "))
            data_viz = int(input("enter Data Vizualization score(1-5) = "))
            stats = int(input("enter Statistics score(1-5) = "))
            docker = int(input("enter docker score(1-5) = "))
            kubernetes = int(input("enter Kubernetes score(1-5) = "))
            aws = int(input("enter AWS score(1-5) = "))
            git = int(input("enter Git score(1-5) = "))
            linux = int(input("enter Linux score(1-5) = "))
            communication = int(input("enter Communication score(1-5) = "))
            aptitude = int(input("enter aptitude score(1-5) = "))
            projects = int(input("enter no. Project score = "))
            inernsihip = int(input("enter No. Internships = "))

            # create the dictionary
            print("preparing input...")
            student_scores = {
                "target_domain": domain,
                "python": python,
                "java":java,
                "javascript":javascript,
                "html_css":html_css,
                "react":react,
                "nodejs":node,
                "sql":sql,
                "machine_learning":ml,
                "deep_learning":dl,
                "data_visualization":data_viz,
                "statistics":stats,
                "docker":docker,
                "kubernetes":kubernetes,
                "aws":aws,
                "git":git,
                "linux":linux,
                "communication":communication,
                "aptitude":aptitude,
                "projects":projects,
                "internship":inernsihip
            }

            # skill gap analyser
            print("calculating skil gap...")
            result = calculate_skill_gap_for_student(domain=domain, student_scores=student_scores)
            result['target_domain'] = domain
            print(f"total gap = {result['total_gap']}")
            print(f"You are a {result['tag']}")
            print(f"technical gap breakdown:\n{result['technical_breakdown']}")
            print(f"Technical Gap: {result['technical_gap_percent']}")
            print(f"Category wise breakdown: {result['category_gap_breakdown']}")

            print("saving Skill Gap details...")
            import pandas as pd
            import numpy as np
            
            def df_to_json(obj):
                if isinstance(obj, pd.DataFrame):
                    return obj.to_dict(orient='records')
                elif isinstance(obj, pd.Series):
                    return obj.to_dict()
                elif isinstance(obj, np.integer):
                    return int(obj)
                elif isinstance(obj, np.floating):
                    return float(obj)
                elif isinstance(obj, np.ndarray):
                    return obj.tolist()
                return str(obj) # Fallback for any other non-serializable objects

            with open("result.json", "w", encoding="utf-8") as f:
                json.dump(result, f, indent=4, default=df_to_json)

        elif choice == 3:
            print("You selected Roadmap Generator")
            try:
                # load skill gap data
                with open("result.json", "r", encoding="utf-8") as f:
                    skill_gap_data = json.load(f)   
            except Exception as e:
                print(f"error loading skill gap data: {e}")
                continue

            domain = skill_gap_data.get('target_domain', 'your domain')
            # use llm to generate roadmap
            roadmap_generator(data_of_student=skill_gap_data)
            # search for the course
            print("Searching for the course...")
            print(f"Following are the courses you can persue for {domain}")
            course_lst = search_course(tavily_api=TAVILY_API_KEY, query=(f"best courses for {domain} in 2026."))
            if course_lst:
                for i in range(len(course_lst)):
                    print(f"{i+1}. title: {course_lst[i]['title']}\nURL: {course_lst[i]['url']}")
            else:
                print("No courses found.")