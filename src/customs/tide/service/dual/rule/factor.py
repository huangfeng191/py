# -*- coding: UTF-8 -*-
# Module  : py
# Description :中间对象
# Author  : Wujj
# Date    : 2020/2/17
# Version : 1.0
from customs.tide.service.utils import * 
from customs.tide.service.utils.wrap import *
from customs.tide.service.gather.layer import *
from customs.tide.service.gather.log import *
from customs.tide.service.persistence import *
class QueryParsed:
    '''
     一般理解是 table 的 查询
            field:value
            field:
                type  # 可以计算得到 value
                    cycle
                        extend
                        day
                        week
                        month
                        year
                    jump
                        hook
                        fetchKey
                            take
                                table  // 1条记录

                    slot

                 value
                 assist:""   // if null get field
                 regulates
                 operate
                    "lte" ...

    '''
    def __init__(self,  config,layer,chains,**kwargs):

        self.config = config or {}
        self.layer=layer
        self.chains=chains
    def parseTypeDate(self,restrain=None,**kwargs):
        t="";
        if restrain==None or not restrain:
            t=kwargs.get("value")
        elif restrain=="extend":
            t=self.layer.get("fetch").get("key").get("t")
        else:
            t=getCycleToT(restrain)
        return t
    def parseJumpFetchKey(self,fetchKey):
        key={}
        for s in ["level","levelSn","sn"]:
            key[s]=fetchKey[s]
        if fetchKey.get("cycleLikely") =="extend":
            key["t"]=self.layer.get("fetch").get("key").get("t")
            key["cycle"]=self.layer.get("fetch").get("key").get("cycle")
        else:
            pass
        #     如果生成过 需要取历史 时间的 TODO:
        return  key
    def parseTypeJump(self,hook,fetchKey,**kwargs):

        key=self.parseJumpFetchKey(fetchKey)
        layerLog = LayerLog(hook, key)
        take=layerLog.getTake()
        fetch={"key":take.get("key")}
        cellLog=CellLog(fetch)
        ret=cellLog.getData()

        return ret


    # @method_in_wrapper("queryParse.get ")
    def get(self):
        conditions=[]
        q={

        }
        for k,v in self.config.items():
            condition = {
                "field": k,
                "operate": "=",
                "value": v
            }
            if type(v) == dict and v.get("type"):
                condition.update(v)   # 取配置值
                value=None
                if v.get("type")=="date":
                    value=self.parseTypeDate(**v)
                else:
                    d={}
                    if v.get("type")=="jump":
                        jump=v.get("jump",{})
                        d= self.parseTypeJump(jump.get("hook"),jump.get("fetchKey"))
                    elif v.get("type")=="slot":
                        hookId=self.layer.get("hookId")
                        level="cell"
                        front_chain=self.chains.getFrontChainByCellId(hookId)
                        front_take=front_chain.get(level).get("take")
                        d = self.parseTypeJump(level, front_take.get("key"))
                    if v.get("regulates"):
                        T = TransformConfig(v.get("regulates"))
                        d = T.go(d)

                    value=d.get(v.get("assist",k))

                condition["value"]=value
                if v.get("overlay")==1:
                    O=OverlayParse(self.layer)
                    v1=O.go()
                    if v1 and  utils.YMD(v1,'%Y%m%d')>value:
                        condition["value"]=utils.YMD(v1,'%Y%m%d')
                        if condition.get("operate")==">=":
                            condition["operate"]=">"
                        self.layer["fetch"]["overlay"]=  {"field":k,"value":None}
                conditions.append(condition)
            else:
                q[k]=v
        q_c=parseConditions(conditions)
        if q_c.get("$and"):
            q.update(q_c.get("$and",{}))
        field_overlay=self.layer["fetch"].get("overlay")
        if field_overlay:
            if q.get(field_overlay.get("field")) :
                field_overlay["value"]=q.get(field_overlay.get("field"))
        return q


class OriginParsed:
    '''
    type
        table

    config
        nm
        query
            field:value
            field:
                type
                    date
                    jump

    '''
    def __init__(self,type,config,layer,chains,**kwargs):
        self.type=type
        self.config=config[type]
        self.layer=layer
        self.chains=chains

    def  get(self):
        source={"type":self.type}
        if self.type=="table":
            table={}
            table.update(self.config)
            QP=QueryParsed(self.config.get("query"),self.layer,self.chains)
            table["query"]=QP.get()
            source[self.type]=table
        return source




class OriginConfig:
    '''
        提供源的可获取配置, 不输出结果
        type
            fixed
            jump
            slot
        config
            fixed
                type: table
                table:{
                    nm:""
                    query:{}
                }
    '''

    def __init__(self, type, config, layer,chains):
        self.type = type
        self.config = config.get(type) or None
        self.layer = layer
        self.chains=chains

    def getJumpParse(self,config):

        J=JumpParse(config.get("hook"),config.get("fetchKey"),self.layer)
        layerLog=J.getLog()
        take = layerLog.getTake()
        if take.get("type") == "table":
            take["table"] = queryTideTableParse(take.get(take.get("type")), take)  # 为了能正确的解析查询数据
        return take
    def getLogParse(self):
        hookId = self.layer.get("hookId")
        level = "cell"
        front_chain = self.chains.getFrontChainByCellId(hookId)
        front_take = front_chain.get(level).get("take")
        con={
            "hook":level,
            "fetchKey":front_take.get("key")
        }
        ret=self.getJumpParse(con)
        return ret

    def get(self):
        '''

        Returns:
            source
                {  // 返回可配置对象的原因是 方便以后的扩展
                    "type":"table",
                    "table":{
                        query:{},
                        nm:""
                    }
                }

        '''
        source = None
        if self.type == "fixed":
            SP = OriginParsed(self.config["type"], self.config, self.layer,self.chains)
            source = SP.get()
        elif self.type == "jump":
            take= self.getJumpParse(self.config)

            SP = OriginParsed(take["type"], take, self.layer,self.chains)
            source = SP.get()
        elif self.type == "slot":
            take = self.getLogParse()
            SP = OriginParsed(take["type"], take, self.layer, self.chains)
            source = SP.get()

        return source



class TransformRegulate:
    '''
        数据转换的规则: 单个规则 
        object:
            quote:  中的对象 字段改名 {"field1":"field2" ,"field3":"field4" }
            restrain: 提取有用的字段 ["field1","field2"...]
        array:
            extract 
                way 
                    rowsToField
                        fields:[f1,f2,f3...]



        func go(data ) start translate 
    '''
    def __init__(self,type,config):
        self.type=type
        self.config=config

    def  quote(self,o={}):
        '''
        quote ={"field1":"field2" ,"field3":"field4" }
        Args:
            o:

        Returns:

        '''
        config=self.config.get("quote")
        for k,q in config.items():
            o[k]=o[q]
            if o.has_key(q):
                del o[q]
    def restrain(self,o={}):
        '''
        restrain=["field1","field2"...]
        Args:
            o:

        Returns:

        '''
        fields = self.config.get("restrain")
        for  k,v in o.items():
            if k not in fields:
                del o[k]

    def extract(self,l):
        '''
        从数组中抽取字段变为 Obj
        Args:
            a:

        Returns:

        '''
        way=self.config.get("way")
        fields=self.config.get("fields")
        o={}
        if way=="rowsToObject":
            for f in fields:
                if f not in o:
                    o[f]=[]
                for r in l:
                    o[f].append(r.get(f))
        elif way=="rowToObject":
            idx=self.config.get("index",0)
            if len(l or [])>idx:
                o=l[idx]
            else:
                o=None
        return o




    def go(self,data=[]) :
        pass
        if type(data)=="dict":
            if self.type == "restrain":
                self.restrain(data)
            elif self.type == "quoto":
                self.quoto(data)

        elif self.type=="extract":
            data= self.extract(data)
        else:
            for r in data:
                if self.type=="restrain":
                    self.restrain(r)
                elif self.type=="quoto":
                    self.quoto(r)
        return data
class TransformConfig:
    '''
        将数据按 配置的 数组规则进行 转换 
    '''
    def __init__(self,config):
        '''
            config =[oneConfig,]
        Args:
            config:
        '''
        self.config=config or []
    def go(self,data):
        '''
            数据转换 按数组的方式应用规则
        Args:
            data:

        Returns:

        '''
        for r in self.config:
            oneRegulate=TransformRegulate(r.get("type"),r[r.get("type")])
            data=oneRegulate.go(data)
        return data




class TideCellOthers:
    def __init__(self, hook,hookId):
        self.hook=hook
        self.hookId=hookId

    def geTabletOpts(self,tableNm,key,query={}):
        T=TileOut(tableNm,key.get("level"))
        query["key"]=key
        o=T.one(compressObject(query))
        a=[]

        for s in o.keys():
            if type (o.get(s))!=dict  and s not in ["created","changed"]:
                if type (o.get(s)) == int or type (o.get(s)) == float :
                   a.append("%s %s"%(s,"float"))
                else:
                    a.append("%s %s" % (s, s))
        if o.get("carousel"):
            for s in o.get("carousel").keys():
                if type(o.get("carousel").get(s)) != dict:
                    if type(o.get("carousel").get(s)) == int:
                        a.append("carousel.%s %s" % (s, "float"))
                    else:
                        a.append("carousel.%s %s" % (s, s))


        return {
            "sn":key.get("sn"),
            "hook": key.get("hook"),
            "opts":("\n").join(a),
            "colInp": ("\n").join(a),

        }

class JumpParse:
    def __init__(self, hook, fetchKey,layer):
        self.hook=hook
        self.fetchKey=fetchKey
        self.layer=layer

    def parseFetchKey(self, fetchKey):
        key = {}
        for s in ["level", "levelSn", "sn"]:
            key[s] = fetchKey[s]
        if fetchKey.get("cycleLikely") == "extend":
            key["t"] = self.layer.get("fetch").get("key").get("t")
            key["cycle"] = self.layer.get("fetch").get("key").get("cycle")
        else:
            for s in ["t", "cycle"]:
                key[s] = fetchKey[s]
        return key

    def getLog(self):
        key=self.parseFetchKey(self.fetchKey)
        layerLog = LayerLog(self.hook, key)
        return layerLog
    def getData(self):
        log=self.getLog()
        take = log.getTake()
        fetch = {"key": take.get("key")}
        cellLog = CellLog(fetch)
        ret = cellLog.getData()

        return ret

class OverlayParse:
    def __init__(self,  layer,**kwargs):
        self.layer= layer
        self.fetch=layer.get("fetch")

    def go(self):
        one=getTideLog("cell", self.fetch.get("key", {}))
        return one.get("changed")

