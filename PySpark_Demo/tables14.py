#使用PySpark完成航线飞行时间散点图数据分析
from pyspark.sql.types import StringType, StructField, IntegerType, DoubleType, StructType
from pyspark.sql.functions import col
from pyspark.sql import SparkSession

# 数据库连接配置
mysql_url = "jdbc:mysql://bigdata:3306/Flink_Fliggy_Flight"
prop = {'user': 'root', 'password': '123456', 'driver': "com.mysql.jdbc.Driver"}

# 1.创建SparkSession
spark = SparkSession.builder.appName("tables14_task").getOrCreate()

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

# 4.航线飞行时间散点图数据
flight_time_scatter_sql = '''
    SELECT 
        start_city,
        end_city,
        flight_total_time_math as flight_time,
        price,
        flight_company,
        COUNT(*) as frequency
    FROM ods_flight
    WHERE flight_total_time_math > 0 
    AND price > 0
    GROUP BY start_city, end_city, flight_total_time_math, price, flight_company
    ORDER BY frequency DESC
'''

# 5.执行SQL并保存结果
spark.sql(flight_time_scatter_sql).write.jdbc(mysql_url, 'tables14', 'overwrite', prop)

# 显示部分结果用于调试
print("航线飞行时间散点图数据示例：")
spark.sql(flight_time_scatter_sql).show(5)