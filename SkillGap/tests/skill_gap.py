import os
import sys
import json
import pytest

project_root = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

if project_root not in sys.path:
    sys.path.insert(0, project_root)

from SkillGap.main_calculation import calculate_skill_gap_for_student


STUDENT = "student_3"
DATA_DIR = "test_data.json"


#@pytest.fixture
def student_data():
    data_file = os.path.join(os.path.dirname(__file__), DATA_DIR)
    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    student = data[STUDENT]
    return student

def test_skill_gap_calculation(student_data):
    domain = student_data.pop("target_domain", None)
    student_scores = student_data

    results = calculate_skill_gap_for_student(
        domain=domain,
        student_scores=student_scores
    )

    total_gap = results["total_gap"]
    print(results)
    #assert total_gap == pytest.approx(99.99, abs=0.01)

if __name__ == "__main__":
    # load student data
    data = student_data()
    test_skill_gap_calculation(student_data=data)