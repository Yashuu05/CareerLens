# calculating total skill gap
import pandas as pd

def total_skill_gap_calculation(domain, technical_score, category_df, category_weight_df):
    """
    Calculates the final skill gap by combining technical and category gaps with their weights.
    """
    tag = ""
    
    # helper to safely get scalar value from single-row dataframe or series
    def get_val(df_or_series, col=None):
        if col is not None:
            if col in df_or_series:
                vals = df_or_series[col].values
                return float(vals[0]) if len(vals) > 0 else 0.0
            return 0.0
        else:
            vals = df_or_series.values
            return float(vals[0]) if len(vals) > 0 else 0.0

    # Extract individual category scores (from category_gap_calculation output)
    aptitude_score = get_val(category_df.loc[category_df['category'] == 'aptitude', 'category_gap'])
    projects_score = get_val(category_df.loc[category_df['category'] == 'projects', 'category_gap'])
    internship_score = get_val(category_df.loc[category_df['category'] == 'internship', 'category_gap'])
    
    # Try 'soft_skill' first, fallback to 'communication' if not found
    soft_skill_series = category_df.loc[category_df['category'].isin(['soft_skill', 'communication']), 'category_gap']
    soft_skill_score = get_val(soft_skill_series)
    
    # 1. calculate the weighted gaps
    technical_gap = float(get_val(category_weight_df, 'technical') * technical_score)
    aptitude_gap = float(get_val(category_weight_df, 'aptitude') * aptitude_score)
    project_gap = float(get_val(category_weight_df, 'projects') * projects_score)
    internship_gap = float(get_val(category_weight_df, 'internship') * internship_score)
    
    # For soft skill, the weight column could be 'soft_skill' or 'communication'
    w_soft_skill = get_val(category_weight_df, 'soft_skill')
    if w_soft_skill == 0.0:
        w_soft_skill = get_val(category_weight_df, 'communication')
    soft_skill_gap = float(w_soft_skill * soft_skill_score)

    # total gap
    total_gap = float(technical_gap + aptitude_gap + project_gap + internship_gap + soft_skill_gap)

    results = pd.DataFrame({
        "gap_category": ["technical", "aptitude", "projects", "internship", "soft_skill"],
        "gap_value": [technical_gap, aptitude_gap, project_gap, internship_gap, soft_skill_gap]
    })
    
    # tags logic updated based on plan
    if total_gap == 1.0:
        tag = "complete fresher"
    elif total_gap == 0.0:
        tag = "master"
    elif (total_gap > 0.0) and (total_gap <= 0.25):
        tag = "skilled"    
    elif (total_gap > 0.25) and (total_gap <= 0.50):
        tag = "learner"
    elif (total_gap > 0.50) and (total_gap <= 0.75):
        tag = "beginner"
    elif (total_gap > 0.75) and (total_gap < 1.0):
        tag = "fresher" 
    
    return total_gap, results, tag