import os.path
import sys
sys.path.append(os.path.abspath(os.getcwd()))

from src import controler


if __name__ == "__main__":
    # controler.create()
    controler.scrape_and_store()
