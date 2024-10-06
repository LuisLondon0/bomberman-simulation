from utils.utils import load_map
from server.server import create_server

if __name__ == "__main__":
    map = load_map("data/maps/level2.txt")
    server = create_server(map)
    server.launch()