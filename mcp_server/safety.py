import re

BLOCKED={"alter","attach","create","delete","detach","drop","exec","grant","insert","merge","pragma","replace","revoke","truncate","update","vacuum"}

def validate_read_only_query(sql:str):
    s=sql.strip().rstrip(";").strip()
    low=s.lower()
    if not low.startswith(("select ","with ")):
        return False,"Unsafe SQL operation detected."
    if ";" in s:
        return False,"Only one SQL statement is allowed."
    if set(re.findall(r"[a-z_]+",low)) & BLOCKED:
        return False,"Unsafe SQL operation detected."
    return True,""
