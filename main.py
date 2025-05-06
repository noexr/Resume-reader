import re
import glob
from resume_reader import ResumeReader
from job_matcher import JobMatcher, visualize_match_scores

ALL_SKILLS = [
    "python", "machine learning", "data analysis", "pandas", "numpy",
    "html", "css", "javascript", "react", "nodejs",
    "java", "android", "kotlin", "xml", "firebase",
    "linux", "docker", "kubernetes", "aws", "ci/cd"
]


def extract_number(filename):
    match = re.search(r'resume(\d+)', filename)
    return int(match.group(1)) if match else float('inf')


def process_resume(path):
    try:
        print(f"\nProcessing {path}...")
        reader = ResumeReader(path)
        name = reader.extract_name()
        email = reader.extract_email()
        skills = reader.extract_skills(ALL_SKILLS)

        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Extracted Skills: {skills}")

        if skills:
            matcher = JobMatcher()
            match, score, all_scores = matcher.match(skills)
            print(f"Best Job Match: {match} (Similarity Score: {score:.2f})")
            visualize_match_scores(list(matcher.jobs.keys()), all_scores)
        else:
            print("No recognizable skills found in the resume.")

    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except ValueError as e:
        print(f"Invalid value encountered: {e}")
    except Exception as e:
        print(f"Unexpected error processing {path}: {e}")


def main():
    cv_paths = glob.glob("sample_cvs/*.pdf") + glob.glob("sample_cvs/*.docx")
    # Sort by numeric resume number
    sorted_paths = sorted(cv_paths, key=extract_number)

    for cv_path in sorted_paths:
        process_resume(cv_path)
        input("\nPress Enter to process the next resume...")


if __name__ == "__main__":
    main()
