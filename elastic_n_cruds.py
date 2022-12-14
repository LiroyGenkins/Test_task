from elasticsearch import helpers, Elasticsearch
import pandas as pd
import model

class Elastic():
    def __init__(self, host):
        self.es = Elasticsearch([{'host': host, 'port': 9200}])
        reader = pd.read_csv("posts.csv")
        self.index = "post"
        self.csv_reader(reader)

    def gendata(self, reader):
        for i, row in reader.iterrows():
            # Задание полей в эластике
            yield {
                "_index": "post",
                "_id": i,
                "_source": {"text": row['text']}
            }

    def csv_reader(self, reader):
        # Создание индекса в эластике
        try:
            if self.es.indices.exists(self.index):
                self.es.indices.delete(index=self.index)
            self.es.indices.create(index=self.index)
            helpers.bulk(self.es, self.gendata(reader))
        except (Exception) as error:
            print("Ошибка при работе с elastic", error)

    def search_by_text(self, text):
        # Поиск в эластике по тексту
        result = self.es.search(index=self.index, body={"size": 20, "query": {"match": {'text': text}}})
        ids = [int(item["_id"]) for item in result["hits"]["hits"]]
        return ids

    def search_post(self, db, search_text):
        # Запуск полнотекстового поиска и сортировка результатов
        ids = self.search_by_text(search_text)
        result =db.query(model.Post).filter(model.Post.id.in_(ids)).order_by(model.Post.created_date.desc()).all()
        return result

    def search_delete_by_id(self, id):
        # поиск в индексе по id и удаление соответствующей записи
        result = self.es.search(index=self.index, body={"size": 1, "query": {"match": {'_id': id}}})
        if len(result['hits']['hits']) != 0:
            self.es.delete(index=self.index, id=id)
            return True, result['hits']['hits']
        return False, 'ID не найден!'

    def delete_by_id(self, db, id):
        # удаление из БД
        db_result = bool(db.query(model.Post).filter(model.Post.id == id).delete())
        if db_result:
            flag, item = self.search_delete_by_id(id)
            if flag:
                db.commit()
                return 'Ok'
            return item
        return 'Deleting from database failed'