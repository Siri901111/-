#使用PySpark完成航线热度分析
from pyspark.sql.types import StringType, StructField, IntegerType, DoubleType, StructType
from pyspark.sql.functions import col
from pyspark.sql import SparkSession

# 数据库连接配置
mysql_url = "jdbc:mysql://bigdata:3306/Flink_Fliggy_Flight"
prop = {'user': 'root', 'password': '123456', 'driver': "com.mysql.jdbc.Driver"}

# 1.创建SparkSession
spark = SparkSession.builder.appName("tables13_task").getOrCreate()

# 2.定义数据schema
fields = [
    StructField("start_city", StringType(), True),
    StructField("end_city", StringType(), True),
    StructField("stime", StringType(), True),
    StructField("airline_name", StringType(), True),
    StructField("flight_info", StringType(), True),
    StructField("flight_type1", StringType(), True),
    StructField("flight_type2", StringType(), True),
    StructField("setup_time", StringType(), True),
    StructField("arr_time", StringType(), True),
    StructField("start_airport", StringType(), True),
    StructField("arr_airport", StringType(), True),
    StructField("ontime_rate", IntegerType(), True),
    StructField("flight_total_time", StringType(), True),
    StructField("price", IntegerType(), True),
    StructField("price_desc", StringType(), True),
    StructField("flight_company", StringType(), True),
    StructField("flight_type3", StringType(), True),
    StructField("setup_time_math", DoubleType(), True),
    StructField("arr_time_math", DoubleType(), True),
    StructField("arr_time2", StringType(), True),
    StructField("start_airport_simple", StringType(), True),
    StructField("arr_airport_simple", StringType(), True),
    StructField("flight_total_time_math", IntegerType(), True),
    StructField("price_desc_math", DoubleType(), True),
]
schema = StructType(fields)

# 3.读取CSV数据
flights_data = spark.read.option("header", "false").schema(schema).csv("hdfs://bigdata:9000/flink_fliggy_flight/flight/hdfs_flights.csv")
flights_data.createOrReplaceTempView("ods_flight")

# 4.热门航线地图数据统计
hot_routes_sql = '''
    SELECT 
        start_city,
        end_city,
        COUNT(*) as flight_count,
        ROUND(AVG(price), 2) as avg_price,
        ROUND(AVG(ontime_rate), 2) as avg_ontime_rate
    FROM ods_flight
    GROUP BY start_city, end_city
    ORDER BY flight_count DESC
    LIMIT 50
'''

# 5.执行SQL并保存结果
spark.sql(hot_routes_sql).write.jdbc(mysql_url, 'tables13', 'overwrite', prop)

# 显示部分结果用于调试
print("热门航线数据示例：")
spark.sql(hot_routes_sql).show(5)