from pymongo import MongoClient

# base de datos local
# db_client= MongoClient().local

# base de datos remota
url= "mongodb+srv://test:test@cluster0.yyvoojv.mongodb.net/?retryWrites=true&w=majority" 
db_client= MongoClient(url).test