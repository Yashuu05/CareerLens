def apply_feature_extraction(data):
    import numpy as np
    """
    Purpose: performs feature extraction on given dataset.

    input = data: current dataframe
    output = df : resulted dataframe
    """
    df = data.copy()
    # 1. Academic Performance
    df["academic_score"] = (
        df["cgpa"] * 10 - df["Backlogs"] * 5
    )
    
    # 2. Academic Risk
    df["academic_risk"] = np.where(
        (df["cgpa"] < 6.5) | (df["Backlogs"] > 2),
        1,
        0
    )

    # 3. Programming Ability    
    df["technical_score"] = (
        df["Coding_skills"] +
        df["Dsa_score"] +
        df["System_design"]
    ) / 3

    # 4. Experience Score
    df["experience_score"] = (
        df["Internships"] * 3 +
        df["projects_count"] * 2 +
        df["Open_source_contributions"] * 2 +
        df["Hackathons"] +
        df["Certifications"]
    )

    # 5. Employability Score
    df["employability_score"] = (
        df["technical_score"] * 0.40 +
        df["Aptitude_score"] * 0.20 +
        df["communication_skills"] * 0.10 +
        df["experience_score"] * 0.30
    )

    return df 