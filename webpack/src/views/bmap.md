按区域显示



 ts_code     | str  | TS代码                                |
| symbol      | str  | 股票代码                              |
| name        | str  | 股票名称                              |
| area        | str  | 所在地域                              |
| industry    | str  | 所属行业                              |
| fullname    | str  | 股票全称                              |
| enname      | str  | 英文全称                              |
| market      | str  | 市场类型 （主板/中小板/创业板）       |
| exchange    | str  | 交易所代码                            |
| curr_type   | str  | 交易货币                              |
| list_status | str  | 上市状态： L上市 D退市 P暂停上市      |
| list_date   | str  | 上市日期                              |
| delist_date | str  | 退市日期                              |
| is_hs       | str  | 是否沪深港通标的，N否 H沪股通 S深股通 |




条件可设置

parent

{
    "theme":"",
    "base":"",
    "queries":[
        {
            queries // 
        },
    "business":[
        {
            // 最近7个工作日 涨> ?
            // 最近1个月
            // 指数/股票 涨跌幅度 离散率
            // 指数涨跌 偏差 
            // 行业涨跌偏差
        }
    ]    

    ]
}