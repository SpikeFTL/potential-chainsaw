import re

BLOCKED={"alter","attach","create","delete","detach","drop","exec","grant","insert","merge","pragma","replace","revoke","truncate","update","vacuum"}
ALLOWED=("select ","show ","describe ","explain ","with ")

class UnsafeQueryError(ValueError):
    pass

def validate_prompt(prompt:str)->str:
    prompt=prompt.strip()
    if not prompt:
        raise UnsafeQueryError("Question cannot be empty.")
    if set(re.findall(r"[a-z_]+",prompt.lower())) & BLOCKED:
        raise UnsafeQueryError("Command not allowed. SQLMind is running in read-only mode.")
    return prompt

def validate_sql(sql:str)->str:
    sql=sql.strip().rstrip(";").strip()
    low=sql.lower()
    if not sql:
        raise UnsafeQueryError("SQL query cannot be empty.")
    if ";" in sql:
        raise UnsafeQueryError("Only one SQL statement is allowed.")
    if not low.startswith(ALLOWED):
        raise UnsafeQueryError("Only read-only queries are allowed.")
    bad=sorted(set(re.findall(r"[a-z_]+",low)) & BLOCKED)
    if bad:
        raise UnsafeQueryError(f"Blocked SQL keyword: {bad[0]}.")
    return sql

def add_limit(sql:str,limit:int)->str:
    if sql.lower().lstrip().startswith(("select ","with ")) and not re.search(r"\blimit\s+\d+\b",sql,re.I):
        return f"{sql} LIMIT {limit}"
    return sql
