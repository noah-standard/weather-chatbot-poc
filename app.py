# weather_chatbot_poc/app.py
from flask import Flask, request, jsonify
from model.predictor import load_model, predict_risk
from llm.parser import extract_weather_query
from feedback.manager import store_feedback
from utils.date_utils import parse_relative_date
import pandas as pd

app = Flask(__name__)
model = load_model()

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    parsed = extract_weather_query(user_input)

    if not parsed:
        return jsonify({"response": "죄송해요, 질문을 이해하지 못했어요."})

    region, date_keyword, element = parsed["region"], parsed["date"], parsed["element"]
    date = parse_relative_date(date_keyword)
    prediction = predict_risk(model, region, date)

    response = f"{date} {region}의 {element} 특보 가능성은 {prediction * 100:.1f}%입니다."
    return jsonify({
        "response": response,
        "parsed": parsed,
        "prediction": prediction
    })

@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.json
    store_feedback(data)
    return jsonify({"message": "피드백 감사합니다! 개선에 반영하겠습니다."})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
