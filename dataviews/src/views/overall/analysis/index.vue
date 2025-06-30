<template>
  <div class="analysis-container">
    <div class="chart-grid">
      <!-- 航空公司实力分析 -->
      <div class="chart-card glass-effect">
        <div class="card-header">
          <h3>航空公司实力分析</h3>
          <div class="header-right">
            <el-tag type="success" effect="dark">实时数据</el-tag>
          </div>
        </div>
        <div ref="airlineStrengthRef" style="width: 100%; height: calc(100% - 60px);"></div>
      </div>

      <!-- 机票价格分析 -->
      <div class="chart-card glass-effect">
        <div class="card-header">
          <h3>机票价格分析</h3>
          <div class="header-right">
            <el-tag type="warning" effect="dark">实时更新</el-tag>
          </div>
        </div>
        <div ref="ticketPriceRef" style="width: 100%; height: calc(100% - 60px);"></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.analysis-container {
  width: 100%;
  height: 100vh;
  padding: 10px;
  box-sizing: border-box;
  background-color: #1a1a1a;
  overflow: hidden;
}

.chart-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  width: 100%;
  height: 100%;
}

.chart-card {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 400px;
  border-radius: 15px;
  padding: 20px;
  box-sizing: border-box;
}

.glass-effect {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 0 10px;
}

.card-header h3 {
  color: #fff;
  font-size: 20px;
  margin: 0;
}

:deep(.el-tag--success) {
  background: linear-gradient(90deg, #1b5e20 0%, #2e7d32 100%);
  border: none;
}

:deep(.el-tag--warning) {
  background: linear-gradient(90deg, #e65100 0%, #ef6c00 100%);
  border: none;
}
</style>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import * as echarts from 'echarts'
import axios from 'axios'

const airlineStrengthRef = ref(null)
const ticketPriceRef = ref(null)

let airlineStrengthChart = null
let ticketPriceChart = null
let resizeObserver = null
let updateTimer = null

const baseURL = 'http://127.0.0.1:8080'

// 初始化图表函数
const initChart = (chartRef, chartInstance) => {
  if (chartInstance) {
    chartInstance.dispose()
  }
  if (chartRef.value) {
    return echarts.init(chartRef.value)
  }
  return null
}

// 航空公司实力分析图表
const initAirlineStrengthChart = async () => {
  airlineStrengthChart = initChart(airlineStrengthRef, airlineStrengthChart)
  if (!airlineStrengthChart) return
  
  try {
    const response = await axios.get(`${baseURL}/tables05`)
    console.log('航空公司实力数据:', response.data)
    const data = response.data
    
    const option = {
      backgroundColor: 'transparent',
      tooltip: {
        trigger: 'axis',
        formatter: "公司: {b}<br/>飞机架数: {c}",
        textStyle: {
          fontSize: 14
        }
      },
      grid: {
        top: '5%',
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: data.map(item => item.flight_company),
        axisLabel: {
          color: 'rgba(255,255,255,0.7)',
          rotate: 45,
          fontSize: 12
        }
      },
      yAxis: {
        type: 'value',
        name: '架数',
        nameTextStyle: {
          color: 'rgba(255,255,255,0.7)'
        },
        axisLabel: {
          color: 'rgba(255,255,255,0.7)'
        }
      },
      series: [{
        type: 'bar',
        data: data.map(item => item.num),
        barWidth: '40%',
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#83bff6' },
            { offset: 0.5, color: '#188df0' },
            { offset: 1, color: '#188df0' }
          ]),
          borderRadius: [8, 8, 0, 0]
        },
        label: {
          show: true,
          position: 'top',
          color: 'rgba(255,255,255,0.7)'
        },
        markPoint: {
          data: [
            { type: 'max', name: '最大值' },
            { type: 'min', name: '最小值' }
          ],
          label: {
            color: '#fff'
          }
        }
      }]
    }
    airlineStrengthChart.setOption(option)
  } catch (error) {
    console.error('获取航空公司实力数据失败:', error)
  }
}

// 机票价格分析图表
const initTicketPriceChart = async () => {
  ticketPriceChart = initChart(ticketPriceRef, ticketPriceChart)
  if (!ticketPriceChart) return
  
  try {
    const response = await axios.get(`${baseURL}/tables06`)
    console.log('机票价格数据:', response.data)
    const data = response.data
    
    const option = {
      backgroundColor: 'transparent',
      tooltip: {
        trigger: 'item',
        formatter: "航班: {b}<br/>价格: {c}元"
      },
      series: [{
        type: 'funnel',
        left: '10%',
        top: 60,
        bottom: 60,
        width: '80%',
        min: Math.min(...data.map(item => item.price)),
        max: Math.max(...data.map(item => item.price)),
        minSize: '0%',
        maxSize: '100%',
        sort: 'descending',
        gap: 10,
        label: {
          show: true,
          position: 'right',
          color: 'rgba(255,255,255,0.7)',
          formatter: '{b}: {c}元'
        },
        itemStyle: {
          borderColor: '#fff',
          borderWidth: 1
        },
        emphasis: {
          label: {
            fontSize: 20,
            color: '#fff'
          }
        },
        data: data.map(item => ({
          name: item.airline_name,
          value: item.price
        }))
      }]
    }
    ticketPriceChart.setOption(option)
  } catch (error) {
    console.error('获取机票价格数据失败:', error)
  }
}

// 监听容器大小变化
const observeResize = () => {
  resizeObserver = new ResizeObserver(() => {
    airlineStrengthChart?.resize()
    ticketPriceChart?.resize()
  })
  
  const containers = [
    airlineStrengthRef.value,
    ticketPriceRef.value
  ]
  
  containers.forEach(container => {
    if (container) {
      resizeObserver.observe(container)
    }
  })
}

// 定时刷新数据
const startUpdateTimer = () => {
  updateTimer = setInterval(() => {
    initAirlineStrengthChart()
    initTicketPriceChart()
  }, 5000)
}

onMounted(async () => {
  await nextTick()
  
  // 初始化所有图表
  await Promise.all([
    initAirlineStrengthChart(),
    initTicketPriceChart()
  ])
  
  // 设置自适应和定时器
  observeResize()
  startUpdateTimer()
})

onBeforeUnmount(() => {
  resizeObserver?.disconnect()
  clearInterval(updateTimer)
  airlineStrengthChart?.dispose()
  ticketPriceChart?.dispose()
})
</script> 