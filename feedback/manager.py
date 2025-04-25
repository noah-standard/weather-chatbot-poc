# weather_chatbot_poc/feedback/manager.py
import json
import os
from datetime import datetime

FEEDBACK_PATH = "weather_chatbot_poc/feedback/store.json"

# 피드백 저장

def store_feedback(feedback_data: dict):
    os.makedirs(os.path.dirname(FEEDBACK_PATH), exist_ok=True)

    feedback_record = {
        "timestamp": datetime.now().isoformat(),
        "user_input": feedback_data.get("user_input"),
        "region": feedback_data.get("region"),
        "date": feedback_data.get("date"),
        "prediction": feedback_data.get("prediction"),
        "actual": feedback_data.get("actual"),  # 사용자가 정답을 알려줬을 경우
        "comment": feedback_data.get("comment", "")
    }

    if os.path.exists(FEEDBACK_PATH):
        with open(FEEDBACK_PATH, "r", encoding="utf-8") as f:
            existing = json.load(f)
    else:
        existing = []

    existing.append(feedback_record)

    with open(FEEDBACK_PATH, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)

    print("💾 피드백 저장 완료!")
