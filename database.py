"""
client = MongoClient("mongodb://root:12345678@34.68.79.134:27017")
db = client['note']
collection = db.col

student = {
    'id': '20170101',
    'name': 'Jordan',
    'age': 20,
    'gender': 'male'
}

result = collection.insert_one(student)
print(result)
"""

def database(data, name):
    print("hello")
    fo = open('static/' + name, 'w')
    fo.write(data)
    fo.close()

if __name__ == '__main__':
    database("hello", 'hello')