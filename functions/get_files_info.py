import os

def get_files_info(working_directory, directory="."):
    working_directory = os.path.abspath(working_directory)


    directory = os.path.abspath(os.path.join(working_directory, directory))
    
    try:
        common_path = os.path.commonpath([ working_directory, directory ])
        if common_path != working_directory:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    except ValueError:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.exists(directory):
        return f'Error: "{directory}" does not exist'

    if not os.path.isdir(directory):
        return f'Error: "{directory}" is not a directory'

    if not os.access(directory, os.R_OK):
        return f'Error: Cannot list "{directory}" as it is not readable'

    pretty_print = ""

    for file in os.listdir(directory):
        file_size = os.stat(os.path.join(directory, file)).st_size
        is_dir = os.path.isdir(os.path.join(directory, file))
        pretty_print += f"- {file}: file_size={file_size} bytes, is_dir={is_dir}\n"
        

    return pretty_print



