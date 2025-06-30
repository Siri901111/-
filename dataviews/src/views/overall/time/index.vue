<template>
  <div class="time-analysis">
    <el-row :gutter="20">
      <!-- 24小时航班分布 -->
      <el-col :span="24">
        <el-card class="chart-card">
          <div ref="hourlyChart" class="chart"></div>
        </el-card>
      </el-col>
      
      <!-- 准点率趋势分析 -->
      <el-col :span="24" class="mt-20">
        <el-card class="chart-card">
          <div ref="ontimeChart" class="chart"></div>
        </el-card>
      </el-col>
      
      <!-- 每日航班量分析 -->
      <el-col :span="24" class="mt-20">
        <el-card class="chart-card">
          <div ref="dailyChart" class="chart"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const hourlyChart = ref(null)
const ontimeChart = ref(null)
const dailyChart = ref(null)
let charts = []

// 初始化24小时航班分布图表
const initHourlyChart = async () => {
  const chart = echarts.init(hourlyChart.value)
  charts.push(chart)
  
  try {
    const { data } = await axios.get('http://localhost:8080/tables07')
    const option = {
      title: {
        text: '24小时航班分布',
        textStyle: {
          color: '#fff',
          fontSize: 16
        }
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross'
        }
      },
      legend: {
        data: ['航班数量', '平均准点率', '平均票价'],
        textStyle: { color: '#fff' },
        top: 25
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        boundaryGap: true,
        data: data.map(item => `${item.hour_period}:00`),
        axisLabel: {
          color: '#fff',
          formatter: '{value}时'
        }
      },
      yAxis: [
        {
          type: 'value',
          name: '航班数量',
          position: 'left',
          axisLabel: {
            color: '#fff',
            formatter: '{value}'
          }
        },
        {
          type: 'value',
          name: '准点率/票价',
          position: 'right',
          axisLabel: {
            color: '#fff',
            formatter: '{value}'
          }
        }
      ],
      series: [
        {
          name: '航班数量',
          type: 'bar',
          data: data.map(item => item.flight_count),
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#83bff6' },
              { offset: 0.5, color: '#188df0' },
              { offset: 1, color: '#188df0' }
            ])
          }
        },
        {
          name: '平均准点率',
          type: 'line',
          yAxisIndex: 1,
          data: data.map(item => item.avg_ontime_rate),
          lineStyle: { color: '#91cc75' },
          itemStyle: { color: '#91cc75' }
        },
        {
          name: '平均票价',
          type: 'line',
          yAxisIndex: 1,
          data: data.map(item => item.avg_price),
          lineStyle: { color: '#fac858' },
          itemStyle: { color: '#fac858' }
        }
      ]
    }
    chart.setOption(option)
  } catch (error) {
    ElMessage.error('获取24小时航班分布数据失败')
    console.error(error)
  }
}

// 初始化准点率趋势图表
const initOntimeChart = async () => {
  const chart = echarts.init(ontimeChart.value)
  charts.push(chart)
  
  try {
    const { data } = await axios.get('http://localhost:8080/tables08')
    const option = {
      title: {
        text: '准点率趋势分析',
        textStyle: {
          color: '#fff',
          fontSize: 16
        }
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      legend: {
        data: ['总航班量', '高准点率', '中准点率', '低准点率', '平均准点率'],
        textStyle: { color: '#fff' },
        top: 25
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: data.map(item => item.stime),
        axisLabel: {
          color: '#fff',
          rotate: 45
        }
      },
      yAxis: [
        {
          type: 'value',
          name: '航班数量',
          position: 'left',
          axisLabel: { color: '#fff' }
        },
        {
          type: 'value',
          name: '准点率(%)',
          position: 'right',
          axisLabel: { color: '#fff' }
        }
      ],
      series: [
        {
          name: '总航班量',
          type: 'bar',
          data: data.map(item => item.total_flights),
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#83bff6' },
              { offset: 0.5, color: '#188df0' },
              { offset: 1, color: '#188df0' }
            ])
          }
        },
        {
          name: '高准点率',
          type: 'bar',
          stack: 'ontime',
          data: data.map(item => item.high_ontime_flights),
          itemStyle: { color: '#91cc75' }
        },
        {
          name: '中准点率',
          type: 'bar',
          stack: 'ontime',
          data: data.map(item => item.mid_ontime_flights),
          itemStyle: { color: '#fac858' }
        },
        {
          name: '低准点率',
          type: 'bar',
          stack: 'ontime',
          data: data.map(item => item.low_ontime_flights),
          itemStyle: { color: '#ee6666' }
        },
        {
          name: '平均准点率',
          type: 'line',
          yAxisIndex: 1,
          data: data.map(item => item.avg_ontime_rate),
          lineStyle: { color: '#73c0de' },
          itemStyle: { color: '#73c0de' }
        }
      ]
    }
    chart.setOption(option)
  } catch (error) {
    ElMessage.error('获取准点率趋势数据失败')
    console.error(error)
  }
}

// 初始化每日航班量分析图表
const initDailyChart = async () => {
  const chart = echarts.init(dailyChart.value)
  charts.push(chart)
  
  try {
    const { data } = await axios.get('http://localhost:8080/tables09')
    const option = {
      title: {
        text: '每日航班量分析',
        textStyle: {
          color: '#fff',
          fontSize: 16
        }
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross'
        }
      },
      legend: {
        data: ['总航班量', '航司数量', '航线数量', '平均票价'],
        textStyle: { color: '#fff' },
        top: 25
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: data.map(item => item.stime),
        axisLabel: {
          color: '#fff',
          rotate: 45
        }
      },
      yAxis: [
        {
          type: 'value',
          name: '数量',
          position: 'left',
          axisLabel: { color: '#fff' }
        },
        {
          type: 'value',
          name: '票价(元)',
          position: 'right',
          axisLabel: { color: '#fff' }
        }
      ],
      series: [
        {
          name: '总航班量',
          type: 'bar',
          data: data.map(item => item.total_flights),
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#83bff6' },
              { offset: 0.5, color: '#188df0' },
              { offset: 1, color: '#188df0' }
            ])
          }
        },
        {
          name: '航司数量',
          type: 'line',
          data: data.map(item => item.airline_companies),
          lineStyle: { color: '#91cc75' },
          itemStyle: { color: '#91cc75' }
        },
        {
          name: '航线数量',
          type: 'line',
          data: data.map(item => item.routes),
          lineStyle: { color: '#fac858' },
          itemStyle: { color: '#fac858' }
        },
        {
          name: '平均票价',
          type: 'line',
          yAxisIndex: 1,
          data: data.map(item => item.avg_price),
          lineStyle: { color: '#ee6666' },
          itemStyle: { color: '#ee6666' }
        }
      ]
    }
    chart.setOption(option)
  } catch (error) {
    ElMessage.error('获取每日航班量数据失败')
    console.error(error)
  }
}

// 监听窗口大小变化
const handleResize = () => {
  charts.forEach(chart => chart && chart.resize())
}

// 生命周期钩子
onMounted(() => {
  initHourlyChart()
  initOntimeChart()
  initDailyChart()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  charts.forEach(chart => chart && chart.dispose())
  charts = []
})
</script>

<style scoped>
.time-analysis {
  padding: 20px;
  height: 100%;
  background: transparent;  /* 改为透明背景 */
}

.chart-card {
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  border: none;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #fff;
}

.chart {
  height: 400px;
  width: 100%;
}

.mt-20 {
  margin-top: 20px;
}

:deep(.el-card__header) {
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}
</style> 