### last update: 2025-02-06  
---
### 실행
```
python3 main.py
python3 main.py > /dev/null
```

## 전체 흐름  
main.py → get_or_generate_record() → (제목 변환 → DB 연결 및 기존 기록 조회)  
└─ 기록 없음 → get_gpt_response() → (프롬프트 설정 로드 → GPT 프롬프트 생성 → OpenAI API 호출 → 응답 파싱)   

[main.py]   
├─ 변수 초기화:   
     • test_user_id   
     • titles_list   
└─ 함수 호출:   
      get_or_generate_record(user_id, titles_list)   
           ├─ 리스트 items 필터링 (utils/text_utils.py)   
                • titles_list → parentheses_aware_split()   
           ├─ DB 연결 (config/db_config.py)   
                • PostgreSQL 연결 생성   
           ├─ 기존 기록 조회   
                • SELECT maxglu_instance, using_gpt   
                • 존재하면 기존 maxglu_instance 반환   
                • 기록 없음:   
                 └─ GPT 응답 생성   
                       get_gpt_response(titles_list, user_id, nutrition)   
                            ├─ 텍스트 로드 (modules/glucose_generator.py)   
                                 • load_prompt_config() prompts/glucose.yaml 파일 읽기   
                            ├─ GPT 프롬프트 생성   
                                 • generate_gpt_prompt(titles_list, user_id, nutrition)   
                                   ├─ get_db_connection() 호출 (config/db_config.py)   
                                   └─ SQL SELECT 실행하여 fbg, user_max_glu 조회 후 포맷팅   
                            ├─ OpenAI API 호출   
                                 • openai.ChatCompletion.create()로 GPT 응답 생성   
                            └─ 응답 파싱   
                                 • GPT 응답에서 gpt_answer 추출 및 반환   