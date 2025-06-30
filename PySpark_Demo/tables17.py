# tables17.py - 机场航线网络关系分析
from pyspark.sql.types import StringType, StructField, IntegerType, DoubleType, StructType
from pyspark.sql.functions import col, count, avg
from pyspark.sql import SparkSession

# 数据库连接配置
mysql_url = "jdbc:mysql://bigdata:3306/Flink_Fliggy_Flight"
prop = {'user': 'root', 'password': '123456', 'driver': "com.mysql.jdbc.Driver"}

# 创建SparkSession
spark = SparkSession.builder.appName("tables17_task").getOrCreate()

# 定义数据schema
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

# 读取CSV数据
flights_data = spark.read.option("header", "false").schema(schema).csv("hdfs://bigdata:9000/flink_fliggy_flight/flight/hdfs_flights.csv")
flights_data.createOrReplaceTempView("ods_flight")

# 计算机场航线网络数据
airport_network_sql = """
    SELECT 
        start_airport as source,
        arr_airport as target,
        COUNT(*) as flight_count,
        COUNT(DISTINCT flight_company) as airline_count,
        ROUND(AVG(price), 2) as avg_price,
        ROUND(AVG(ontime_rate), 2) as avg_ontime_rate,
        ROUND(AVG(flight_total_time_math), 2) as avg_flight_time
    FROM ods_flight
    GROUP BY start_airport, arr_airport
    HAVING flight_count >= 10
    ORDER BY flight_count DESC
"""

# 执行SQL并保存结果
spark.sql(airport_network_sql).write.jdbc(mysql_url, 'tables17', 'overwrite', prop)