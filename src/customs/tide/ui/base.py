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

@path("/tide/base/cell.html")
class TideBaseCell:
    def GET(self, _cid = None, *args, **kwargs):
        return tide_base["base/cell"]()

@wildcard("/tide/base/cell/")
class TideBaseCellCRUD(CRUD):
    def __init__(self):
        self.module = tide_cell


@wildcard("/tide/base/link/")
class TideBaseLinkCRUD(CRUD):

    def __init__(self):
        self.module = tide_link
    def action(self, act, *args, **kwArgs):
          if act == 'aduit':
              return self.aduit(*args, **kwArgs)
          else:
              return CRUD.action(self, act, *args, **kwArgs)

    def aduit(self, record=None, *args, **kwArgs):

            return {}




@wildcard("/tide/base/step/")
class TideBaseStepCRUD(CRUD):
    def __init__(self):
        self.module = tide_step


@wildcard("/tide/base/measure/")
class TideBaseMeasureCRUD(CRUD):
    def __init__(self):
        self.module = tide_measure


@wildcard("/tide/base/plan/")
class TideBasePlanCRUD(CRUD):
    def __init__(self):
        self.module = tide_plan