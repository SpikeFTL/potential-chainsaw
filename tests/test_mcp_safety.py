from mcp_server.safety import validate_read_only_query

def test_mcp_allows_select():
    assert validate_read_only_query("SELECT * FROM students LIMIT 5")[0] is True

def test_mcp_blocks_drop():
    assert validate_read_only_query("DROP TABLE students")[0] is False
