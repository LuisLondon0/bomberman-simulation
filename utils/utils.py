def load_map(file_path):
    with open(file_path, 'r') as f:
        map = [line.strip().split(",") for line in f.readlines()]

    map.reverse()
    return map