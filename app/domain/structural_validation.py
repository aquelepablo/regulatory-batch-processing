import os
import psycopg2

def validate_structure(file_path: str) -> tuple[bool, str | None]:
    print('validate_structure')
     
    is_valid, error_message = validate_size(file_path)
    if not is_valid:
        return False, error_message


    with open(file_path, "r") as file:
        first_line = next(file).strip()
        last_line = None

        #TODO: For bigger files, best to go backwards
        for line in file:
            last_line = line.strip()

    is_valid, error_message = validate_header(first_line)
    if not is_valid:
        return False, error_message
    
    is_valid, error_message = validate_trailer(last_line)
    if not is_valid:
        return False, error_message

    return True, None

def validate_size(file_path: str)  -> tuple[bool, str | None]:
    print('validate_size')
    
    if not os.path.getsize(file_path) > 0:
        print('File is empty')
        return False, 'File empty'

    return True, None

def validate_header(line: str) -> tuple[bool, str | None]:
    print('validate_header', line)
    if len(line) < 5:
        return False, 'Header invalid'
    
    return True, None

def validate_trailer(line: str) -> tuple[bool, str | None]:
    print('validate_trailer', line)
    if len(line) < 5:
        return False, 'Trailler invalid'

    return True, None
