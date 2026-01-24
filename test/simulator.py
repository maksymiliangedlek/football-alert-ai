import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.brain import generate_commentary
from src.notification import send_all_notifications

# def simulate_goal():
#     print("⚽ Symulacja: Robert Lewandowski strzela gola!")

#     fake_event = "Robert Lewandowski strzela gola przewrotką w 92 minucie meczu z Realem Madryt po asyście Lamine Yamala."
#     score = "5:0"

#     commentary = generate_commentary("FC Barcelona","Real Madrid",score,fake_event)

#     send_all_notifications("GOOOL DLA BARCY! 🔵🔴", commentary, score,fake_event)
#     print("✅ Powiadomienia wysłane!")


def simulate_goal():
    print("⚽ Symulacja: Real strzela gola!")

    fake_event = "Robert Lewandowski nie trafia sam na sam po czym idzie kontra i Mbappe strzela gola przewrotką w 92 minucie meczu z Barcelona po asyscie Rodrygo."
    score = "1:2"

    commentary = generate_commentary(
        "FC Barcelona", "Real Madrid", "FC Barcelona", score, fake_event
    )

    send_all_notifications("GOOOL DLA Realu! ", commentary, score, fake_event)
    print("✅ Powiadomienia wysłane!")


if __name__ == "__main__":
    simulate_goal()
