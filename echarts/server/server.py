from flask import Flask, request
import json
import pymysql
from flask_mysqldb import MySQL
import io, sys
from flask_cors import CORS
# 创建应用对象
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'         # 正确主机名
app.config['MYSQL_PORT'] = 3306                # 端口号
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '102626cn'
app.config['MYSQL_DB'] = 'Flink_Fliggy_Flight'
CORS(app)
mysql = MySQL(app)  # this is the instantiation
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

@app.route('/tables01')
def tables01():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM tables01 order by price_desc_math asc ''')
    row_headers = [x[0] for x in cur.description]  # this will extract row headers
    rv = cur.fetchall()
    json_data = []
    print(json_data)
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data, ensure_ascii=False)


@app.route('/tables05')
def tables05():
    cur = mysql.connection.cursor()
    cur.execute('''select * from tables05 limit 5''')
    #cur.execute('''SELECT * FROM tables05 ''')
    row_headers = [x[0] for x in cur.description]  # this will extract row headers
    rv = cur.fetchall()
    json_data = []
    print(json_data)
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data, ensure_ascii=False)

@app.route('/tables06')
def tables06():
    cur = mysql.connection.cursor()
    cur.execute('''select * from tables06 order by  price desc limit 10''')
    #cur.execute('''SELECT * FROM tables05 ''')
    row_headers = [x[0] for x in cur.description]  # this will extract row headers
    rv = cur.fetchall()
    json_data = []
    print(json_data)
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data, ensure_ascii=False)


@app.route('/tables03')
def tables03():
    cur = mysql.connection.cursor()
    cur.execute('''select * from tables03 ''')
    row_headers = [x[0] for x in cur.description]  # this will extract row headers
    rv = cur.fetchall()
    json_data = []
    print(json_data)
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data, ensure_ascii=False)


@app.route('/tables02')
def tables02():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM tables02''')
    row_headers = [x[0] for x in cur.description]  # this will extract row headers
    rv = cur.fetchall()
    json_data = []
    print(json_data)
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data, ensure_ascii=False)


@app.route('/tables04')
def tables04():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM tables04 order by stime asc''')
    #row_headers = [x[1] for x in cur.description]  # this will extract row headers
    row_headers = ['stime', 'num']
    rv = cur.fetchall()
    json_data = []
    print(json_data)
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data, ensure_ascii=False)

# - 24小时航班分布统计接口
@app.route('/tables07')
def tables07():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT 
            hour_period,
            flight_count,
            ROUND(avg_ontime_rate, 2) as avg_ontime_rate,
            ROUND(avg_price, 2) as avg_price
        FROM tables07 
        ORDER BY hour_period''')
    row_headers = [x[0] for x in cur.description]
    rv = cur.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data, ensure_ascii=False)

@app.route('/tables08')
def tables08():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT 
            stime,
            total_flights,
            ROUND(avg_ontime_rate, 2) as avg_ontime_rate,
            high_ontime_flights,
            mid_ontime_flights,
            low_ontime_flights
        FROM tables08 
        ORDER BY stime''')
    row_headers = [x[0] for x in cur.description]
    rv = cur.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data, ensure_ascii=False)

# tables09 - 每日航班量分析接口
@app.route('/tables09')
def tables09():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT 
            stime,
            total_flights,
            airline_companies,
            routes,
            ROUND(avg_price, 2) as avg_price
        FROM tables09 
        ORDER BY stime''')
    row_headers = [x[0] for x in cur.description]
    rv = cur.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data, ensure_ascii=False)

# 机型分析接口
@app.route('/tables10')
def tables10():
    """
    机型总体分析接口
    返回数据格式：
    {
        "aircraft_type": "机型名称",
        "route_count": "航线覆盖数量",
        "city_coverage": "城市覆盖数量",
        "avg_price": "平均票价",
        "avg_ontime_rate": "平均准点率",
        "flight_count": "航班数量",
        "avg_flight_time": "平均飞行时间"
    }
    """
    cur = mysql.connection.cursor()
    cur.execute('''SELECT 
            aircraft_type,
            route_count,
            city_coverage,
            ROUND(avg_price, 2) as avg_price,
            ROUND(avg_ontime_rate, 2) as avg_ontime_rate,
            flight_count,
            avg_flight_time
        FROM tables10 
        ORDER BY flight_count DESC''')
    row_headers = [x[0] for x in cur.description]
    rv = cur.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data, ensure_ascii=False)

# 机型地理分布接口
@app.route('/tables11')
def tables11():
    """
    机型地理分布分析接口
    返回数据格式：
    {
        "aircraft_type": "机型名称",
        "city": "城市名称",
        "flight_count": "航班数量",
        "avg_price": "平均票价",
        "dest_city_count": "目的地城市数量"
    }
    """
    cur = mysql.connection.cursor()
    cur.execute('''SELECT 
            aircraft_type,
            city,
            flight_count,
            ROUND(avg_price, 2) as avg_price,
            dest_city_count
        FROM tables11 
        ORDER BY aircraft_type, flight_count DESC''')
    row_headers = [x[0] for x in cur.description]
    rv = cur.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data, ensure_ascii=False)

# 机型价格分析接口
@app.route('/tables12')
def tables12():
    """
    机型价格分析接口
    返回数据格式：
    {
        "aircraft_type": "机型名称",
        "avg_price": "平均票价",
        "min_price": "最低票价",
        "max_price": "最高票价",
        "avg_flight_time": "平均飞行时间",
        "sample_count": "样本数量"
    }
    """
    cur = mysql.connection.cursor()
    cur.execute('''SELECT 
            aircraft_type,
            avg_price,
            min_price,
            max_price,
            avg_flight_time,
            sample_count
        FROM tables12 
        ORDER BY avg_price DESC''')
    row_headers = [x[0] for x in cur.description]
    rv = cur.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data, ensure_ascii=False)

# 热门航线数据接口
@app.route('/tables13')
def tables13():
    """
    获取热门航线数据
    返回格式：[{
        "start_city": "出发城市",
        "end_city": "到达城市",
        "flight_count": "航班数量",
        "avg_price": "平均票价",
        "avg_ontime_rate": "平均准点率"
    }]
    """
    cur = mysql.connection.cursor()
    cur.execute('''SELECT 
            start_city,
            end_city,
            flight_count,
            ROUND(avg_price, 2) as avg_price,
            ROUND(avg_ontime_rate, 2) as avg_ontime_rate
        FROM tables13 
        ORDER BY flight_count DESC''')
    row_headers = [x[0] for x in cur.description]
    rv = cur.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data, ensure_ascii=False)

# 航线飞行时间散点图数据接口
@app.route('/tables14')
def tables14():
    """
    获取航线飞行时间散点图数据
    返回格式：[{
        "start_city": "出发城市",
        "end_city": "到达城市",
        "flight_time": "飞行时间(分钟)",
        "price": "票价",
        "flight_company": "航空公司",
        "frequency": "航班频次"
    }]
    """
    cur = mysql.connection.cursor()
    cur.execute('''SELECT 
            start_city,
            end_city,
            flight_time,
            price,
            flight_company,
            frequency
        FROM tables14 
        ORDER BY frequency DESC''')
    row_headers = [x[0] for x in cur.description]
    rv = cur.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data, ensure_ascii=False)

# 航线网络关系图数据接口
@app.route('/tables15')
def tables15():
    """
    获取航线网络关系图数据
    返回格式：[{
        "source": "出发城市",
        "target": "到达城市",
        "value": "航班数量",
        "avg_price": "平均票价",
        "airline_count": "航空公司数量"
    }]
    """
    cur = mysql.connection.cursor()
    cur.execute('''SELECT 
            source,
            target,
            value,
            ROUND(avg_price, 2) as avg_price,
            airline_count
        FROM tables15 
        ORDER BY value DESC''')
    row_headers = [x[0] for x in cur.description]
    rv = cur.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data, ensure_ascii=False)


# 机场繁忙度时钟图数据接口
@app.route('/tables16')
def tables16():
    """
    获取机场繁忙度时钟数据
    返回格式：[{
        "airport": "机场名称",
        "hour": "小时(0-23)",
        "flight_count": "航班数量",
        "avg_ontime_rate": "平均准点率"
    }]
    """
    cur = mysql.connection.cursor()
    cur.execute('''SELECT 
            airport,
            hour,
            flight_count,
            ROUND(avg_ontime_rate, 2) as avg_ontime_rate
        FROM tables16 
        ORDER BY airport, hour''')
    row_headers = [x[0] for x in cur.description]
    rv = cur.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data, ensure_ascii=False)

# 机场航线网络关系图数据接口
@app.route('/tables17')
def tables17():
    """
    获取机场航线网络关系数据
    返回格式：[{
        "source": "起始机场",
        "target": "目的机场",
        "flight_count": "航班数量",
        "airline_count": "航空公司数量",
        "avg_price": "平均票价",
        "avg_ontime_rate": "平均准点率",
        "avg_flight_time": "平均飞行时间"
    }]
    """
    cur = mysql.connection.cursor()
    cur.execute('''SELECT 
            source,
            target,
            flight_count,
            airline_count,
            avg_price,
            avg_ontime_rate,
            avg_flight_time
        FROM tables17 
        ORDER BY flight_count DESC''')
    row_headers = [x[0] for x in cur.description]
    rv = cur.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data, ensure_ascii=False)

# 机场吞吐量排名数据接口
@app.route('/tables18')
def tables18():
    """
    获取机场吞吐量排名数据
    返回格式：[{
        "airport": "机场名称",
        "total_flights": "总航班数",
        "avg_dest_count": "平均目的地数",
        "avg_airline_count": "平均航司数",
        "avg_price": "平均票价",
        "avg_ontime_rate": "平均准点率"
    }]
    """
    cur = mysql.connection.cursor()
    cur.execute('''SELECT 
            airport,
            total_flights,
            avg_dest_count,
            avg_airline_count,
            avg_price,
            avg_ontime_rate
        FROM tables18 
        ORDER BY total_flights DESC''')
    row_headers = [x[0] for x in cur.description]
    rv = cur.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data, ensure_ascii=False)



# 航班延误原因分类统计接口
@app.route('/tables19')
def tables19():
    """
    获取航班延误原因分类统计数据
    返回格式：[{
        "delay_reason": "延误原因",
        "delay_count": "延误航班数",
        "avg_delay_time": "平均延误时间",
        "avg_ontime_rate": "平均准点率"
    }]
    """
    cur = mysql.connection.cursor()
    cur.execute('''SELECT 
            delay_reason,
            delay_count,
            ROUND(avg_delay_time, 2) as avg_delay_time,
            ROUND(avg_ontime_rate, 2) as avg_ontime_rate
        FROM tables19 
        ORDER BY delay_count DESC''')
    row_headers = [x[0] for x in cur.description]
    rv = cur.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data, ensure_ascii=False)

# 机场吞吐量与延误率关系接口
@app.route('/tables20')
def tables20():
    """
    获取机场吞吐量与延误率关系数据
    返回格式：[{
        "airport": "机场名称",
        "total_flights": "总航班数",
        "delayed_flights": "延误航班数",
        "avg_delay_time": "平均延误时间",
        "avg_ontime_rate": "平均准点率"
    }]
    """
    cur = mysql.connection.cursor()
    cur.execute('''SELECT 
            airport,
            total_flights,
            delayed_flights,
            ROUND(avg_delay_time, 2) as avg_delay_time,
            ROUND(avg_ontime_rate, 2) as avg_ontime_rate
        FROM tables20 
        ORDER BY total_flights DESC''')
    row_headers = [x[0] for x in cur.description]
    rv = cur.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data, ensure_ascii=False)

# 航线拥堵程度评估接口
@app.route('/tables21')
def tables21():
    """
    获取航线拥堵程度评估数据
    返回格式：[{
        "start_city": "出发城市",
        "end_city": "到达城市",
        "flight_count": "航班数量",
        "congested_flights": "拥堵航班数",
        "avg_flight_time": "平均飞行时间",
        "avg_ontime_rate": "平均准点率"
    }]
    """
    cur = mysql.connection.cursor()
    cur.execute('''SELECT 
            start_city,
            end_city,
            flight_count,
            congested_flights,
            ROUND(avg_flight_time, 2) as avg_flight_time,
            ROUND(avg_ontime_rate, 2) as avg_ontime_rate
        FROM tables21 
        ORDER BY congested_flights DESC''')
    row_headers = [x[0] for x in cur.description]
    rv = cur.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data, ensure_ascii=False)

    
if __name__ == "__main__":
    # print('Server running at: http://localhost:8080/static/html/index.html')
    app.run(host="0.0.0.0", port=8080, debug=True)
