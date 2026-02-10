import os

def validate_structure(file_path: str) -> str | None:
    error_message = validate_size(file_path)
    if error_message:
        return error_message

    with open(file_path, "r") as file:
        first_line = next(file).strip("\r\n")
        last_line = None

        for line in file:
            last_line = line.strip("\r\n")

    error_message = validate_header(first_line)
    if error_message:
        return error_message
    
    error_message = validate_trailer(last_line)
    if error_message:
        return error_message

    return None

def validate_size(file_path: str)  -> str | None:
    if not os.path.getsize(file_path) > 0:
        print('File is empty')
        return 'File empty'

    return None

def validate_header(line: str) -> str | None:
    if len(line) < 30:
        return 'Header invalid'
    
    return None

def validate_trailer(line: str) -> str | None:
    if not line or len(line) < 30:
        return 'Trailler invalid'

    return None
