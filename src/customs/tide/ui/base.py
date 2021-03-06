# -*- coding: UTF-8 -*-
# Module  : py
# Description :
# Author  : Wujj
# Date    : 2020/2/4
# Version : 1.0

from ui import wildcard,CRUD,path

from web.contrib.template import render_mako
tide_base= render_mako(directories=["customs/tide/templates/", "templates"], input_encoding="utf-8",
                       output_encoding="utf-8")
from  customs.tide.service.bean.base  import *

from customs.tide.service.expose.expose import *



@path("/tide/base/cell.html")
class TideBaseCell:
    def GET(self, _cid = None, *args, **kwargs):
        return tide_base["base/cell"]()

@wildcard("/tide/base/cell/")
class TideBaseCellCRUD(CRUD):
    def __init__(self):
        self.module = tide_cell
    def action(self, act, *args, **kwArgs):
          if act == 'doing':
              return self.doing(*args, **kwArgs)
          if act == 'copy':
              return self.copy(*args, **kwArgs)
          else:
              return CRUD.action(self, act, *args, **kwArgs)

          # 将配置复制到 本选中的 link 下

    def copy(self, from_id=None,  toPid=None, **kwArgs):
        if not toPid:
            raise Exception("need toPid")
        record = self.module.get(from_id)
        if record:
            record["pid"]=toPid
            del record["_id"]
        return self.action("insert", record=record)

    def doing(self, record=None, *args, **kwArgs):
        task = TaskRun(record.get("_id"), "cell", None)
        re = task.go()
        return re

@wildcard("/tide/base/link/")
class TideBaseLinkCRUD(CRUD):

    def __init__(self):
        self.module = tide_link
    def action(self, act, *args, **kwArgs):
          if act == 'doing':
              return self.doing(*args, **kwArgs)
          if act == 'copy':
              return self.copy(*args, **kwArgs)
          else:
              return CRUD.action(self, act, *args, **kwArgs)

    def copy(self, record=None, **kwArgs):
        if not record:
            raise Exception("need toPid")
        record = self.module.get(record.get("_id"))
        if record:
            del record["_id"]
        return self.action("insert", record=record)
    def doing(self, record=None, *args, **kwArgs):
        task = TaskRun(record.get("_id"), "link", None)
        re = task.go()
        return re





@wildcard("/tide/base/step/")
class TideBaseStepCRUD(CRUD):
    def __init__(self):
        self.module = tide_step
    def action(self, act, *args, **kwArgs):
          if act == 'doing':
              return self.doing(*args, **kwArgs)
          if act == 'copy':
              return self.copy(*args, **kwArgs)
          else:
              return CRUD.action(self, act, *args, **kwArgs)
    def copy(self, record=None, **kwArgs):
        if not record:
            raise Exception("need toPid")
        record = self.module.get(record.get("_id"))
        if record:
            del record["_id"]
        return self.action("insert", record=record)
    def doing(self, record=None, *args, **kwArgs):
        task = TaskRun(record.get("_id"), "step", None)
        re = task.go()
        return re

@wildcard("/tide/base/measure/")
class TideBaseMeasureCRUD(CRUD):
    def __init__(self):
        self.module = tide_measure
    def action(self, act, *args, **kwArgs):
          if act == 'doing':
              return self.doing(*args, **kwArgs)
          if act == 'copy':
              return self.copy(*args, **kwArgs)
          else:
              return CRUD.action(self, act, *args, **kwArgs)
    def copy(self, record=None, **kwArgs):
        if not record:
            raise Exception("need toPid")
        record = self.module.get(record.get("_id"))
        if record:
            del record["_id"]
        return self.action("insert", record=record)
    def doing(self, record=None, *args, **kwArgs):
        task = TaskRun(record.get("_id"), "measure", None)
        re = task.go()
        return re

@path("/tide/base/plan.html")
class TidebasePlan:
    def GET(self, _cid = None, *args, **kwargs):
        return tide_base["base/plan"]()



@wildcard("/tide/base/plan/")
class TideBasePlanCRUD(CRUD):
    def __init__(self):
        self.module = tide_plan
    def action(self, act, *args, **kwArgs):
          if act == 'doing':
              return self.doing(*args, **kwArgs)
          if act == 'copy':
              return self.copy(*args, **kwArgs)
          else:
              return CRUD.action(self, act, *args, **kwArgs)
    def copy(self, record=None, **kwArgs):
        if not record:
            raise Exception("need toPid")
        record = self.module.get(record.get("_id"))
        if record:
            del record["_id"]
        return self.action("insert", record=record)
    def doing(self, record=None, *args, **kwArgs):
        task = TaskRun(record.get("_id"), "plan", None)
        re = task.go()
        return re



@path("/tide/base/chains.html")
class TideBaseChains:
    def GET(self, _cid = None, *args, **kwargs):
        return tide_base["base/chains"]()


@wildcard("/tide/base/chains/")
class TideBaseChainsCRUD(CRUD):
    def __init__(self):
        self.module = tide_chains_log
        def action(self, act, *args, **kwArgs):
          if act == 'redo':
              return self.redo(*args, **kwArgs)
          else:
              return CRUD.action(self, act, *args, **kwArgs)

    def redo(self, record=None, *args, **kwArgs):
        task=TaskRun(record.get("topHookId"),record.get("topHook"),record.get("_id"))
        re=task.go()
        return re
