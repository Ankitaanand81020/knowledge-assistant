import json
import requests
import time


API_URL = "http://localhost:8000/ask"


def ask(question: str):
    start = time.time()

    res = requests.post(
        API_URL,
        json={
            "question": question,
            "top_k": 3
        }
    )

    elapsed = round(
        (time.time() - start) * 1000,
        2
    )

    return (
        res.json(),
        elapsed
    )


def keyword_score(
    answer: str,
    expected_keywords: list
):
    answer = answer.lower()

    found = 0

    for k in expected_keywords:
        if k.lower() in answer:
            found += 1

    return (
        found,
        len(expected_keywords)
    )


def evaluate():
    with open(
        "tools/eval_set.json",
        "r",
        encoding="utf-8"
    ) as f:
        dataset = json.load(f)

    total = 0

    print("\n===== Evaluation =====\n")

    for item in dataset:

        question = item["question"]

        expected = item[
            "expected_keywords"
        ]

        result, latency = ask(
            question
        )

        answer = result.get(
            "answer",
            ""
        )

        matched, count = (
            keyword_score(
                answer,
                expected
            )
        )

        score = round(
            (
                matched
                / count
            )
            * 100,
            1,
        )

        total += score

        print(
            f"Q: {question}"
        )

        print(
            f"Score: {score}%"
        )

        print(
            f"Latency: {latency} ms"
        )

        print(
            f"Answer: {answer[:200]}"
        )

        print("-" * 50)

    avg = round(
        total
        / len(dataset),
        1,
    )

    print(
        f"\nAverage Score: {avg}%"
    )


if __name__ == "__main__":
    evaluate()