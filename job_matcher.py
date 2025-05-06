from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt


class JobMatcher:
    def __init__(self):
        self.jobs = {
            "Data Scientist": ["python", "machine learning", "data analysis", "pandas", "numpy"],
            "Web Developer": ["html", "css", "javascript", "react", "nodejs"],
            "Android Developer": ["java", "android", "kotlin", "xml", "firebase"],
            "DevOps Engineer": ["linux", "docker", "kubernetes", "aws", "ci/cd"]
        }

    def match(self, candidate_skills):
        if not candidate_skills:
            raise ValueError("Candidate skills list cannot be empty.")

        job_names = list(self.jobs.keys())
        job_skill_strings = [" ".join(skills) for skills in self.jobs.values()]
        candidate_string = " ".join(candidate_skills)

        vectorizer = CountVectorizer().fit_transform([candidate_string] + job_skill_strings)
        vectors = vectorizer.toarray()

        similarity_scores = cosine_similarity([vectors[0]], vectors[1:])[0]
        best_match_index = similarity_scores.argmax()
        best_score = similarity_scores[best_match_index]

        return job_names[best_match_index], best_score, similarity_scores


def visualize_match_scores(job_names, scores):
    pct_scores = [score * 100 for score in scores]

    plt.figure(figsize=(10, 5))
    plt.bar(job_names, pct_scores, color='skyblue')
    plt.ylim(0, 100)
    plt.ylabel('Similarity Score (%)')
    plt.title('Job Match Similarity')

    for i, pct in enumerate(pct_scores):
        plt.text(i, pct + 1, f"{pct:.1f}%", ha='center')

    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.show()
