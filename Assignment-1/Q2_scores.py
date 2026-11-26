import requests
import matplotlib.pyplot as plt

# quick script to grab student scores and plot a bar chart
# falls back to dummy data if the endpoint isn't live yet

ENDPOINT_URL = "https://example.com/api/students/scores"

FALLBACK_DATA = [
    {"name": "Aarav", "score": 78},
    {"name": "Isha", "score": 91},
    {"name": "Rohan", "score": 64},
    {"name": "Meera", "score": 85},
    {"name": "Kabir", "score": 72},
]


def fetch_student_scores(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as err:
        print(f"Couldn't reach the API ({err}), switching to local fallback data...")
        return FALLBACK_DATA


def main():
    records = fetch_student_scores(ENDPOINT_URL)

    student_names = []
    test_scores = []

    for entry in records:
        student_names.append(entry["name"])
        test_scores.append(entry["score"])

    class_avg = sum(test_scores) / len(test_scores)
    print(f"Class average: {class_avg:.2f}")

    # build the bar chart
    plt.figure(figsize=(8, 5))
    plt.bar(student_names, test_scores, color="steelblue")
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