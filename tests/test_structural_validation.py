from app.domain.structural_validation import validate_structure

def test_validate_structure_empty_file_returns_error(tmp_path):
    p = tmp_path / "empty.dat"
    p.write_text("", encoding="utf-8")
    assert validate_structure(str(p)) == "File empty"

def test_validate_structure_short_header_rejected(tmp_path):
    p = tmp_path / "short_header.dat"
    p.write_text("H123\nT" + ("x" * 29) + "\n", encoding="utf-8")
    assert validate_structure(str(p)) == "Header invalid"

def test_validate_structure_header_only_returns_trailer_error(tmp_path):
    p = tmp_path / "header_only.dat"
    p.write_text("H" + ("x" * 29) + "\n", encoding="utf-8")  # len == 30
    assert validate_structure(str(p)) == "Trailler invalid"