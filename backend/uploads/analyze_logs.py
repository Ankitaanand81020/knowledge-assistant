import requests


STATS_URL = "http://localhost:8000/stats"


def analyze_logs():

    try:
        response = requests.get(STATS_URL)

        if response.status_code != 200:
            print(
                f"Failed: {response.status_code}"
            )
            return

        data = response.json()

        print("\n===== API Log Analysis =====\n")

        print(
            f"Total Queries: "
            f"{data.get('total_queries', 0)}"
        )

        print(
            f"Average Latency: "
            f"{data.get('average_latency_ms', 0)} ms"
        )

        print(
            f"Last Query: "
            f"{data.get('last_query', 'None')}"
        )

        latency = data.get(
            "average_latency_ms",
            0
        )

        print("\nPerformance:")

        if latency <= 3000:
            print("Excellent")

        elif latency <= 8000:
            print("Good")

        elif latency <= 15000:
            print("Slow")

        else:
            print("Needs Optimization")

    except Exception as e:
        print(
            f"Error: {e}"
        )


if __name__ == "__main__":
    analyze_logs()