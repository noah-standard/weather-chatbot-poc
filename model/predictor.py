# weather_chatbot_poc/model/predictor.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "data", "risk_model.pkl")


# 사용할 피처 목록
FEATURE_COLUMNS = [
    "temp", "temp_max", "temp_min", "wind_speed", "vector_wind_speed",
    "max_gust_speed", "cloud_cover", "precipitation", "sea_level_pressure",
    "dew_point", "visibility", "cloud_height"
]

# 임시 라벨 생성 함수 (임의 기준: 강수량이 5mm 이상이면 특보 위험)
def create_label(df: pd.DataFrame) -> pd.Series:
    return (df["precipitation"] >= 5.0).astype(int)

# 모델 학습 및 저장
def train_model(csv_path: str):
    df = pd.read_csv(csv_path)
    df = df.dropna(subset=FEATURE_COLUMNS)
    df["label"] = create_label(df)
    X = df[FEATURE_COLUMNS]
    y = df["label"]

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)
    print("✅ 예측 모델 학습 및 저장 완료")

# 모델 로딩
def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("예측 모델이 존재하지 않습니다. 먼저 train_model을 실행하세요.")
    return joblib.load(MODEL_PATH)

# 예측 함수 (간단히 가장 최근 데이터 중 해당 지역 선택)
def predict_risk(model, region: str, date: str) -> float:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_PATH = os.path.join(BASE_DIR, "data", "201901.csv")
    df = pd.read_csv(DATA_PATH)

    # 날짜 변환
    target_date = pd.to_datetime(date, errors="coerce")
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")

    # 날짜 + region 필터링 (region은 station_id로 간주)
    region_code = 90 if region.startswith("서울") else 90  # TODO: 매핑 적용
    df_region = df[df["station_id"] == region_code]
    df_target = df_region[df_region["datetime"].dt.date == target_date.date()]

    if df_target.empty:
        return 0.0

    # 가장 최근 데이터 1건으로 예측
    X = df_target[FEATURE_COLUMNS].iloc[-1:]
    prob = model.predict_proba(X)[0][1]  # 1 = 특보 위험일 확률
    return round(prob, 2)
