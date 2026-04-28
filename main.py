from src.Server import Server

if __name__ == "__main__":
    server = Server(dev=False)
    server.run()