from src.Server import Server

if __name__ == "__main__":
    server = Server(dev=True)
    server_thread = server.run()
    if server_thread:
        server_thread.join()