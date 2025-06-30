#使用PySpark完成每日航班量分析
from pyspark.sql.types import StringType, StructField, IntegerType, DoubleType, StructType
from pyspark.sql.functions import col
from pyspark.sql import SparkSession

csv_format = 'com.databricks.spark.csv'
mysql_url = "jdbc:mysql://bigdata:3306/Flink_Fliggy_Flight"
prop = {'user': 'root', 'password': '123456', 'driver': "com.mysql.jdbc.Driver"}

# 1.创建SparkSession
spark = SparkSession.builder.appName("tables09_task").getOrCreate()

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

# 2.读取本地文件路径
flights_data = spark.read.option("header", "false").schema(schema).csv("hdfs://bigdata:9000/flink_fliggy_flight/flight/hdfs_flights.csv")

# 3.创建临时表
flights_data.createOrReplaceTempView("ods_flight")

# 4.每日航班量分析
tables09_sql = '''
    SELECT 
        stime,
        COUNT(1) as total_flights,
        COUNT(DISTINCT flight_company) as airline_companies,
        COUNT(DISTINCT CONCAT(start_city, '-', end_city)) as routes,
        AVG(price) as avg_price
    FROM ods_flight
    GROUP BY stime
    ORDER BY stime
'''

# 执行SQL并显示结果
spark.sql(tables09_sql).show()

# 将结果写入MySQL
spark.sql(tables09_sql).write.jdbc(mysql_url, 'tables09', 'overwrite', prop) 