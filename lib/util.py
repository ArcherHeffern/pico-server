def parse_str_to_bool(b: str) -> bool|None:
    b = b.lower()
    if b == "true":
        return True
    elif b == "false":
        return False
    return None
