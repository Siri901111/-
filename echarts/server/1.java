package cn.itcast

import org.apache.spark.sql.{SparkSession, functions => F}
import org.apache.spark.sql.expressions.Window

object MovieDataAnalysis {
  // 常量定义
  private val HDFS_DATA_PATH = "hdfs://192.168.220.201:8020/data/input/u.data"
  private val MIN_RATINGS_THRESHOLD = 200
  private val TOP_N_MOVIES = 10

  def main(args: Array[String]): Unit = {
    // 创建SparkSession
    val spark = SparkSession.builder()
      .appName("MovieDataAnalysis")
      .master("local[*]")
      .config("spark.sql.shuffle.partitions", "4")
      .getOrCreate()

    try {
      // 设置日志级别
      spark.sparkContext.setLogLevel("WARN")
      
      // 执行数据分析流程
      runAnalysis(spark)
      
    } finally {
      // 确保SparkSession正确关闭
      spark.stop()
    }
  }

  /**
   * 执行电影数据分析流程
   */
  private def runAnalysis(spark: SparkSession): Unit = {
    import spark.implicits._
    
    // 加载并解析数据
    val movieRatingsDF = loadAndParseData(spark)
    
    // 展示数据样例
    showDataSample(movieRatingsDF)
    
    // SQL方式分析
    val sqlResult = analyzeBySQL(movieRatingsDF)
    println("\n===== SQL查询结果 (Top10电影) =====")
    sqlResult.show()
    
    // DSL方式分析
    val dslResult = analyzeByDSL(movieRatingsDF)
    println("\n===== DSL查询结果 (Top10电影) =====")
    dslResult.show()
  }

  /**
   * 加载并解析电影评分数据
   */
  private def loadAndParseData(spark: SparkSession): org.apache.spark.sql.DataFrame = {
    spark.read.textFile(HDFS_DATA_PATH)
      .map(line => {
        val fields = line.split("\t")
        (fields(1), fields(2).toInt)  // (movieId, rating)
      })
      .toDF("movieId", "rating")
  }

  /**
   * 展示数据样例和结构
   */
  private def showDataSample(df: org.apache.spark.sql.DataFrame): Unit = {
    println("===== 原始数据样例 =====")
    df.show(5, truncate = false)
    df.printSchema()
  }

  /**
   * 使用SQL方式分析电影评分数据
   */
  private def analyzeBySQL(df: org.apache.spark.sql.DataFrame): org.apache.spark.sql.DataFrame = {
    df.createOrReplaceTempView("ratings")
    
    val sqlQuery =
      s"""
      SELECT movieId,
             COUNT(*) AS total_ratings,
             ROUND(AVG(rating), 2) AS avg_rating
      FROM ratings
      GROUP BY movieId
      HAVING total_ratings > $MIN_RATINGS_THRESHOLD
      ORDER BY avg_rating DESC
      LIMIT $TOP_N_MOVIES
      """
    
    df.sparkSession.sql(sqlQuery)
  }

  /**
   * 使用DSL方式分析电影评分数据
   */
  private def analyzeByDSL(df: org.apache.spark.sql.DataFrame): org.apache.spark.sql.DataFrame = {
    import df.sparkSession.implicits._
    
    df.groupBy("movieId")
      .agg(
        F.count("rating").alias("total_ratings"),
        F.avg("rating").alias("avg_rating")
      )
      .filter($"total_ratings" > MIN_RATINGS_THRESHOLD)
      .orderBy(F.desc("avg_rating"))
      .limit(TOP_N_MOVIES)
      .select($"movieId", $"total_ratings", F.round($"avg_rating", 2).alias("avg_rating"))
  }
}  