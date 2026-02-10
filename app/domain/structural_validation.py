import os
import psycopg2

def validate_structure(file_path: str) -> str | None:
    print('validate_structure')
     
    error_message = validate_size(file_path)
    if error_message:
        return error_message

    with open(file_path, "r") as file:
        first_line = next(file).strip("\r\n")
        last_line = None

        #TODO: For bigger files, best to go backwards
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
    print('validate_size')
    
    if not os.path.getsize(file_path) > 0:
        print('File is empty')
        return 'File empty'

    return None

def validate_header(line: str) -> str | None:
    print('validate_header', line)
    if len(line) < 30:
        return 'Header invalid'
    
    return None

def validate_trailer(line: str) -> str | None:
    print('validate_trailer', line)
    if len(line) < 30:
        return 'Trailler invalid'

    return None
