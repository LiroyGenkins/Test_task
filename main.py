import uvicorn
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

import model
from elastic_n_cruds import Elastic
from config import SessionLocal, engine

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
@app.get("/posts/delete/{id}")
def remove_post(id: int, db: Session = Depends(get_db)):
    result = es.delete_by_id(db=db, id=id)
    return {"result": result}

#http://127.0.0.1:8000/posts/search?text=Слив
@app.get("/posts/search")
def search_post(text: str, db: Session = Depends(get_db)):
    results_list = es.search_post(db=db, search_text=text)
    return {"results": results_list}


def main():
    uvicorn.run("main:app", host="127.0.0.1", reload=False, use_colors=True)

    # Для записи в бд ругого файла .csv
    # import os
    # reader = pd.read_csv("НАЗВАНИЕ_ФАЙЛА")
    # os.remove('posts.db')
    # sqlite_connection = engine.connect()
    # reader.to_sql("posts", sqlite_connection, if_exists='fail', index_label="id")
    # sqlite_connection.close()


if __name__ == "__main__":
    main()
