import sys
import os
import yaml
import openai
from config.db_config import get_db_connection

openai.api_key = os.environ.get("OPENAI_API_KEY")

def load_prompt_config(filepath="prompts/glucose.yaml"):
    with open(filepath, "r") as file:
        prompt_config = yaml.safe_load(file)
    return prompt_config

def generate_gpt_prompt(titles_list: list, user_id: str, nutrition): # nutrition: dict
    try: 
        conn = get_db_connection()
        with conn.cursor() as cur:
            query_select = """
                            SELECT fbg, user_max_glu
                            FROM caster.user_glucose_monitoring
                            WHERE user_id = %s
                            LIMIT 1;
                        """
            cur.execute(query_select, (user_id,))
            result = cur.fetchone()
            fbg, user_max_glu = result
        user_info = (
            f"Foods: {titles_list}\n"
            f"FBG: {fbg}\n"
            f"User Max Glucose: {user_max_glu}\n"
            f"Cluster: {3}\n" #f"Cluster: {user_data['cluster']}\n"
            f"Nutritional Info: starch {nutrition['starch']}, sugar {nutrition['sugar']}, carbohydrate {nutrition['carbohydrate']}, protein {nutrition['protein']}, fat {nutrition['fat']}, dietary fiber {nutrition['dietaryfiber']}"
        )
    except Exception as e:
        sys.stdout.write("[ERROR] 유저 정보 조회 오류:", e)
        raise
    finally:
        conn.close()
    return user_info

def get_gpt_response(title, user_id, nutrition):
    prompt_config = load_prompt_config()
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": prompt_config['system_prompt']
            },
            {
                "role": "user",
                "content": prompt_config['user_prompt']+ generate_gpt_prompt(title, user_id, nutrition)
            }
        ],
        temperature=0,
        presence_penalty=0.7,
    )
    response = completion.choices[0].message.content.strip()
    gpt_answer = round(float(response.split("Answer: [[")[-1].split("]]")[0].strip()))
    sys.stdout.write("gpt_answer: " + str(gpt_answer))
    return gpt_answer
