from file_manager import FileManager

def test_file_create_read(tmp_path):
    file = tmp_path / "test.txt"
    FileManager.write(str(file), "hello")
    assert FileManager.read(str(file)) == "hello"
