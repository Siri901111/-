<template>
    <div class="airport-analysis">
      <el-row :gutter="20">
        <!-- 机场繁忙度时钟图 -->
        <el-col :span="12">
          <el-card class="chart-card">
            <template #header>
              <div class="card-header">
                <span style="font-size: 18px;font-weight: 700;">机场繁忙度时钟图</span>
                <el-select 
                  v-model="selectedAirport" 
                  placeholder="选择机场"
                  size="small"
                  @change="updateClockChart"
                  style="width: 200px;"
                >
                  <el-option 
                    v-for="item in airportList" 
                    :key="item" 
                    :label="item" 
                    :value="item"
                    
                  />
                </el-select>
              </div>
            </template>
            <div ref="clockChartRef" class="chart"></div>
          </el-card>
        </el-col>
  
        <!-- 机场吞吐量排名 -->
        <el-col :span="12">
          <el-card class="chart-card">
            <template #header>
              <div class="card-header">
                <span style="font-size: 18px;font-weight: 700;">机场吞吐量排名</span>
              </div>
            </template>
            <div ref="rankChartRef" class="chart"></div>
          </el-card>
        </el-col>
  
        <!-- 机场航线网络关系图 -->
        <el-col :span="24" class="mt-20">
          <el-card class="chart-card">
            <div ref="networkChartRef" class="chart network-chart"></div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, onUnmounted } from 'vue'
  import * as echarts from 'echarts'
  import axios from 'axios'
  
  // 图表DOM引用
  const clockChartRef = ref(null)
  const rankChartRef = ref(null)
  const networkChartRef = ref(null)
  
  // 选择器数据
  const selectedAirport = ref('')
  const airportList = ref([])
  
  // 图表实例数组
  let charts = []
  
  // 初始化机场繁忙度时钟图
  const initClockChart = async () => {
    const chart = echarts.init(clockChartRef.value)
    charts.push(chart)
  
    try {
      const { data } = await axios.get('http://localhost:8080/tables16')
      // 获取所有机场列表
      airportList.value = [...new Set(data.map(item => item.airport))]
      selectedAirport.value = airportList.value[0]
  
      const option = {
        backgroundColor: 'transparent',
        title: {
          text: '24小时航班分布',
          textStyle: {
            color: '#fff'
          }
        },
        polar: {
          radius: ['20%', '80%']
        },
        angleAxis: {
          type: 'category',
          data: Array.from({length: 24}, (_, i) => `${i}:00`),
          boundaryGap: false,
          splitLine: {
            show: true,
            lineStyle: {
              color: 'rgba(255,255,255,0.2)'
            }
          },
          axisLine: {
            lineStyle: {
              color: '#fff'
            }
          }
        },
        radiusAxis: {
          type: 'value',
          axisLine: {
            show: false
          },
          axisLabel: {
            color: '#fff'
          },
          splitLine: {
            lineStyle: {
              color: 'rgba(255,255,255,0.2)'
            }
          }
        },
        series: [{
          name: '航班数量',
          type: 'bar',
          coordinateSystem: 'polar',
          data: data
            .filter(item => item.airport === selectedAirport.value)
            .map(item => ({
              value: item.flight_count,
              itemStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: '#50E3FF' },
                  { offset: 1, color: '#2940D1' }
                ])
              }
            })),
          barWidth: 8,
          roundCap: true
        }]
      }
      chart.setOption(option)
    } catch (error) {
      console.error('获取机场繁忙度数据失败:', error)
    }
  }
  
  // 更新时钟图
  const updateClockChart = async () => {
    const chart = echarts.getInstanceByDom(clockChartRef.value)
    const { data } = await axios.get('http://localhost:8080/tables16')
    
    const option = chart.getOption()
    option.series[0].data = data
      .filter(item => item.airport === selectedAirport.value)
      .map(item => ({
        value: item.flight_count,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#50E3FF' },
            { offset: 1, color: '#2940D1' }
          ])
        }
      }))
    chart.setOption(option)
  }
  
  // 初始化机场吞吐量排名图
  const initRankChart = async () => {
    const chart = echarts.init(rankChartRef.value)
    charts.push(chart)
  
    try {
      const { data } = await axios.get('http://localhost:8080/tables18')
      // 取前15个机场数据
      const top15Data = data.slice(0, 15)
  
      const option = {
        backgroundColor: 'transparent',
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          },
          formatter: function(params) {
            const data = params[0].data
            return `${data.name}<br/>
                    航班数量: ${data.value}<br/>
                    航空公司: ${data.avg_airline_count}家<br/>
                    平均票价: ¥${data.avg_price.toFixed(2)}<br/>
                    准点率: ${data.avg_ontime_rate.toFixed(1)}%`
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'value',
          axisLabel: {
            color: '#fff'
          },
          splitLine: {
            lineStyle: {
              color: 'rgba(255,255,255,0.1)'
            }
          }
        },
        yAxis: {
          type: 'category',
          data: top15Data.map(item => item.airport),
          axisLabel: {
            color: '#fff'
          }
        },
        series: [{
          name: '总航班数',
          type: 'bar',
          data: top15Data.map(item => ({
            name: item.airport,
            value: item.total_flights,
            avg_airline_count: Math.round(item.avg_airline_count),
            avg_price: item.avg_price,
            avg_ontime_rate: item.avg_ontime_rate,
            itemStyle: {
              color: new echarts.graphic.LinearGradient(1, 0, 0, 0, [
                { offset: 0, color: '#50E3FF' },
                { offset: 1, color: '#2940D1' }
              ])
            }
          })),
          label: {
            show: true,
            position: 'right',
            color: '#fff'
          }
        }]
      }
      chart.setOption(option)
    } catch (error) {
      console.error('获取机场排名数据失败:', error)
    }
  }
  
  // 初始化机场航线网络关系图
  const initNetworkChart = async () => {
    const chart = echarts.init(networkChartRef.value)
    charts.push(chart)
  
    try {
      const { data } = await axios.get('http://localhost:8080/tables17')
      
      // 获取所有机场
      const airports = [...new Set([...data.map(item => item.source), ...data.map(item => item.target)])]
      
      // 计算节点大小（基于连接数）
      const airportConnections = {}
      airports.forEach(airport => {
        airportConnections[airport] = data.filter(item => 
          item.source === airport || item.target === airport
        ).length
      })
  
      const option = {
        backgroundColor: 'transparent',
        title: {
          text: '机场航线网络',
          left: 'center',
          top: 20,
          textStyle: {
            color: '#fff'
          }
        },
        tooltip: {
          trigger: 'item',
          formatter: function(params) {
            if (params.dataType === 'edge') {
              const data = params.data
              return `${data.source} → ${data.target}<br/>
                      航班数量: ${data.flight_count}<br/>
                      航空公司: ${data.airline_count}家<br/>
                      平均票价: ¥${Number(data.avg_price).toFixed(2)}<br/>
                      准点率: ${Number(data.avg_ontime_rate).toFixed(1)}%`
            }
            return `${params.name}<br/>连接航线数: ${airportConnections[params.name]}`
          }
        },
        series: [{
          type: 'graph',
          layout: 'force',
          data: airports.map(airport => ({
            name: airport,
            symbolSize: Math.sqrt(airportConnections[airport]) * 5,
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 1, 1, [
                { offset: 0, color: '#50E3FF' },
                { offset: 1, color: '#2940D1' }
              ])
            }
          })),
          links: data.map(item => ({
            source: item.source,
            target: item.target,
            flight_count: item.flight_count,
            airline_count: item.airline_count,
            avg_price: item.avg_price,
            avg_ontime_rate: item.avg_ontime_rate,
            lineStyle: {
              width: Math.log(item.flight_count) * 2,
              color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                { offset: 0, color: '#50E3FF' },
                { offset: 1, color: '#2940D1' }
              ]),
              opacity: 0.6
            }
          })),
          force: {
            repulsion: 100,
            gravity: 0.1,
            edgeLength: 200,
            layoutAnimation: true
          },
          label: {
            show: true,
            color: '#fff',
            fontSize: 10
          },
          emphasis: {
            focus: 'adjacency',
            lineStyle: {
              width: 10
            }
          }
        }]
      }
      chart.setOption(option)
    } catch (error) {
      console.error('获取机场网络数据失败:', error)
    }
  }
  
  // 监听窗口大小变化
  const handleResize = () => {
    charts.forEach(chart => chart && chart.resize())
  }
  
  onMounted(() => {
    initClockChart()
    initRankChart()
    initNetworkChart()
    window.addEventListener('resize', handleResize)
  })
  
  onUnmounted(() => {
    window.removeEventListener('resize', handleResize)
    charts.forEach(chart => chart && chart.dispose())
    charts = []
  })
  </script>
  
  <style scoped>
  .airport-analysis {
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
  
  .network-chart {
    height: 500px;
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