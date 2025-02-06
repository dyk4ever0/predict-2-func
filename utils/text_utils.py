def split_by_top_level_commas(line: str) -> list:
    """
    ['치킨 , 피자'] → ['치킨', '피자']
    ['치킨('무', '콜라')', '피자'] → ['치킨('무', '콜라')', '피자']
    """
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