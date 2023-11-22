import re

def keep_arabic(text):
    arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]+')
    # Regular expression pattern for Arabic Unicode ranges

    arabic_text = arabic_pattern.findall(text)
    # Find all matches of Arabic characters in the text

    cleaned_text = ''.join(arabic_text)
    # Join the matches to form a string containing only Arabic characters

    return cleaned_text