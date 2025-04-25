# weather_chatbot_poc/data/preprocess_weather.py
import pandas as pd

def preprocess_weather_data(input_path: str, output_path: str):
    df = None  # 미리 선언
    for enc in ["utf-8", "cp949", "euc-kr"]:
        try:
            df = pd.read_csv(input_path, encoding=enc)
            break
        except Exception:
            continue

    if df is None:
        raise ValueError("CSV 파일을 불러오는 데 실패했습니다. 인코딩을 확인하세요.")

    # 이후 전처리 진행
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    df = df.dropna()

    if "precipitation" in df.columns:
        df["label"] = (df["precipitation"] >= 5.0).astype(int)

    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"✅ 전처리 완료: {output_path}")


if __name__ == "__main__":
    preprocess_weather_data(
        input_path="./201901.csv",
        output_path="./weather_sample_processed.csv"
    )
