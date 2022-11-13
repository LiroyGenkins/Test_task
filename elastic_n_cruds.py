from elasticsearch import helpers, Elasticsearch, NotFoundError
import pandas as pd
import model

class Elastic():
    def __init__(self):
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        self.reader = pd.read_csv("posts.csv")
        self.index = "post"
        self.csv_reader()

    def gendata(self):
        for i, row in self.reader.iterrows():
            yield {
                "_index": "post",
                "_id": i,
                "_source": {"text": row['text']}
            }

    def csv_reader(self):
        # Создание индекса в эластике
        try:
            if self.es.indices.exists(self.index):
                self.es.indices.delete(index=self.index)
            self.es.indices.create(index=self.index)
            helpers.bulk(self.es, self.gendata())
        except (Exception) as error:
            print("Ошибка при работе с elastic", error)

    def search_by_text(self, text):
        result = self.es.search(index=self.index, body={"size": 20, "query": {"match": {'text': text}}})
        ids = [int(item["_id"]) for item in result["hits"]["hits"]]
        return ids

    def search_post(self, db, search_text):
        ids = self.search_by_text(search_text)
        result =db.query(model.Post).filter(model.Post.id.in_(ids)).order_by(model.Post.created_date.desc()).all()
        return result

    def search_delete_by_id(self, id):
        result = self.es.search(index=self.index, body={"size": 1, "query": {"match": {'_id': id}}})
        if len(result['hits']['hits']) != 0:
            self.es.delete(index=self.index, id=id)
            return True, result['hits']['hits']
        return False, 'ID не найден!'

    def delete_by_id(self, db, id):
        flag, item = self.search_delete_by_id(id)
        if flag:
            db_result = bool(db.query(model.Post).filter(model.Post.id == id).delete())
            db.commit()
        return 'Ok' if flag and db_result else item


# Импортировал данные в Индекс Эластика используя add_to_index через cmd.
# Обязательно проверьте запущен ли Elasticsearch через cmd или как сервис!
# Полный код импорта через интепретатор Python:
# from app.models import Docs
# from app.elastic import add_to_index
# for post in Docs.query.all():\
#     add_to_index('docs', post)
#
# Удалить индекс из эластика:
# from app import es
# es.indices.delete(index='docs')