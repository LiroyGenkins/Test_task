import os
import sys
import pandas as pd
from config import engine

def main():
    reader = pd.read_csv(sys.argv[1])
    os.remove('posts.db')
    sqlite_connection = engine.connect()
    reader.to_sql("posts", sqlite_connection, index_label="id")
    sqlite_connection.close()


if __name__ == "__main__":
    main()