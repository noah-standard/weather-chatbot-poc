from datetime import datetime, timedelta
import re

# 한글 날짜 표현을 datetime으로 변환하는 함수
def parse_relative_date(keyword: str, today: datetime = None) -> str:
    if today is None:
        today = datetime.today()

    keyword = keyword.strip()
    keyword_map = {
        "오늘": 0,
        "내일": 1,
        "모레": 2,
        "글피": 3
    }
    if keyword in keyword_map:
        target_date = today + timedelta(days=keyword_map[keyword])
        return target_date.strftime("%Y-%m-%d")

    # YYYY-MM-DD 형식이면 그대로 반환
    if re.match(r"\d{4}-\d{2}-\d{2}", keyword):
        return keyword

    # 기타 형태는 오늘 날짜 반환
    return today.strftime("%Y-%m-%d")

# 예시 사용:
# parse_relative_date("모레") → "2025-04-27"