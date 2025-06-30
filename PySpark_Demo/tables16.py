# 机场繁忙度时钟分析
from pyspark.sql.types import StringType, StructField, IntegerType, DoubleType, StructType
from pyspark.sql.functions import col, hour, count
from pyspark.sql import SparkSession

# 数据库连接配置
mysql_url = "jdbc:mysql://bigdata:3306/Flink_Fliggy_Flight"
prop = {'user': 'root', 'password': '123456', 'driver': "com.mysql.jdbc.Driver"}

# 创建SparkSession
spark = SparkSession.builder.appName("tables16_task").getOrCreate()

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

# 计算机场繁忙度时钟数据
busy_hours_sql = """
    SELECT 
        start_airport as airport,
        HOUR(setup_time) as hour,
        COUNT(*) as flight_count,
        AVG(ontime_rate) as avg_ontime_rate
    FROM ods_flight
    GROUP BY start_airport, HOUR(setup_time)
    ORDER BY start_airport, hour
"""

# 执行SQL并保存结果
spark.sql(busy_hours_sql).write.jdbc(mysql_url, 'tables16', 'overwrite', prop)