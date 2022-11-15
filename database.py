import random

from pymongo import MongoClient

class DataBase :
    database = MongoClient(host="localhost" , port=27017)["stages"]
    collectionsDataBase = database["stagesForUsers"]
    id = 0
    work = ""
    prise = 0
    domain = ""
    nameStage = ""
    def __init__(self):
        pass


    def insertData(self,id,work,prise,domain,nameStage):
        self.id = id                               
        self.prise = prise
        self.work = work
        self.domain = domain
        self.nameStage = nameStage
        data = {
            "id": self.id,
            "work": self.work,
            "domain": self.domain,
            "prise": self.prise,
            "nameStage": self.nameStage,
        }

        self.collectionsDataBase.insert_one(data)
 


    def delete(self,id):
        self.collectionsDataBase.delete_one({"id":id})
    def update(self,id,work,prise,domain,nameStage):
        data = {"$set":{
            "id": id,
            "work": work,
            "domain": domain,
            "prise": prise,
            "nameStage": nameStage,
        }}
        self.collectionsDataBase.update_one({"id":id},data)

    def affich(self):
        res = list(self.collectionsDataBase.find())
        return res



    def isTheIdExecteInDataBase(self,id)->bool:
        count = self.collectionsDataBase.count_documents({"id":id})
        return count == 0



    def findById(self,id):
        return self.collectionsDataBase.find({"id":id})[0]




