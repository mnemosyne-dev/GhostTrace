import re


def detect_sensitive_data(text):

    result = {}
    risk = 0


    patterns = {

        "Email":
        r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",

        "Phone":
        r"\b[6-9]\d{9}\b",

        "Password":
        r"(?i)(password|passwd|pwd)\s*[:=]\s*\S+",

        "API Key":
        r"(?i)(api[_-]?key|token|secret)\s*[:=]\s*\S+",

        "Aadhaar":
        r"\b\d{4}\s?\d{4}\s?\d{4}\b",

        "PAN":
        r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"
    }


    weight = {

        "Email":10,
        "Phone":15,
        "Password":50,
        "API Key":60,
        "Aadhaar":50,
        "PAN":40
    }


    for name,pattern in patterns.items():

        found = re.findall(pattern,text)

        if found:

            result[name] = found

            risk += weight[name] * len(found)


    return result,risk