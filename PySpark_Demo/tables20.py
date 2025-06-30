# 机场吞吐量与延误率关系分析
from pyspark.sql.types import StringType, StructField, IntegerType, DoubleType, StructType
from pyspark.sql.functions import col, count
from pyspark.sql import SparkSession

# 数据库连接配置
mysql_url = "jdbc:mysql://bigdata:3306/Flink_Fliggy_Flight"
prop = {'user': 'root', 'password': '123456', 'driver': "com.mysql.jdbc.Driver"}

# 创建SparkSession
spark = SparkSession.builder.appName("tables20_task").getOrCreate()

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

# 计算机场吞吐量与延误关系
airport_delay_sql = """
    WITH airport_stats AS (
        SELECT 
            start_airport as airport,
            COUNT(*) as total_flights,
            COUNT(CASE WHEN ontime_rate < 80 THEN 1 END) as delayed_flights,
            ROUND(AVG(CASE WHEN ontime_rate < 80 THEN flight_total_time_math END), 2) as avg_delay_time,
            ROUND(AVG(ontime_rate), 2) as avg_ontime_rate
        FROM ods_flight
        GROUP BY start_airport
    )
    SELECT 
        airport,
        total_flights,
        delayed_flights,
        avg_delay_time,
        avg_ontime_rate
    FROM airport_stats
    ORDER BY total_flights DESC
"""

# 执行SQL并保存结果
spark.sql(airport_delay_sql).write.jdbc(mysql_url, 'tables20', 'overwrite', prop)