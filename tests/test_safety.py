import pytest
from backend.safety import validate_sql,UnsafeQueryError

def test_select_allowed():
    assert validate_sql("SELECT * FROM students")

@pytest.mark.parametrize("sql",[
    "DROP TABLE students",
    "DELETE FROM students",
    "UPDATE students SET year=4",
    "INSERT INTO students VALUES(9,'x',1,'IT')",
    "SELECT * FROM students; SELECT * FROM fees"
])
def test_mutations_blocked(sql):
    with pytest.raises(UnsafeQueryError):
        validate_sql(sql)
