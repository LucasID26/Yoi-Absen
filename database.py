import pymongo 
import os 

DB = os.environ['DB']
database = pymongo.MongoClient(DB)
mydb = database["VirtualRobot"]