import sys
from config.db_config import get_db_connection
from modules.glucose_generator import get_gpt_response
from utils.text_utils import parentheses_aware_split

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
                sys.stdout.write(f"[INFO] 기존 기록 DB 존재"
                      f"(maxglu_instance: {maxglu_instance}, using_gpt: {using_gpt})")
                return maxglu_instance
            else:
                maxglu_instance = get_gpt_response(titles_list, user_id, {'starch': 15, 'sugar': 25, 'carbohydrate': 10, 'protein': 5, 'fat': 2, 'dietaryfiber': 0}) #!db영양성분으로교체
                # insert_query = """
                #     INSERT INTO caster.user_glucose_monitoring (user_id, title, maxglu_instance, using_gpt)
                #     VALUES (%s, %s::text[], %s, %s)
                # """
                # cur.execute(insert_query, (user_id, normalized_titles, maxglu_instance, True))
                # conn.commit()
                print(f"[INFO] GPT 생성 값: {maxglu_instance} (new record INSERT)")
                return maxglu_instance

    except Exception as e:
        sys.stdout.write("[ERROR] 기록 조회/생성 중 오류 발생:", e)
        raise
    finally:
        conn.close()
