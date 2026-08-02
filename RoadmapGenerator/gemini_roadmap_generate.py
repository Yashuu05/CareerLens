from google import genai
from dotenv import load_dotenv
import os 
import sys 
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from logger import logging as log
import yaml
import json
from pathlib import Path
load_dotenv()

def read_file(file_path: Path):
    """
    *purpose*: reads system prompt file
    *input*: file_path (path of a system prompt file)
    *output*: conent (file contents)
    """
    try:
        # Open and read the raw markdown syntax
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            return content
        
    except Exception as e:
        return f"error: {e}"

def run_model(model_name: str, prompt: str, temp: float, system_instruction):
    """
    - *purpose*: runs selected Gemini Model through API call
    - *inputs*:
        1. model_name: name of selected model
        2. prompt: user prompt to LLM
        3. system_intruction: system prompt to generate roadmap
        4. temp: tuning resonse of llm
    - *output*: LLM response to user promopt
        
    """
    client = genai.Client()
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config={
            "temperature": temp,
            "system_instruction": system_instruction
        }
    )
    full_response = response.text
    if hasattr(response, "usage_metadata") and response.usage_metadata:
        total_tokens = getattr(response.usage_metadata, "total_token_count", 0)
        total_input_tokens = getattr(response.usage_metadata, "prompt_token_count", 0)
        total_output_tokens = getattr(response.usage_metadata, "candidates_token_count", 0)
    else:
        total_tokens, total_input_tokens, total_output_tokens = 0, 0, 0
        
    print(full_response)
        
    return full_response, total_tokens, total_input_tokens, total_output_tokens

def load_yaml(file_path:Path):
    print(f"opening {file_path}")
    with open(file_path, "r") as f:
        try:
            print("reading file")
            data = yaml.safe_load(f)
            return data 
        
        except yaml.YAMLError as exc:
            print(f"Error parsing YAML file: {exc}")
        except Exception as e:
            print(f"{e}")

def load_json(file_path: Path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data
         
    except Exception as e:
        print(f"error: {e}")
        return None

def generate_roadmap(student_gap_data: dict):
    config_path = os.path.join(project_root, "RoadmapGenerator", "config.yaml")
    data = load_yaml(file_path=config_path)
    system_prompt_path = os.path.join(project_root, "RoadmapGenerator", "system_prompt.md")
    system_prompt = read_file(file_path=system_prompt_path)
    
    if data:
        model_1 = data["cloud_llm"]["models"]["model_1"]
        model_2 = data["cloud_llm"]["models"]["model_2"]
        temperature = data["cloud_llm"]["temperature"]
        
        user_input = f"Generate personalized and concise career roadmap by analyzing given student data. Strictly follow instructions.\nStudent data:\n'{json.dumps(student_gap_data)}'"
        
        try:
            full_response, tokens, it, ot = run_model(model_name=model_1, prompt=user_input, temp=temperature, system_instruction=system_prompt)
            return full_response
        except Exception as e:
            error_msg = str(e).lower()
            if "service_unavailable" in error_msg or "quota_exceeded" in error_msg:
                log.error(f"API Error '{error_msg}'. Falling back to model: {model_2}")
                try:
                    full_response, tokens, it, ot = run_model(model_name=model_2, prompt=user_input, temp=temperature, system_instruction=system_prompt)
                    return full_response
                except Exception as fallback_e:
                    log.error(f"Fallback model failed: {fallback_e}")
            log.error(f"Error in generate_roadmap: {e}")
            return None
    return None

if __name__ == "__main__":
    try:
        # Load configuration
        log.info("reading configuration")
        config_path = os.path.join(project_root, "RoadmapGenerator", "config.yaml")
        data = load_yaml(file_path=config_path)
        log.info("reading system instruction")
        # load system instruction file
        system_prompt_path = os.path.join(project_root, "RoadmapGenerator", "system_prompt.md")
        system_prompt = read_file(file_path=system_prompt_path)
        log.info("reading student skill data")
        # load student skill gap data
        student_gap_data_path = os.path.join(project_root, "RoadmapGenerator", "tests", "student_data.json")
        student_gap_data = load_json(file_path=student_gap_data_path)
        # output example
        log.info("reading example file")
        example_file_path = os.path.join(project_root, "RoadmapGenerator", "tests", "results", "result_3.md")
        example = read_file(file_path=example_file_path)
        
        if data:
            log.info("extracting configurations")
            # Extract models
            model_1 = data["cloud_llm"]["models"]["model_1"]
            model_2 = data["cloud_llm"]["models"]["model_2"]

            # extract temperature
            temperature = data["cloud_llm"]["temperature"]
            
            print(f"\n--- Testing primary model: {model_1} ---")
            log.info(f"running {model_1} with temperature {temperature}")
            try:
                if student_gap_data is not None:
                    user_input = f"Generate personalized roadmap by analyzing given student data. Strictly follow instruction prompt. Refer to example for assistance.Example:\n'{example}'.\nStudent data:\n'{student_gap_data}'"
                    full_response, total_tokens, input_tokens, output_tokens = run_model(model_name=model_1, prompt=user_input, temp=temperature, system_instruction=system_prompt)
                    print(f"\n[Usage] total tokens= {total_tokens} | input tokens= {input_tokens} | output tokens= {output_tokens}")
                    log.info(f"{model_1} ran with input tokens {input_tokens} and output tokens {output_tokens}")
                else:
                    print("Stundent Data not found.")
                    log.error("Student data couldn't find.")
            except Exception as e:
                error_msg = str(e).lower()
                
                # Check for specific error types
                if "service_unavailable" in error_msg or "quota_exceeded" in error_msg:
                    print(f"\nAPI Error '{error_msg}'. Falling back to model: {model_2}")
                    log.error(f"API Error '{error_msg}")
                    try:
                        full_response, total_tokens, input_tokens, output_tokens = run_model(model_name=model_2, prompt=user_input, temp=temperature, system_instruction=system_prompt)
                        print(f"\n[Usage] total tokens= {total_tokens} | input tokens= {input_tokens} | output tokens= {output_tokens}")
                    except Exception as fallback_e:
                        print(f"Fallback model failed: {fallback_e}")
                        log.error(f"{fallback_e}")

                elif "model_not_found" in error_msg:
                    print(f"Model not found: {e}")
                    log.error(f"model not found: {e}")
                elif "rate_limit_exceeded" in error_msg:
                    print(f"Rate limit exceeded: {e}")
                    log.error(f"Rate limit exceeded: {e}")
                elif "api_error" in error_msg:
                    print(f"API Error: {e}")
                    log.error(f"API Error: {e}")
                else:
                    print(f"Unhandled API error: {e}")
                    log.error(f"Unhandled API error: {e}")
        
    except Exception as e:
        print(f"error: {e}")
        log.error(f"{e}")