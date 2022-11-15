import uvicorn
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
import time

time.sleep(80)

import model
from elastic_n_cruds import Elastic
from config import SessionLocal, engine

# Для записи в бд другого файла .csv надо раскомментировать следующий кусок кода:
# import os
# import pandas as pd
# reader = pd.read_csv("НАЗВАНИЕ_ФАЙЛА")
# os.remove('posts.db')
# sqlite_connection = engine.connect()
# reader.to_sql("posts", sqlite_connection, index_label="id")
# sqlite_connection.close()

model.Base.metadata.create_all(bind=engine)

app = FastAPI()
es = Elastic()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#http://127.0.0.1:8000/posts/delete/0
#get в этом методе нужен чтобы протестировать через браузер
@app.get("/posts/delete/{id}")  #как только появится возможность задавать метод запроса его следует заменить на delete
def remove_post(id: int, db: Session = Depends(get_db)):
    result = es.delete_by_id(db=db, id=id)
    return {"result": result}

#http://127.0.0.1:8000/posts/search?text=текст
@app.get("/posts/search")
def search_post(text: str, db: Session = Depends(get_db)):
    results_list = es.search_post(db=db, search_text=text)
    return {"results": results_list}


def main():
    uvicorn.run("main:app", host="127.0.0.1", reload=False, use_colors=True)

if __name__ == "__main__":
    main()
