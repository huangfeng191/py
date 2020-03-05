# -*- coding: UTF-8 -*-
# Module  : py
# Description :与cell 配置有关的 对象
# Author  : Wujj
# Date    : 2020/2/16
# Version : 1.0

from factor import *

from  customs.tide.service import utils as tide_utils
class CellLoopConfig:
    def __init__(self, layer):
        self.layer = layer
        basket = layer.get("basket")
        self.type = basket.get("loopType")
        self.config = basket.get("loopConfig")
        self.origin = OriginConfig(self.type, self.config, self.layer)

    def get(self):
        return self.origin.get()


class CellSourceConfig:
    def __init__(self, layer):
        self.layer=layer
        basket=layer.get("basket")
        self.type=basket.get("sourceType")
        self.config=basket.get("sourceConfig")
        self.origin= OriginConfig(self.type,self.config,self.layer)
    def get(self):
        return self.origin.get()



class CellRuleConfig:
    '''
        {
          "table":{
                query:{
                "is_open":1
                },

                "limits": {
                    "size": 7
                },
                "sorts": {
                    "order": [{"Field": "cal_date", "Type": true}]
                }
          },
          "agg":{

          }
        }

    '''

    def __init__(self, type, config, layer):
        self.type = type
        self.config = config.get(type) or {}
        self.layer = layer

    def get(self):
        rule = {}
        if self.type == "table":
            rule.update(self.config)
            QP = QueryParsed(self.config.get("query"), self.layer)
            rule["query"] = QP.get()
        elif self.type == "agg":
            pass
        return rule


class CellOutConfig:
    '''
    此处才生成take
    '''
    def __init__(self, type, config,layer):
        self.type=type
        self.config=config
        self.layer=layer
        self.layer["take"]={
            "type":type,
            "key":layer.get("fetch").get("key")
        }
        self.layer["take"][type]={
            "hook":"cell"
        }

    def table(self):
        config = self.config["table"]
        take=self.layer["take"]

        o = take["table"]
        o["nm"]=config.get("nm")




    def log(self):
        config=self.config["log"]
        take = self.layer["take"]

        o=take["log"]
        if config.get("field"):
            o["fields"]=[config.get("field")]
        else:
            o["fields"] = config.get("fields")


    def accrue(self):
        if self.type:
            if(self.type=="log"):
                self.log()
            elif(self.type=="table"):
                self.table()
        else:
            raise Exception("CellOutConfig error ")
        pass
    def go(self,data):
        if self.config.get("regulates"):
             T=TransformConfig(self.config.get("regulates"))
             data=T.go(data)
        self.accrue() # 绑定 take
        return data


