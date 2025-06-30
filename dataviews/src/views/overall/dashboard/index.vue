<template>
  <div class="dashboard-container">
    <div class="chart-grid">
      <div class="chart-card glass-effect">
        <div ref="planeTypeChartRef" style="width: 100%; height: 100%;"></div>
      </div>
      <div class="chart-card glass-effect">
        <div ref="takeoffChartRef" style="width: 100%; height: 100%;"></div>
      </div>
      <div class="chart-card glass-effect">
        <div ref="wordCloudChartRef" style="width: 100%; height: 100%;"></div>
      </div>
      <div class="chart-card glass-effect">
        <div ref="flightRankChartRef" style="width: 100%; height: 100%;"></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard-container {
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
  grid-template-rows: repeat(2, 1fr);
  gap: 20px;
  width: 100%;
  height: 100%;
}

.chart-card {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 300px;
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
</style>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import * as echarts from 'echarts'
import 'echarts-wordcloud'
import axios from 'axios'

const planeTypeChartRef = ref(null)
const takeoffChartRef = ref(null)
const wordCloudChartRef = ref(null)
const flightRankChartRef = ref(null)

let planeTypeChart = null
let takeoffChart = null
let wordCloudChart = null
let flightRankChart = null
let resizeObserver = null
let flightRankTimer = null

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

// 飞机型号占比图表
const initPlaneTypeChart = async () => {
  planeTypeChart = initChart(planeTypeChartRef, planeTypeChart)
  if (!planeTypeChart) return
  
  try {
    const response = await axios.get(`${baseURL}/tables03`)
    console.log('飞机型号数据:', response.data)
    const data = response.data
    
    const option = {
      backgroundColor: 'transparent',
      title: {
        text: "飞机型号占比分析",
        left: 'center',
        top: 20,
        textStyle: {
          fontSize: 18,
          color: "#fff"
        }
      },
      tooltip: {
        trigger: 'item',
        formatter: "{b}: {c}架 ({d}%)"
      },
      legend: {
        orient: 'horizontal',
        bottom: 20,
        textStyle: { color: 'rgba(255,255,255,0.7)' }
      },
      series: [{
        name: '机型分布',
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['50%', '50%'],
        avoidLabelOverlap: true,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#121212',
          borderWidth: 2
        },
        label: {
          show: true,
          formatter: '{b}: {c}架',
          color: 'rgba(255,255,255,0.7)'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 20,
            fontWeight: 'bold',
            color: '#fff'
          }
        },
        data: data.map(item => ({
          name: item.flight_type1,
          value: item.num
        }))
      }]
    }
    planeTypeChart.setOption(option)
  } catch (error) {
    console.error('获取飞机型号数据失败:', error)
  }
}

// 近期起飞架次图表
const initTakeoffChart = async () => {
  takeoffChart = initChart(takeoffChartRef, takeoffChart)
  if (!takeoffChart) return
  
  try {
    const response = await axios.get(`${baseURL}/tables04`)
    console.log('起飞架次数据:', response.data)
    const data = response.data
    
    const option = {
      backgroundColor: 'transparent',
      title: {
        text: "近期起飞架次",
        left: 'center',
        top: 20,
        textStyle: {
          fontSize: 18,
          color: "#fff"
        }
      },
      tooltip: {
        trigger: 'axis',
        formatter: "时间: {b}<br/>起飞架次: {c}"
      },
      grid: {
        top: '15%',
        left: '5%',
        right: '5%',
        bottom: '15%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: data.map(item => item.stime),
        axisLabel: {
          color: 'rgba(255,255,255,0.7)',
          rotate: 45
        }
      },
      yAxis: {
        type: 'value',
        name: '架次',
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
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#83bff6' },
            { offset: 0.5, color: '#188df0' },
            { offset: 1, color: '#188df0' }
          ])
        }
      }]
    }
    takeoffChart.setOption(option)
  } catch (error) {
    console.error('获取起飞架次数据失败:', error)
  }
}

// 热门机场词云图表
const initWordCloudChart = async () => {
  wordCloudChart = initChart(wordCloudChartRef, wordCloudChart)
  if (!wordCloudChart) return
  
  try {
    const response = await axios.get(`${baseURL}/tables02`)
    console.log('机场数据:', response.data)
    const data = response.data
    
    const option = {
      backgroundColor: 'transparent',
      title: {
        text: "热门机场词云",
        left: 'center',
        top: 20,
        textStyle: {
          fontSize: 18,
          color: "#fff"
        }
      },
      tooltip: {
        show: true,
        formatter: "机场: {b}<br/>起飞架次: {c}"
      },
      series: [{
        type: 'wordCloud',
        shape: 'circle',
        left: 'center',
        top: 'center',
        width: '80%',
        height: '80%',
        right: null,
        bottom: null,
        sizeRange: [12, 60],
        rotationRange: [-45, 45],
        rotationStep: 45,
        gridSize: 8,
        drawOutOfBound: false,
        textStyle: {
          fontFamily: 'sans-serif',
          fontWeight: 'bold',
          color: function() {
            return 'rgb(' + [
              Math.round(Math.random() * 160 + 95),
              Math.round(Math.random() * 160 + 95),
              Math.round(Math.random() * 160 + 95)
            ].join(',') + ')'
          }
        },
        emphasis: {
          focus: 'self',
          textStyle: {
            shadowBlur: 10,
            shadowColor: '#333'
          }
        },
        data: data.map(item => ({
          name: item.start_airport_simple,
          value: item.num
        }))
      }]
    }
    wordCloudChart.setOption(option)
  } catch (error) {
    console.error('获取机场数据失败:', error)
  }
}

// 实时航班榜单图表
const initFlightRankChart = async () => {
  flightRankChart = initChart(flightRankChartRef, flightRankChart)
  if (!flightRankChart) return
  
  try {
    const response = await axios.get(`${baseURL}/tables01`)
    console.log('航班数据:', response.data)
    const data = response.data
    
    const option = {
      backgroundColor: 'transparent',
      title: {
        text: "实时航班优惠力度榜单",
        left: 'center',
        top: 20,
        textStyle: {
          fontSize: 18,
          color: "#fff"
        }
      },
      tooltip: {
        trigger: 'axis',
        formatter: "航班: {b}<br/>优惠力度: {c}折"
      },
      grid: {
        top: '15%',
        left: '5%',
        right: '5%',
        bottom: '15%',
        containLabel: true
      },
      xAxis: {
        type: 'value',
        name: '折扣',
        nameTextStyle: {
          color: 'rgba(255,255,255,0.7)'
        },
        axisLabel: {
          color: 'rgba(255,255,255,0.7)'
        }
      },
      yAxis: {
        type: 'category',
        data: data.map(item => item.airline_name),
        axisLabel: {
          color: 'rgba(255,255,255,0.7)',
          width: 100,
          overflow: 'truncate'
        }
      },
      series: [{
        name: '优惠力度',
        type: 'bar',
        data: data.map(item => item.price_desc_math),
        barWidth: '60%',
        itemStyle: {
          color: new echarts.graphic.LinearGradient(1, 0, 0, 0, [
            { offset: 0, color: '#83bff6' },
            { offset: 0.5, color: '#188df0' },
            { offset: 1, color: '#188df0' }
          ]),
          borderRadius: [0, 4, 4, 0]
        },
        label: {
          show: true,
          position: 'right',
          formatter: '{c}折',
          color: 'rgba(255,255,255,0.7)'
        }
      }]
    }
    flightRankChart.setOption(option)
  } catch (error) {
    console.error('获取航班数据失败:', error)
  }
}

// 监听容器大小变化
const observeResize = () => {
  resizeObserver = new ResizeObserver(() => {
    planeTypeChart?.resize()
    takeoffChart?.resize()
    wordCloudChart?.resize()
    flightRankChart?.resize()
  })
  
  const containers = [
    planeTypeChartRef.value,
    takeoffChartRef.value,
    wordCloudChartRef.value,
    flightRankChartRef.value
  ]
  
  containers.forEach(container => {
    if (container) {
      resizeObserver.observe(container)
    }
  })
}

// 定时刷新实时航班数据
const startFlightRankTimer = () => {
  flightRankTimer = setInterval(initFlightRankChart, 5000)
}

onMounted(async () => {
  await nextTick()
  
  // 初始化所有图表
  await Promise.all([
    initPlaneTypeChart(),
    initTakeoffChart(),
    initWordCloudChart(),
    initFlightRankChart()
  ])
  
  // 设置自适应和定时器
  observeResize()
  startFlightRankTimer()
})

onBeforeUnmount(() => {
  resizeObserver?.disconnect()
  clearInterval(flightRankTimer)
  planeTypeChart?.dispose()
  takeoffChart?.dispose()
  wordCloudChart?.dispose()
  flightRankChart?.dispose()
})
</script> 