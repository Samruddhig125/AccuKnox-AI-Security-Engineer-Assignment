
import requests
import matplotlib.pyplot as plt

# API endpoint from which we'll try to fetch the student scores
ENDPOINT_URL = "https://example.com/api/students/scores"

# Keeping some sample records handy in case the API is unavailable
FALLBACK_DATA = [
    {"name": "Aarav", "score": 78},
    {"name": "Isha", "score": 91},
    {"name": "Rohan", "score": 64},
    {"name": "Meera", "score": 85},
    {"name": "Kabir", "score": 72},
]


def fetch_student_scores(url):
    """
    Tries to fetch student names and their test scores from the given API.
    If the request fails, it uses the sample data defined above so the
    rest of the script can still run.
    """
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as err:
        print(f"Couldn't reach the API ({err}), switching to local fallback data...")
        return FALLBACK_DATA


def main():
    """
    Fetches the student scores, calculates the class average and creates
    a bar chart to make it easier to compare everyone's performance.
    The chart is also saved as an image for later reference.
    """
    records = fetch_student_scores(ENDPOINT_URL)
    
    student_names = []
    test_scores = []

    for entry in records:
        student_names.append(entry["name"])
        test_scores.append(entry["score"])

    # Calculate the average score across all students
    class_avg = sum(test_scores) / len(test_scores)
    print(f"Class average: {class_avg:.2f}")

    # Create a bar chart to compare individual student scores
    plt.figure(figsize=(8, 5))
    plt.bar(student_names, test_scores, color="steelblue")

    # The dashed line helps show where the class average stands
    plt.axhline(class_avg, color="crimson", linestyle="--", label=f"Avg: {class_avg:.1f}")

    plt.xlabel("Student")
    plt.ylabel("Score")
    plt.title("Student Test Scores")
    plt.legend()
    plt.tight_layout()

    
    plt.savefig("scores.png", dpi=150)
    plt.show()


if __name__ == "__main__":
    main()
