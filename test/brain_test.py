import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.brain import generate_commentary


def run_test():
    events = {
        "type": "Goal",
        "player": "R. Lewandowski",
        "detail": "Gol w samo okienko",
        "assist": "Lamine Yamal",
    }

    print("\n--- KOMENTARZ BOTA ---")
    for i in range(1, 5):
        wynik = generate_commentary(
            "FC Barcelona", "Real Madrid", "Real Madrid", f"{i}:0", events
        )
        print(wynik)
    print("----------------------")


if __name__ == "__main__":
    run_test()
