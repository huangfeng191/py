# -*- coding: UTF-8 -*-
# Module  : py
# Description :获取数据
# Author  : Wujj
# Date    : 2017-11-4
# Version : 1.0


from ui import path, CRUD, wildcard
from web.contrib.template import render_mako
from customs.stock.service import *
import customs.stock.service.tushare_api  as tushare_api
render_stock = render_mako(directories=["customs/stock/templates", "templates"], input_encoding="utf-8",
                       output_encoding="utf-8")




@path("/stock/admin.html")
class StockAdmin:
    def GET(self, _cid=None, *args, **kwargs):
        return render_stock["admin"]()


@wildcard("/stock/admin/")
class StockAdminCRUD(CRUD):
    def __init__(self):
        self.module = tushare_api.stock_admin_save
    def action(self, act, *args, **kwArgs):
        if act == 'basics':
            return self.basics(*args, **kwArgs)
        if act == 'getInfo':
            return self.getInfo(*args, **kwArgs)
        else:
            return CRUD.action(self, act, *args, **kwArgs)
    def getInfo(self, table_nm=None, *args, **kwArgs):
        tushare_api.getInfo(table_nm)
        print 1
        return "OK"
    def basics(self, record=None, *args, **kwArgs):
        tushare_api.get_stock_basics()
        print 1
        return "OK"
