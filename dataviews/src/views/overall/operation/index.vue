<template>
    <div class="operation-analysis">
      <el-row :gutter="20">
        <!-- 航班延误原因分析 -->
        <el-col :span="12">
          <el-card class="chart-card">
            <template #header>
              <div class="card-header">
                <span>航班延误原因分析</span>
              </div>
            </template>
            <div ref="delayReasonChartRef" class="chart"></div>
          </el-card>
        </el-col>
  
        <!-- 机场吞吐量与延误率关系 -->
        <el-col :span="12">
          <el-card class="chart-card">
            <template #header>
              <div class="card-header">
                <span>机场吞吐量与延误率关系</span>
              </div>
            </template>
            <div ref="airportDelayChartRef" class="chart"></div>
          </el-card>
        </el-col>
  
        <!-- 航线拥堵程度评估 -->
        <el-col :span="24" class="mt-20">
          <el-card class="chart-card">
            <template #header>
              <div class="card-header">
                <span>航线拥堵程度评估</span>
              </div>
            </template>
            <div ref="routeCongestionChartRef" class="chart"></div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, onUnmounted } from 'vue'
  import * as echarts from 'echarts'
  // 引入 3D 组件
  import 'echarts-gl'
  import axios from 'axios'
  
  const delayReasonChartRef = ref(null)
  const airportDelayChartRef = ref(null)
  const routeCongestionChartRef = ref(null)
  const charts = []
  
  // 修改 initDelayReasonChart 函数
  const initDelayReasonChart = async () => {
    const chart = echarts.init(delayReasonChartRef.value)
    charts.push(chart)
    
    try {
      const { data } = await axios.get('http://localhost:8080/tables19')
      
      const option = {
        backgroundColor: '#1a1a1a',
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        grid3D: {
          boxWidth: 100,
          boxHeight: 80,
          boxDepth: 80,
          viewControl: {
            // 初始视角
            beta: 10,
            alpha: 20,
            distance: 300,
            rotateSensitivity: 1,
            zoomSensitivity: 1
          },
          light: {
            main: {
              intensity: 1.2
            },
            ambient: {
              intensity: 0.3
            }
          }
        },
        xAxis3D: {
          type: 'category',
          data: data.map(item => item.delay_reason),
          axisLabel: {
            interval: 0,
            textStyle: {
              color: '#fff',
              fontSize: 12
            }
          },
          axisLine: {
            lineStyle: {
              color: '#fff'
            }
          }
        },
        yAxis3D: {
          type: 'value',
          name: '延误航班数',
          nameTextStyle: {
            color: '#fff'
          },
          axisLine: {
            lineStyle: {
              color: '#fff'
            }
          }
        },
        zAxis3D: {
          type: 'value',
          name: '平均延误时间(分钟)',
          nameTextStyle: {
            color: '#fff'
          },
          axisLine: {
            lineStyle: {
              color: '#fff'
            }
          }
        },
        series: [{
          type: 'bar3D',
          data: data.map(item => [
            item.delay_reason,
            item.delay_count,
            item.avg_delay_time
          ]),
          shading: 'realistic',
          itemStyle: {
            color: '#2f89cf',
            opacity: 0.8
          },
          emphasis: {
            itemStyle: {
              color: '#ff5722'
            }
          },
          label: {
            show: false,
            formatter: '{b}'
          }
        }]
      }
      
      chart.setOption(option)
    } catch (error) {
      console.error('获取延误原因数据失败:', error)
    }
  }
  
  // 初始化机场吞吐量与延误率关系图表
  const initAirportDelayChart = async () => {
    const chart = echarts.init(airportDelayChartRef.value)
    charts.push(chart)
    
    try {
      const { data } = await axios.get('http://localhost:8080/tables20')
      
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross'
          }
        },
        legend: {
          data: ['总航班数', '延误率'],
          textStyle: {
            color: '#fff'
          }
        },
        xAxis: [
          {
            type: 'category',
            data: data.slice(0, 15).map(item => item.airport),
            axisLabel: {
              rotate: 45,
              color: '#fff'
            }
          }
        ],
        yAxis: [
          {
            type: 'value',
            name: '航班数量',
            axisLabel: {
              color: '#fff'
            }
          },
          {
            type: 'value',
            name: '延误率(%)',
            axisLabel: {
              color: '#fff'
            }
          }
        ],
        series: [
          {
            name: '总航班数',
            type: 'bar',
            data: data.slice(0, 15).map(item => item.total_flights)
          },
          {
            name: '延误率',
            type: 'line',
            yAxisIndex: 1,
            data: data.slice(0, 15).map(item => 
              ((item.delayed_flights / item.total_flights) * 100).toFixed(2)
            )
          }
        ]
      }
      
      chart.setOption(option)
    } catch (error) {
      console.error('获取机场延误数据失败:', error)
    }
  }
  
  // 初始化航线拥堵程度评估图表
  const initRouteCongestionChart = async () => {
    const chart = echarts.init(routeCongestionChartRef.value)
    charts.push(chart)
    
    try {
      const { data } = await axios.get('http://localhost:8080/tables21')
      
      const option = {
        tooltip: {
          trigger: 'item'
        },
        legend: {
          top: '5%',
          left: 'center',
          textStyle: {
            color: '#fff'
          }
        },
        series: [
          {
            type: 'scatter',
            symbolSize: function (data) {
              return Math.sqrt(data[2]) * 3
            },
            emphasis: {
              focus: 'series',
              label: {
                show: true,
                formatter: function (param) {
                  return param.data[3]
                },
                position: 'top'
              }
            },
            itemStyle: {
              shadowBlur: 10,
              shadowColor: 'rgba(120, 36, 50, 0.5)',
              shadowOffsetY: 5,
              color: new echarts.graphic.RadialGradient(0.4, 0.3, 1, [
                {
                  offset: 0,
                  color: 'rgb(251, 118, 123)'
                },
                {
                  offset: 1,
                  color: 'rgb(204, 46, 72)'
                }
              ])
            },
            data: data.map(item => [
              item.flight_count,
              item.avg_ontime_rate,
              item.congested_flights,
              `${item.start_city}-${item.end_city}`
            ])
          }
        ],
        xAxis: {
          name: '航班数量',
          axisLabel: {
            color: '#fff'
          }
        },
        yAxis: {
          name: '准点率(%)',
          axisLabel: {
            color: '#fff'
          }
        }
      }
      
      chart.setOption(option)
    } catch (error) {
      console.error('获取航线拥堵数据失败:', error)
    }
  }
  
  // 初始化所有图表
  onMounted(() => {
    initDelayReasonChart()
    initAirportDelayChart()
    initRouteCongestionChart()
    
    window.addEventListener('resize', handleResize)
  })
  
  // 处理窗口大小变化
  const handleResize = () => {
    charts.forEach(chart => chart.resize())
  }
  
  // 组件卸载时清理
  onUnmounted(() => {
    window.removeEventListener('resize', handleResize)
    charts.forEach(chart => chart.dispose())
  })
  </script>
  
  <style scoped>
  .operation-analysis {
    padding: 20px;
  }
  
  .chart-card {
    background-color: #1a1a1a;
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
    height: 500px;  
    width: 100%;
  }
  
  .mt-20 {
    margin-top: 20px;
  }
  
  :deep(.el-card__header) {
    border-bottom: 1px solid #2c2c2c;
  }
  
  :deep(.el-card__body) {
    padding: 20px;
  }
  </style>