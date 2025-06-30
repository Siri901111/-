<template>
    <div class="route-analysis">
      <el-row :gutter="20">
        <!-- 热门航线地图 -->
        <el-col :span="24">
          <el-card class="chart-card">
            <template #header>
              <div class="card-header">
                <span style="font-size: 18px;font-weight: 700;">全国航线热力图</span>
              </div>
            </template>
            <div ref="hotRoutesMapRef" class="chart map-chart"></div>
          </el-card>
        </el-col>
        
        <!-- 航线飞行时间散点图 -->
        <el-col :span="12" class="mt-20">
          <el-card class="chart-card">
            <!-- <template #header>
              <div class="card-header">
                <span>航线飞行时间分析</span>
              </div>
            </template> -->
            <div ref="flightTimeScatterRef" class="chart"></div>
          </el-card>
        </el-col>
        
        <!-- 航线网络关系图 -->
        <el-col :span="12" class="mt-20">
          <el-card class="chart-card">
            <!-- <template #header>
              <div class="card-header">
                <span>航线网络关系图</span>
              </div>
            </template> -->
            <div ref="routeNetworkRef" class="chart"></div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, onUnmounted } from 'vue'
  import * as echarts from 'echarts'
  import axios from 'axios'
  import chinaGeoJson from '@/assets/map/china.json'
  
  // 注册中国地图
  echarts.registerMap('china', chinaGeoJson)
  
  // 图表DOM引用
  const hotRoutesMapRef = ref(null)
  const flightTimeScatterRef = ref(null)
  const routeNetworkRef = ref(null)
  
  // 图表实例
  let charts = []
  
  // 城市坐标数据
  const cityCoordinates = {
    '北京': [116.405285, 39.904989],
    '上海': [121.472644, 31.231706],
    '广州': [113.280637, 23.125178],
    '深圳': [114.085947, 22.547],
    '成都': [104.065735, 30.659462],
    '杭州': [120.153576, 30.287459],
    '武汉': [114.298572, 30.584355],
    '西安': [108.948024, 34.263161],
    '重庆': [106.504962, 29.533155],
    '南京': [118.767413, 32.041544],
    '长沙': [112.982279, 28.19409],
    '厦门': [118.089425, 24.479834],
    '昆明': [102.712251, 25.040609],
    '天津': [117.190182, 39.125596],
    '郑州': [113.665412, 34.757975],
    '青岛': [120.355173, 36.082982],
    '沈阳': [123.429096, 41.796767],
    '大连': [121.618622, 38.91459],
    '哈尔滨': [126.642464, 45.756967]
  }
  
  // 初始化热门航线地图
  const initHotRoutesMap = async () => {
    const chart = echarts.init(hotRoutesMapRef.value)
    charts.push(chart)
    
    try {
      const { data } = await axios.get('http://localhost:8080/tables13')
      
      const option = {
        backgroundColor: 'transparent',
        tooltip: {
          trigger: 'item',
          formatter: params => {
            if (params.componentSubType === 'lines') {
              return `${params.data.fromName} -> ${params.data.toName}<br/>
                      航班数量: ${params.data.value}<br/>
                      平均票价: ¥${params.data.avg_price}<br/>
                      准点率: ${params.data.avg_ontime_rate}%`
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
          max: Math.max(...data.map(item => item.flight_count)),
          text: ['高', '低'],
          realtime: false,
          calculable: true,
          inRange: {
            color: ['#040449', '#0B1C8C', '#2940D1', '#3E66F9', '#50E3FF']
          },
          textStyle: {
            color: '#fff'
          }
        },
        geo: {
          map: 'china',
          roam: true,
          emphasis: {
            label: {
              show: true,
              color: '#fff'
            },
            itemStyle: {
              areaColor: '#0160AD'
            }
          },
          itemStyle: {
            areaColor: '#101a3c',
            borderColor: '#1683ff',
            borderWidth: 1
          }
        },
        series: [
          {
            type: 'lines',
            coordinateSystem: 'geo',
            data: data.map(item => ({
              fromName: item.start_city,
              toName: item.end_city,
              coords: [
                cityCoordinates[item.start_city],
                cityCoordinates[item.end_city]
              ],
              value: item.flight_count,
              avg_price: item.avg_price,
              avg_ontime_rate: item.avg_ontime_rate
            })).filter(item => item.coords[0] && item.coords[1]),
            effect: {
              show: true,
              period: 6,
              trailLength: 0.7,
              symbol: 'arrow',
              symbolSize: 5
            },
            lineStyle: {
              width: 1,
              opacity: 0.6,
              curveness: 0.2,
              color: '#fff'
            }
          },
          {
            name: '热力分布',
            type: 'effectScatter',
            coordinateSystem: 'geo',
            data: data.map(item => ({
              name: item.start_city,
              value: [
                cityCoordinates[item.start_city]?.[0] || 0,
                cityCoordinates[item.start_city]?.[1] || 0,
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
            itemStyle: {
              color: params => {
                return new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: '#50E3FF' },
                  { offset: 1, color: '#2940D1' }
                ])
              }
            },
            zlevel: 1
          }
        ]
      }
      chart.setOption(option)
    } catch (error) {
      console.error('获取热门航线数据失败:', error)
    }
  }
  
  // 初始化飞行时间分析图
  const initFlightTimeScatter = async () => {
    const chart = echarts.init(flightTimeScatterRef.value)
    charts.push(chart)
    
    try {
      const { data } = await axios.get('http://localhost:8080/tables14')
      console.log('API返回的数据:', data) // 调试用
      
      // 确保数据格式正确
      if (!Array.isArray(data) || data.length === 0) {
        console.error('数据格式不正确或为空')
        return
      }

      // 使用更简单的2D散点图配置，确保数据可以正确显示
      const option = {
        backgroundColor: 'transparent',
        title: {
          text: '航线飞行时间与票价分析',
          textStyle: {
            color: '#fff'
          }
        },
        legend: {
          data: ['航线'],
          textStyle: {
            color: '#fff'
          }
        },
        grid: {
          left: '5%',
          right: '5%',
          bottom: '5%',
          top: '15%',
          containLabel: true
        },
        tooltip: {
          trigger: 'item',
          backgroundColor: 'rgba(0,0,0,0.8)',
          borderColor: '#fff',
          textStyle: {
            color: '#fff'
          },
          formatter: function(params) {
            const data = params.data
            return `起始城市: ${data.start_city}<br/>
                    目的城市: ${data.end_city}<br/>
                    飞行时间: ${data.flight_time}分钟<br/>
                    票价: ¥${data.price}<br/>
                    航班频次: ${data.frequency}班`
          }
        },
        xAxis: {
          type: 'value',
          name: '飞行时间(分钟)',
          nameTextStyle: {
            color: '#fff',
            fontSize: 14
          },
          axisLine: {
            lineStyle: {
              color: '#fff'
            }
          },
          axisLabel: {
            color: '#fff'
          },
          splitLine: {
            show: true,
            lineStyle: {
              color: 'rgba(255,255,255,0.1)'
            }
          }
        },
        yAxis: {
          type: 'value',
          name: '票价(元)',
          nameTextStyle: {
            color: '#fff',
            fontSize: 14
          },
          axisLine: {
            lineStyle: {
              color: '#fff'
            }
          },
          axisLabel: {
            color: '#fff'
          },
          splitLine: {
            show: true,
            lineStyle: {
              color: 'rgba(255,255,255,0.1)'
            }
          }
        },
        series: [
          {
            name: '航线',
            type: 'scatter',
            symbolSize: function(data) {
              // 根据航班频次调整散点大小
              return Math.sqrt(data[2]) * 3
            },
            data: data.map(item => ({
              value: [
                item.flight_time,
                item.price,
                item.frequency || 1
              ],
              start_city: item.start_city,
              end_city: item.end_city,
              flight_time: item.flight_time,
              price: item.price,
              frequency: item.frequency
            })),
            itemStyle: {
              color: function(params) {
                // 根据飞行时间设置渐变色
                return new echarts.graphic.LinearGradient(0, 0, 1, 1, [
                  {
                    offset: 0,
                    color: '#50E3FF'
                  },
                  {
                    offset: 1,
                    color: '#2940D1'
                  }
                ])
              },
              borderColor: '#fff',
              borderWidth: 1,
              shadowColor: 'rgba(255,255,255,0.5)',
              shadowBlur: 10
            },
            emphasis: {
              itemStyle: {
                borderColor: '#fff',
                borderWidth: 2,
                shadowBlur: 20
              }
            }
          },
          // 添加趋势线
          {
            name: '趋势线',
            type: 'line',
            smooth: true,
            showSymbol: false,
            data: calculateTrendLine(data),
            lineStyle: {
              color: 'rgba(255,255,255,0.3)',
              type: 'dashed'
            }
          }
        ]
      }

      chart.setOption(option)
    } catch (error) {
      console.error('获取或处理数据失败:', error)
    }
  }
  
  // 计算趋势线数据
  function calculateTrendLine(data) {
    if (!data || data.length === 0) return []
    
    // 简单线性回归
    let sumX = 0, sumY = 0, sumXY = 0, sumX2 = 0
    const n = data.length
    
    data.forEach(item => {
      const x = item.flight_time
      const y = item.price
      sumX += x
      sumY += y
      sumXY += x * y
      sumX2 += x * x
    })
    
    const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX)
    const intercept = (sumY - slope * sumX) / n
    
    // 获取x轴的最小值和最大值
    const minX = Math.min(...data.map(item => item.flight_time))
    const maxX = Math.max(...data.map(item => item.flight_time))
    
    // 生成趋势线的两个端点
    return [
      [minX, minX * slope + intercept],
      [maxX, maxX * slope + intercept]
    ]
  }
  
  // 初始化航线网络关系图
  const initRouteNetwork = async () => {
    const chart = echarts.init(routeNetworkRef.value)
    charts.push(chart)
    
    try {
      const { data } = await axios.get('http://localhost:8080/tables15')
      
      // 数据预处理：筛选重要航线
      const threshold = Math.max(...data.map(item => item.value)) * 0.1 // 取最大航班量的10%作为阈值
      const filteredData = data.filter(item => item.value >= threshold)
      
      // 获取所有城市
      const cities = [...new Set([...filteredData.map(item => item.source), ...filteredData.map(item => item.target)])]
      
      // 计算城市节点位置（圆形布局）
      const radius = 300
      const nodeData = cities.map((city, index) => {
        const angle = (index / cities.length) * Math.PI * 2
        return {
          name: city,
          x: radius * Math.cos(angle),
          y: radius * Math.sin(angle),
          symbolSize: 20,
          value: filteredData.reduce((sum, item) => {
            if (item.source === city || item.target === city) {
              sum += item.value
            }
            return sum
          }, 0)
        }
      })

      const option = {
        backgroundColor: 'transparent',
        title: {
          text: '主要航线网络',
          textStyle: {
            color: '#fff',
            fontSize: 16
          }
        },
        tooltip: {
          trigger: 'item',
          formatter: params => {
            if (params.dataType === 'edge') {
              return `${params.data.source} → ${params.data.target}<br/>
                      航班数量: ${params.data.value}班次<br/>
                      平均票价: ¥${params.data.avg_price}<br/>
                      航空公司: ${params.data.airline_count}家`
            }
            return `${params.data.name}<br/>总航班量: ${params.data.value}班次`
          },
          backgroundColor: 'rgba(0,0,0,0.85)',
          borderColor: '#fff',
          textStyle: {
            color: '#fff'
          }
        },
        series: [{
          type: 'graph',
          layout: 'none', // 使用预设的圆形布局
          data: nodeData,
          links: filteredData.map(item => ({
            source: item.source,
            target: item.target,
            value: item.value,
            avg_price: item.avg_price,
            airline_count: item.airline_count,
            lineStyle: {
              width: Math.log(item.value) * 2,
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: '#50E3FF' },
                { offset: 1, color: '#2940D1' }
              ]),
              opacity: 0.6,
              curveness: 0.3
            }
          })),
          itemStyle: {
            color: params => {
              return new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: '#50E3FF' },
                { offset: 1, color: '#2940D1' }
              ])
            },
            borderColor: '#fff',
            borderWidth: 2,
            shadowColor: 'rgba(255,255,255,0.3)',
            shadowBlur: 10
          },
          label: {
            show: true,
            position: 'right',
            color: '#fff',
            fontSize: 12,
            fontWeight: 'bold',
            backgroundColor: 'rgba(0,0,0,0.5)',
            padding: [4, 8],
            borderRadius: 3
          },
          edgeSymbol: ['circle', 'arrow'],
          edgeSymbolSize: [4, 10],
          emphasis: {
            focus: 'adjacency',
            lineStyle: {
              width: 10
            },
            label: {
              fontSize: 14
            }
          }
        }]
      }
      chart.setOption(option)
    } catch (error) {
      console.error('获取航线网络数据失败:', error)
    }
  }
  
  // 监听窗口大小变化
  const handleResize = () => {
    charts.forEach(chart => chart && chart.resize())
  }
  
  onMounted(() => {
    console.log('组件已挂载，开始初始化图表')
    initHotRoutesMap()
    initFlightTimeScatter()
    initRouteNetwork()
    window.addEventListener('resize', handleResize)
  })
  
  onUnmounted(() => {
    window.removeEventListener('resize', handleResize)
    charts.forEach(chart => chart && chart.dispose())
    charts = []
  })
  </script>
  
  <style scoped>
  .route-analysis {
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
  </style>