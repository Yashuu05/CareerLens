import pandas as pd
import os
from .technical_gap import technical_skill_calculate
from .category_gap import category_gap_calculation
from .total_skill_gap import total_skill_gap_calculation

# Base path for datasets
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'DataSource')

def calculate_skill_gap_for_student(domain, student_scores):
    """
    Orchestrates the skill gap calculation by strictly mapping user scores
    to the domain requirements and weights.
    
    :param domain: (str) Target domain (e.g., 'Data Science')
    :param student_scores: (dict) Dictionary mapping skill/category names to student's scores (e.g., {'python': 4, 'aptitude': 3})
    :return: dict with total_gap, technical_breakdown, category_breakdown, tag
    """
    domain = domain.strip()
    
    # Load datasets
    weights_df = pd.read_csv(os.path.join(DATA_DIR, 'domain_skill_weights.csv'))
    req_df = pd.read_csv(os.path.join(DATA_DIR, 'skill_requirement.csv'))
    cat_weights_df = pd.read_csv(os.path.join(DATA_DIR, 'category_weights.csv'))
    
    # Strictly filter by domain (case-insensitive for robust matching)
    domain_mask_weights = weights_df['domain'].str.lower() == domain.lower()
    domain_mask_req = req_df['domain'].str.lower() == domain.lower()
    domain_mask_cat_w = cat_weights_df['domain'].str.lower() == domain.lower()
    
    if not domain_mask_weights.any() or not domain_mask_req.any() or not domain_mask_cat_w.any():
        raise ValueError(f"Domain '{domain}' not found in one or more datasets.")
        
    domain_weights = weights_df[domain_mask_weights].iloc[0]
    domain_reqs = req_df[domain_mask_req].iloc[0]
    domain_cat_weights = cat_weights_df[domain_mask_cat_w] # keep as DataFrame for total_skill_gap_calculation
    
    # 1. Construct technical skill_data
    # Technical skills are all columns in domain_skill_weights.csv except 'domain'
    tech_skills = [col for col in weights_df.columns if col != 'domain']
    
    skill_data_list = []
    for skill in tech_skills:
        req_val = float(domain_reqs.get(skill, 0))
        weight_val = float(domain_weights.get(skill, 0))
        student_val = float(student_scores.get(skill, 0))
        
        skill_data_list.append({
            'skill': skill,
            'required': req_val,
            'student': student_val,
            'weight': weight_val
        })
        
    skill_data = pd.DataFrame(skill_data_list)
    
    # 2. Construct category_data
    # Categories: aptitude, projects, internship, communication/soft_skill
    cat_keys = ['aptitude', 'projects', 'internship', 'communication']
    cat_data_list = []
    
    for cat in cat_keys:
        req_val = float(domain_reqs.get(cat, 0))
        # Note: mapping communication to soft_skill in student_scores if provided that way
        student_score_key = 'soft_skill' if cat == 'communication' and 'soft_skill' in student_scores else cat
        student_val = float(student_scores.get(student_score_key, 0))
        
        cat_data_list.append({
            'category': 'soft_skill' if cat == 'communication' else cat, 
            'required': req_val,
            'student': student_val
        })
        
    category_data = pd.DataFrame(cat_data_list)
    
    # 3. Calculate gaps
    tech_total, tech_percent, tech_df = technical_skill_calculate(domain, skill_data)
    cat_df = category_gap_calculation(domain, category_data)
    
    total_gap, results_df, tag = total_skill_gap_calculation(
        domain, 
        tech_total, 
        cat_df, 
        domain_cat_weights
    )
    
    return {
        'total_gap': total_gap,
        'tag': tag,
        'technical_gap_percent': tech_percent,
        'technical_breakdown': tech_df,
        'category_gap_breakdown': cat_df,
        'overall_results': results_df
    }
