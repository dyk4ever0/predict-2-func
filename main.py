import sys
from modules.record_handler import get_or_generate_record

if __name__ == "__main__":
    test_user_id = '2411001@sookmyung.ac.kr'
    titles_list = ['캘리포니아롤']
    
    record = get_or_generate_record(test_user_id, titles_list)
    sys.stdout.write("\nvalue: " + str(record))