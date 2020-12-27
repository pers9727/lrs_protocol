def write(write_file, data_for_writing, mode):    # mode 'a' - for adding, 'w' - for writing
    with open(write_file, mode) as file:
        if isinstance(data_for_writing, list):
            for i in data_for_writing:
                file.write(i)
        else:
            file.write(data_for_writing)


def read(read_file):
    with open(read_file, 'r') as file:
        return list(file)