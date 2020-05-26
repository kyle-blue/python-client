from src.UI import UI
from src.Client import Client
from src.Data.Wrangler import Wrangler


def main():
    client = Client()
    wrangler = Wrangler()
    wrangler.start()

    ui = UI()  # Start all threads before here (since UI is an infinite loop run on this thread)

if __name__ == "__main__":
    main()