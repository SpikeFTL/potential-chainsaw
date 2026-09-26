import sqlite3
from pathlib import Path
from .safety import validate_read_only_query

class Database:
    def __init__(self,path="data/sample.db",max_rows=100):
        self.path=Path(path)
        self.max_rows=max_rows

    def connect(self):
        if not self.path.exists():
            raise RuntimeError(f"Database not found: {self.path}")
        return sqlite3.connect(f"file:{self.path.resolve().as_posix()}?mode=ro",uri=True)

    def schema(self):
        with self.connect() as c:
            tables=[r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")]
            out=[]
            for table in tables:
                cols=[]
                for r in c.execute(f'PRAGMA table_info("{table.replace(chr(34),chr(34)*2)}")'):
                    cols.append({"name":r[1],"type":r[2],"nullable":not bool(r[3]),"primary_key":bool(r[5])})
                out.append({"name":table,"columns":cols})
            return out

    def query(self,sql):
        ok,msg=validate_read_only_query(sql)
        if not ok:
            return {"success":False,"error":msg}
        with self.connect() as c:
            cur=c.execute(sql)
            rows=cur.fetchmany(self.max_rows+1)
            columns=[d[0] for d in cur.description or []]
        limited=rows[:self.max_rows]
        return {"success":True,"columns":columns,"rows":[list(r) for r in limited],"row_count":len(limited),"truncated":len(rows)>self.max_rows}
