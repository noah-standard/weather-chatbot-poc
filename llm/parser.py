from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# 사용할 모델 지정 (KoAlpaca 또는 KoGPT 등 HuggingFace 모델)
# MODEL_NAME = "beomi/KoAlpaca-Polyglot-5.8B"
MODEL_NAME = "beomi/KcELECTRA-base-v2022"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
# model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, device_map="auto")
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map={"": "cpu"}  # 전체를 CPU에 로드
)
model.eval()

import re

def extract_weather_query(user_input: str):
    # ✅ 1차: LLM 기반 파싱 시도
    prompt = f"""
사용자의 기상 관련 질문을 분석하여 날짜, 지역, 기상요소를 구조화된 형태로 추출하세요.
출력 형식은 JSON이며 key는 region, date, element 입니다.

입력: "{user_input}"
출력:
"""
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    inputs.pop("token_type_ids", None)

    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=100,
            do_sample=False,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.eos_token_id
        )

    decoded_output = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    extracted_part = decoded_output.split("출력:")[-1].strip()

    try:
        result = eval(extracted_part)
        if all(k in result for k in ("region", "date", "element")):
            return result
    except:
        pass

    # ✅ 2차: fallback - 정규식 기반 추출
    date = next((d for d in ["오늘", "내일", "모레", "글피"] if d in user_input), None)
    region = next((r for r in ["서울", "부산", "대구", "광주", "대전", "제주"] if r in user_input), None)
    element = next((e for e in ["비", "폭우", "눈", "강풍"] if e in user_input), None)

    if date and region and element:
        return {"region": region, "date": date, "element": element}
    return None
