# -*- coding: UTF-8 -*-
# Module  : py
# Description :基本接口
# Author  : Wujj
# Date    : 2017-11-5
# Version : 1.0



import ctx
from service import comm
stock_basics = comm.CRUD(ctx.cmdb, "stock_basics", [("cid", 1)])




import tushare as ts


def get_stock_basics():
    print 1
    l=ts.get_stock_basics()
    print 2