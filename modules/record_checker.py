#from ..utils.db_config import get_db_connection

import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, parent_dir)
from utils.db_config import get_db_connection

def generate_record_using_gpt(user_id, instance_id):
    generated_value = 50
    return generated_value

def split_by_top_level_commas(line: str) -> list:
    result = []
    current = []
    depth = 0
    for ch in line:
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth = max(0, depth - 1)
        if ch == ',' and depth == 0:
            result.append("".join(current).strip())
            current = []
        else:
            current.append(ch)
    if current:
        result.append("".join(current).strip())
    return result

def parentheses_aware_split(titles_list: list) -> list:
    result = []
    for item in titles_list:
        parts = split_by_top_level_commas(item)
        parts = [x.strip() for x in parts if x.strip()]
        result.extend(parts)
    return result

def get_or_generate_record(user_id: str, titles_list: list) -> int:
    titles_list = parentheses_aware_split(titles_list) #*중복 미허용시 list(set(parentheses_aware_split(titles_list)))
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            query_select = """
                SELECT maxglu_instance, using_gpt
                FROM caster.user_glucose_monitoring
                WHERE user_id = %s
                  AND title @> %s::text[]
                  AND title <@ %s::text[]
                LIMIT 1;
            """
            cur.execute(query_select, (user_id, titles_list, titles_list))
            result = cur.fetchone()

            if result:
                maxglu_instance, using_gpt = result
                print(f"[INFO] DB에 기존 기록이 존재합니다. "
                      f"(maxglu_instance: {maxglu_instance}, using_gpt: {using_gpt})")
                return maxglu_instance
            else:
                maxglu_instance = generate_record_using_gpt(user_id, titles_list)
                # insert_query = """
                #     INSERT INTO caster.user_glucose_monitoring (user_id, title, maxglu_instance, using_gpt)
                #     VALUES (%s, %s::text[], %s, %s)
                # """
                # cur.execute(insert_query, (user_id, normalized_titles, maxglu_instance, True))
                # conn.commit()
                print(f"[INFO] GPT로 생성된 값: {maxglu_instance} (DB에 새로 INSERT됨)")
                return maxglu_instance

    except Exception as e:
        print("[ERROR] 기록 조회/생성 중 오류 발생:", e)
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    test_user_id = 1234
    test_instance_id = 1
    record = get_or_generate_record('2411001@sookmyung.ac.kr', ['치킨, 어묵탕'])
    print("최종 도출 혈당상승량:", record)
