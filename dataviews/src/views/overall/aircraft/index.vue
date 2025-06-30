<template>
  <div class="aircraft-analysis">
    <el-row :gutter="20">
      <!-- 机型航线覆盖雷达图 -->
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span style="font-size: 18px;font-weight: 800;">机型性能雷达图</span>
              <el-select 
                v-model="selectedAircraft" 
                placeholder="选择机型"
                size="small"
                @change="updateRadarChart"
              >
                <el-option 
                  v-for="item in aircraftList" 
                  :key="item" 
                  :label="item" 
                  :value="item"
                />
              </el-select>
            </div>
          </template>
          <div ref="radarChart" class="chart"></div>
        </el-card>
      </el-col>
      
      <!-- 机型价格对比条形图 -->
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span style="font-size: 18px;font-weight: 800;">机型价格分析</span>
            </div>
          </template>
          <div ref="priceChart" class="chart"></div>
        </el-card>
      </el-col>
      
      <!-- 机型分布地图 -->
      <el-col :span="24" class="mt-20">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span style="font-size: 18px;font-weight: 800;">机型地理分布</span>
              <el-select 
                v-model="selectedMapAircraft" 
                placeholder="选择机型"
                size="small"
                @change="updateMapChart"
              >
                <el-option 
                  v-for="item in aircraftList" 
                  :key="item" 
                  :label="item" 
                  :value="item"
                />
              </el-select>
            </div>
          </template>
          <div ref="mapChart" class="chart map-chart"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import axios from 'axios'

// 加载在线地图数据
const loadMapData = async () => {
  try {
    const response = await fetch('https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json')
    const chinaMap = await response.json()
    echarts.registerMap('china', chinaMap)
  } catch (error) {
    console.error('加载地图数据失败:', error)
  }
}

const radarChart = ref(null)
const priceChart = ref(null)
const mapChart = ref(null)
const selectedAircraft = ref('')
const selectedMapAircraft = ref('')
const aircraftList = ref([])
let charts = []

// 初始化雷达图
const initRadarChart = async () => {
  const chart = echarts.init(radarChart.value)
  charts.push(chart)
  
  try {
    const { data } = await axios.get('http://localhost:8080/tables10')
    aircraftList.value = data.map(item => item.aircraft_type)
    selectedAircraft.value = data[0].aircraft_type
    
    const option = {
      backgroundColor: 'transparent',
      tooltip: {
        trigger: 'item',
        backgroundColor: 'rgba(0,0,0,0.7)',
        borderColor: 'rgba(255,255,255,0.2)',
        textStyle: {
          color: '#fff'
        }
      },
      radar: {
        indicator: [
          { name: '航线覆盖', max: Math.max(...data.map(item => item.route_count)) },
          { name: '城市覆盖', max: Math.max(...data.map(item => item.city_coverage)) },
          { name: '准点率', max: 100 },
          { name: '航班数量', max: Math.max(...data.map(item => item.flight_count)) },
          { name: '平均飞行时间', max: Math.max(...data.map(item => item.avg_flight_time)) }
        ],
        center: ['50%', '50%'],
        radius: '65%',
        splitNumber: 4,
        shape: 'circle',
        axisName: {
          color: '#fff',
          fontSize: 12,
          padding: [3, 5]
        },
        splitArea: {
          areaStyle: {
            color: ['rgba(255,255,255,0.02)', 'rgba(255,255,255,0.05)',
                   'rgba(255,255,255,0.08)', 'rgba(255,255,255,0.11)'],
            shadowColor: 'rgba(0, 0, 0, 0.3)',
            shadowBlur: 10
          }
        },
        axisLine: {
          lineStyle: {
            color: 'rgba(255,255,255,0.2)'
          }
        },
        splitLine: {
          lineStyle: {
            color: 'rgba(255,255,255,0.2)'
          }
        }
      },
      series: [{
        type: 'radar',
        data: [{
          value: [
            data[0].route_count,
            data[0].city_coverage,
            data[0].avg_ontime_rate,
            data[0].flight_count,
            data[0].avg_flight_time
          ],
          name: data[0].aircraft_type,
          symbol: 'circle',
          symbolSize: 6,
          lineStyle: {
            width: 2,
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#1890ff' },
              { offset: 1, color: '#39c8c8' }
            ])
          },
          areaStyle: {
            color: new echarts.graphic.RadialGradient(0.5, 0.5, 1, [
              { offset: 0, color: 'rgba(24,144,255,0.5)' },
              { offset: 1, color: 'rgba(57,200,200,0.1)' }
            ])
          },
          itemStyle: {
            color: '#1890ff',
            borderColor: '#fff',
            borderWidth: 2,
            shadowColor: 'rgba(0,0,0,0.3)',
            shadowBlur: 5
          }
        }]
      }]
    }
    chart.setOption(option)
  } catch (error) {
    console.error('获取机型分析数据失败:', error)
  }
}

// 更新雷达图
const updateRadarChart = async () => {
  const chart = echarts.getInstanceByDom(radarChart.value)
  const { data } = await axios.get('http://localhost:8080/tables10')
  const selectedData = data.find(item => item.aircraft_type === selectedAircraft.value)
  
  const option = chart.getOption()
  option.series[0].data = [{
    value: [
      selectedData.route_count,
      selectedData.city_coverage,
      selectedData.avg_ontime_rate,
      selectedData.flight_count,
      selectedData.avg_flight_time
    ],
    name: selectedData.aircraft_type,
    symbol: 'circle',
    symbolSize: 6,
    lineStyle: {
      width: 2,
      color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
        { offset: 0, color: '#1890ff' },
        { offset: 1, color: '#39c8c8' }
      ])
    },
    areaStyle: {
      color: new echarts.graphic.RadialGradient(0.5, 0.5, 1, [
        { offset: 0, color: 'rgba(24,144,255,0.5)' },
        { offset: 1, color: 'rgba(57,200,200,0.1)' }
      ])
    },
    itemStyle: {
      color: '#1890ff',
      borderColor: '#fff',
      borderWidth: 2,
      shadowColor: 'rgba(0,0,0,0.3)',
      shadowBlur: 5
    }
  }]
  chart.setOption(option)
}

// 初始化价格图表
const initPriceChart = async () => {
  const chart = echarts.init(priceChart.value)
  charts.push(chart)
  
  try {
    const { data } = await axios.get('http://localhost:8080/tables12')
    const option = {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      legend: {
        data: ['平均票价', '最低票价', '最高票价'],
        textStyle: { color: '#fff' },
        top: 10
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: data.map(item => item.aircraft_type),
        axisLabel: {
          color: '#fff',
          rotate: 45
        }
      },
      yAxis: {
        type: 'value',
        name: '价格(元)',
        axisLabel: {
          color: '#fff'
        }
      },
      series: [
        {
          name: '平均票价',
          type: 'bar',
          data: data.map(item => item.avg_price),
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#83bff6' },
              { offset: 0.5, color: '#188df0' },
              { offset: 1, color: '#188df0' }
            ])
          }
        },
        {
          name: '最低票价',
          type: 'bar',
          data: data.map(item => item.min_price),
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#91cc75' },
              { offset: 1, color: '#47a447' }
            ])
          }
        },
        {
          name: '最高票价',
          type: 'bar',
          data: data.map(item => item.max_price),
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#fac858' },
              { offset: 1, color: '#e5a008' }
            ])
          }
        }
      ]
    }
    chart.setOption(option)
  } catch (error) {
    console.error('获取机型价格数据失败:', error)
  }
}

// 初始化地图
const initMapChart = async () => {
  const chart = echarts.init(mapChart.value)
  charts.push(chart)
  
  try {
    const { data } = await axios.get('http://localhost:8080/tables11')
    selectedMapAircraft.value = data[0].aircraft_type
    updateMapChart()
  } catch (error) {
    console.error('获取机型地理分布数据失败:', error)
  }
}

// 更新地图
const updateMapChart = async () => {
  const chart = echarts.getInstanceByDom(mapChart.value)
  const { data } = await axios.get('http://localhost:8080/tables11')
  const selectedData = data.filter(item => item.aircraft_type === selectedMapAircraft.value)
  
  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'item',
      formatter: params => {
        const cityData = selectedData.find(item => item.city === params.name)
        if (cityData) {
          return `${params.name}<br/>
                  航班数量：${cityData.flight_count}<br/>
                  平均票价：${cityData.avg_price}元<br/>
                  目的地数：${cityData.dest_city_count}`
        }
        return params.name
      },
      backgroundColor: 'rgba(0,0,0,0.85)',
      borderColor: '#fff',
      textStyle: {
        color: '#fff'
      }
    },
    visualMap: {
      min: 0,
      max: Math.max(...selectedData.map(item => item.flight_count)),
      text: ['高', '低'],
      realtime: false,
      calculable: true,
      inRange: {
        color: [
          '#040449',
          '#0B1C8C',
          '#2940D1',
          '#3E66F9',
          '#50E3FF'
        ]
      },
      textStyle: {
        color: '#fff',
        fontSize: 12,
        textShadow: '0 0 3px rgba(0,0,0,0.5)'
      },
      left: 'left',
      top: 'bottom'
    },
    geo: {
      map: 'china',
      roam: true,
      emphasis: {
        label: {
          show: true,
          color: '#fff',
          textStyle: {
            textShadow: '0 0 5px #000'
          }
        },
        itemStyle: {
          areaColor: '#0160AD',
          shadowColor: 'rgba(0, 0, 0, 0.5)',
          shadowBlur: 10
        }
      },
      itemStyle: {
        areaColor: '#101a3c',
        borderColor: '#1683ff',
        borderWidth: 1,
        shadowColor: 'rgba(0, 0, 0, 0.5)',
        shadowBlur: 5
      },
      silent: false,
      zoom: 1.2,
      scaleLimit: {
        min: 1,
        max: 3
      }
    },
    series: [
      {
        name: '航班数量',
        type: 'map',
        geoIndex: 0,
        data: selectedData.map(item => ({
          name: item.city,
          value: item.flight_count
        }))
      },
      {
        name: '热力分布',
        type: 'effectScatter',
        coordinateSystem: 'geo',
        data: selectedData.map(item => ({
          name: item.city,
          value: [
            cityCoordinates[item.city]?.[0] || 0,
            cityCoordinates[item.city]?.[1] || 0,
            item.flight_count
          ]
        })),
        symbolSize: val => Math.min(val[2] / 100 + 5, 25),
        showEffectOn: 'render',
        rippleEffect: {
          brushType: 'stroke',
          scale: 4,
          period: 4
        },
        hoverAnimation: true,
        itemStyle: {
          color: params => {
            return new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#50E3FF' },
              { offset: 1, color: '#2940D1' }
            ])
          },
          shadowBlur: 10,
          shadowColor: '#333'
        },
        zlevel: 1
      },
      {
        name: '热力层',
        type: 'heatmap',
        coordinateSystem: 'geo',
        data: selectedData.map(item => ({
          name: item.city,
          value: [
            cityCoordinates[item.city]?.[0] || 0,
            cityCoordinates[item.city]?.[1] || 0,
            item.flight_count
          ]
        })),
        pointSize: 15,
        blurSize: 20,
        minOpacity: 0.3,
        maxOpacity: 0.8
      }
    ]
  }
  chart.setOption(option)
}

// 添加城市经纬度数据（这里只列举部分城市作为示例）
const cityCoordinates = {
  '北京': [116.405285, 39.904989],
  '上海': [121.472644, 31.231706],
  '广州': [113.280637, 23.125178],
  '深圳': [114.085947, 22.547],
  '成都': [104.065735, 30.659462],
  // ... 添加更多城市的经纬度数据
}

// 监听窗口大小变化
const handleResize = () => {
  charts.forEach(chart => chart && chart.resize())
}

onMounted(async () => {
  await loadMapData()  // 先加载地图数据
  initRadarChart()
  initPriceChart()
  initMapChart()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  charts.forEach(chart => chart && chart.dispose())
  charts = []
})
</script>

<style scoped>
.aircraft-analysis {
  padding: 20px;
  height: 100%;
  background: transparent;
}

.chart-card {
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  border: none;
  margin-bottom: 20px;
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

.map-chart {
  height: 600px;
}

.mt-20 {
  margin-top: 20px;
}

:deep(.el-card__header) {
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding: 15px 20px;
}

:deep(.el-card__body) {
  padding: 20px;
}

:deep(.el-select) {
  width: 150px;
}

:deep(.el-select .el-input__inner) {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #fff;
}

:deep(.el-select-dropdown) {
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

:deep(.el-select-dropdown__item) {
  color: #fff;
}

:deep(.el-select-dropdown__item.hover),
:deep(.el-select-dropdown__item:hover) {
  background: rgba(255, 255, 255, 0.1);
}
</style> 