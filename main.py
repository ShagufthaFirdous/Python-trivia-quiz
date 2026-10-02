import html
import requests
import random


# Get questions from the Open Trivia DB
def fetch_questions(amount=10):

    url = "https://opentdb.com/api.php"

    parameters = {
        "amount": amount,
        "difficulty" : "easy",
        "category" : 18,
        "type": "multiple"
    }

    try:
        response = requests.get(url, params=parameters)
        response.raise_for_status()

        data = response.json()

        return data.get("results", [])

    except requests.RequestException as e:
        print(f"Could not connect to the trivia website: {e}")
        return []


# Run the quiz
def run_quiz():
    print("=" * 60)
    print("Welcome to the Trivia Quiz!".center(70))
    print("=" * 60)
     

    questions = fetch_questions(10)

    if not questions:
        print("Sorry, couldn't load the questions.")
        print("Please check your internet connection.")
        return

    score = 0

    for number, question in enumerate(questions, 1):

        question_text = html.unescape(question["question"])
        correct_answer = html.unescape(question["correct_answer"])

        wrong_answers = [
            html.unescape(answer)
            for answer in question["incorrect_answers"]
        ]

        answers = wrong_answers + [correct_answer]

        # shuffle the answers so the correct answer isn't always in the same place
        random.shuffle(answers)

        print(f"\nQuestion {number}: {question_text}")

        options = {}

        for letter, answer in zip(["A", "B", "C", "D"], answers):
            options[letter] = answer
            print(f"{letter}. {answer}")

        while True:

            user_answer = input(
                "\nEnter your answer (A, B, C or D): "
            ).strip().upper()

            if user_answer in options:
                break

            print("Please enter only A, B, C or D.")

        # Check the answer
        if options[user_answer] == correct_answer:
            print("Correct! 🎉")
            score += 1
        else:
            print(f"Wrong! ❌ The correct answer was: {correct_answer}")

    # Show final score
    print("="*60)
    print("Woohooo Quiz Finished!")
    print(f"You scored: {score}/{len(questions)}")
    print("="*60)


if __name__ == "__main__":
    run_quiz()