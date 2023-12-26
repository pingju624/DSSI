import pandas as pd
import re

def criterion_1(title):
    # 要搜索的中文字列表
    target_characters = ["他", "她", "它", "他們", "她們", "它們", "祂", "牠", "你", "妳", "這"]
    if any(target_character in title for target_character in target_characters):
        return 1
    else:
        return 0
    
def criterion_2(title):
    # 要搜索的中文字列表
    target_characters = ["崩", "砲", "瘋", "扯", "狂", "激", "慘", "笑", "哭", "酸", "諷", "神", "猛", "讚", "嗆", "轟", "罵", "怒", "怒斥", "冷回", "飆罵", "怒批", "痛批", "打臉", "譴責"]
    if any(target_character in title for target_character in target_characters):
        return 1
    else:
        return 0
    
def criterion_3(title):
    # Check if the title contains two or more of the specified characters ('!', '?', '！', '？')
    if len(re.findall(r'[!？！?]', title)) >= 2:
        return 1
    else:
        return 0
    
def criterion_4(title):
    # target_characters = r'\b(?!驚天|驚訝|辯才|人才|步步驚心|專才|育才|武嚇|才是|恐嚇)\b(居然|竟然|竟|甚至|甚而|反而|反倒|原來|未料|不料|想不到|沒想到|才|卻|驚)'
    target_characters = r'(?!驚天|驚訝|辯才|人才|步步驚心|專才|育才|武嚇|才是|恐嚇)(居然|竟然|竟|甚至|甚而|反而|反倒|原來|未料|不料|想不到|沒想到|才|卻|驚)'
    match = re.search(target_characters, title)
    if match:
        return 1
    else:
        return 0
    
def criterion_5(title):
    # 要搜索的中文字列表
    target_characters = ["⋯⋯", "⋯", "...", "…"]
    if any(target_character in title for target_character in target_characters):
        return 1
    else:
        return 0
def chinese_to_arabic(chinese_number):
    chinese_number_map = {
        '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
        '六': 6, '七': 7, '八': 8, '九': 9, '十': 10
    }

    number = 0

    for char in chinese_number:
        if char in chinese_number_map:
            number = chinese_number_map[char]
            chinese_number = chinese_number.replace(char, str(number))

    return chinese_number

def criterion_6(news_title):
    news_title = chinese_to_arabic(news_title)
    quantifiers = {"個", "種", "項", "位", "張", "大", "招"}

    # 空白去除
    title_without_spaces = "".join(news_title.split())

    for quantifier in quantifiers:
        if quantifier in title_without_spaces:
            try:
                if quantifier == "個":
                    month_char = title_without_spaces.split(f"{quantifier}")[1][0]
                    if month_char == "月":
                        return 0
                    else:
                        last_char = title_without_spaces.split(f"{quantifier}")[0][-1]
                        if last_char.isdigit():
                            return 1
                else:
                    last_char = title_without_spaces.split(f"{quantifier}")[0][-1]
                    if last_char.isdigit():
                        return 1
            except IndexError:
                pass
    return 0

def criterion_7(title):
    # 要搜索的中文字列表
    target_characters = ["如何", "該怎麼做", "該如何"]
    if any(target_character in title for target_character in target_characters):
        return 1
    else:
        return 0
    
def criterion_8(title):
    # 要搜索的中文字列表
    target_characters = ["嗯", "哎", "咦", "啊", "唉", "呦"]
    if any(target_character in title for target_character in target_characters):
        return 1
    else:
        return 0

# 爆料文體
def criterion_9(title):
    # 要搜索的中文字列表
    target_characters = ["曝光", "自爆", "爆料", "再爆"]
    if any(target_character in title for target_character in target_characters):
        return 1
    else:
        return 0

# 八卦文體
def criterion_10(title):
    # 要搜索的中文字列表
    target_characters = ["正妹", "美女", "老司機", "傻眼", "性感", "辣", "小模", "女神", "嫩", "甜美", "型男", "嘟嘴", "寶寶", "可愛"]
    # 如果標題中包含指定的任一關鍵字，返回 True，否則返回 False
    if any(target_character in title for target_character in target_characters):
        return 1
    else:
        return 0

# 句尾詞「了」
def criterion_11(title):
    if re.search(r'了', title):
        return 1
    # 如果以上條件都不符合，返回 False
    return 0

# 群眾效果
def criterion_12(title):
    # 如果標題中包含 '網'，但不包含 '網路' 和 '網站'，返回 True
    if re.search(r'網(?!路|站|銀)', title):
        return 1
    # 如果以上條件都不滿足，返回 False
    return 0

# 誇大
def criterion_13(title):
    target_characters = ["最", "太", "狠", "極其", "更加", "非常", "格外", "越加", "神", "狂", "超"]
    # 如果標題中包含指定的任一關鍵字，返回 True，否則返回 False
    if any(target_character in title for target_character in target_characters):
        return 1
    else:
        return 0

# 不確定性
def criterion_14(title):
    target_characters = r'(?!宣傳|傳統|傳奇|傳遞|頻傳|銘傳|傳訊|傳喚|傳承|遠傳|傳記|驚恐|恐嚇|恐怖|唯恐天下不亂|質疑|遲疑|疑點|疑惑)(傳|瘋傳|轉傳|網傳|誤傳|疑|恐)'

    match = re.search(target_characters, title)

    if match:
        return 1
    else:
        return 0
#微疑問
def criterion_15(title):
    # Check if the title contains two or more of the specified characters ('!', '?', '！', '？')
    if len(re.findall(r'[!？！?]', title)) >= 1:
        return 1
    else:
        return 0
    
# 定義誘餌式標題判斷函數
def is_clickbait(title):
    criteria_results = [criterion_1(title), criterion_2(title), criterion_3(title), criterion_4(title), criterion_5(title), criterion_6(title), criterion_7(title), criterion_8(title), criterion_9(title), criterion_10(title), criterion_11(title), criterion_12(title), criterion_13(title), criterion_14(title),criterion_15(title)]
    print(criteria_results)
    if criterion_1(title) or criterion_3(title) or criterion_5(title) or criterion_7(title) or criterion_8(title) or criterion_9(title) or criterion_12(title) == 1:
        return 1
    elif sum(criteria_results) >= 2:
        return 1
    else:
        return 0