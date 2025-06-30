<template>
  <div class="layout-container">
    <div class="layout-header">
      <div class="header-left">
        <div class="logo">
          <el-icon class="logo-icon"><Airplane /></el-icon>
          <span class="logo-text">航线运输系统</span>
        </div>
      </div>
      <div class="header-right">
        <div class="theme-switch-container">
          <div class="theme-switch-slider" :class="{ 'dark': isDarkTheme }"></div>
          <button 
            class="theme-btn light-btn" 
            :class="{ 'active': !isDarkTheme }"
            @click="() => !isDarkTheme || toggleTheme()"
          >
            <el-icon><Sunny /></el-icon>
          </button>
          <button 
            class="theme-btn dark-btn" 
            :class="{ 'active': isDarkTheme }"
            @click="() => isDarkTheme || toggleTheme()"
          >
            <el-icon><Moon /></el-icon>
          </button>
        </div>
      </div>
    </div>
    
    <div class="layout-content">
      <div class="sidebar">
        <div class="menu-container">
          <div class="custom-menu">
            <div 
              v-for="menuItem in menuItems" 
              :key="menuItem.path"
              class="menu-pill"
              :class="{ 'active': activeMenu === menuItem.path }"
              @click="handleMenuClick(menuItem.path)"
            >
              <div class="menu-pill-content">
                <el-icon class="menu-icon">
                  <component :is="menuItem.icon" />
                </el-icon>
                <span class="menu-text">{{ menuItem.name }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="main-content">
        <div class="breadcrumb">
          <el-breadcrumb :separator-icon="ArrowRight">
            <el-breadcrumb-item 
              v-for="(item, index) in breadcrumbList" 
              :key="index"
            >
              <span 
                class="breadcrumb-text"
                @click="handleBreadcrumbClick(item.path)"
                :class="{ 
                  'is-last': index === breadcrumbList.length - 1,
                  'is-link': index !== breadcrumbList.length - 1 
                }"
              >
                {{ item.name }}
              </span>
            </el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="page-container">
          <router-view v-slot="{ Component }">
            <transition name="fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, inject } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Timer, ArrowRight, Sunny, Moon, DataLine, MapLocation, TrendCharts, Position, Share, Location } from '@element-plus/icons-vue'

// 注入主题功能
const theme = inject('theme')
const { isDarkTheme, toggleTheme } = theme

const route = useRoute()
const router = useRouter()
const isCollapse = ref(false)
const activeMenu = computed(() => route.path)

// 菜单项数据
const menuItems = [
  { path: '/overall/dashboard', name: '数据总览', icon: DataLine },
  { path: '/overall/map', name: '地图分析', icon: MapLocation },
  { path: '/overall/analysis', name: '航司展板', icon: TrendCharts },
  { path: '/overall/time', name: '时间分析', icon: Timer },
  { path: '/overall/aircraft', name: '机型分析', icon: Position },
  { path: '/overall/route', name: '航线分析', icon: Share },
  { path: '/overall/airport', name: '机场分析', icon: Location },
  { path: '/overall/operation', name: '延误分析', icon: TrendCharts }
]

// 处理菜单点击
const handleMenuClick = (path) => {
  router.push(path)
}

// 页面映射表
const pageNameMap = {
  '/overall': '数据总览',
  '/overall/dashboard': '数据总览',
  '/overall/map': '地图分析',
  '/overall/analysis': '航司展板',
  '/overall/time': '时间分析',
  '/overall/aircraft': '机型分析',
  '/overall/route': '航线分析',
  '/overall/airport': '机场分析',
  '/overall/operation': '延误分析'
}

// 面包屑路径追踪
const breadcrumbList = ref([
  { path: '/overall/dashboard', name: '数据总览' }
])

// 获取路径的所有层级，但排除重复的数据总览
const getPathLevels = (path) => {
  const parts = path.split('/').filter(Boolean)
  const levels = parts.map((_, index) => '/' + parts.slice(0, index + 1).join('/'))
  
  // 如果是 dashboard 路径，只返回数据总览
  if (path.includes('/dashboard')) {
    return ['/overall/dashboard']
  }
  
  // 对于其他路径，始终以数据总览开头
  return ['/overall/dashboard', path]
}

// 监听路由变化，更新面包屑
watch(
  () => route.path,
  (newPath) => {
    // 获取处理后的路径层级
    const pathLevels = getPathLevels(newPath)
    
    // 构建新的面包屑列表
    const newBreadcrumbs = pathLevels.map(path => ({
      path,
      name: pageNameMap[path] || path.split('/').pop()
    }))

    // 更新面包屑列表
    breadcrumbList.value = newBreadcrumbs
  },
  { immediate: true }
)

// 处理面包屑点击
const handleBreadcrumbClick = (path) => {
  router.push(path)
}
</script>

<style scoped>
.layout-container {
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--primary-bg);
  overflow: hidden;
  transition: all 0.3s ease;
}

.layout-header {
  height: 60px;
  background: var(--gradient-accent);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  box-shadow: 0 2px 10px var(--shadow-color);
  z-index: 1000;
  transition: all 0.3s ease;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo-icon {
  font-size: 24px;
  color: var(--primary-bg);
}

.logo-text {
  font-size: 20px;
  font-weight: bold;
  color: var(--primary-bg);
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
  letter-spacing: 0.5px;
}

.header-right {
  display: flex;
  align-items: center;
}

/* 胶囊式主题切换器 */
.theme-switch-container {
  position: relative;
  display: flex;
  align-items: center;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 25px;
  padding: 4px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  overflow: hidden;
  transition: all 0.3s ease;
}

/* 滑动指示器 */
.theme-switch-slider {
  position: absolute;
  top: 4px;
  left: 4px;
  width: 36px;
  height: 36px;
  background: var(--primary-bg);
  border-radius: 50%;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  z-index: 1;
}

.theme-switch-slider.dark {
  left: calc(100% - 40px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2),
              0 0 15px rgba(0, 191, 255, 0.3);
}

/* 主题按钮 */
.theme-btn {
  position: relative;
  width: 36px;
  height: 36px;
  border: none;
  background: transparent;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 2;
}

.theme-btn .el-icon {
  font-size: 18px;
  transition: all 0.3s ease;
}

.light-btn .el-icon {
  color: var(--primary-bg);
  opacity: 0.7;
}

.dark-btn .el-icon {
  color: var(--primary-bg);
  opacity: 0.7;
}

.theme-btn.active .el-icon {
  color: var(--accent-color);
  opacity: 1;
  transform: scale(1.1);
}

.theme-btn:hover:not(.active) {
  transform: scale(1.05);
}

.theme-btn:hover:not(.active) .el-icon {
  color: var(--accent-hover);
}
/* 
.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #fff;
  cursor: pointer;
} */

.layout-content {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.sidebar {
  width: 200px;
  background: var(--secondary-bg);
  box-shadow: 2px 0 10px var(--shadow-color);
  z-index: 999;
  transition: all 0.3s ease;
}

.menu-container {
  height: calc(100vh - 60px);
  overflow-y: auto;
  padding: 20px 12px;
}

/* 自定义胶囊式菜单 */
.custom-menu {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.menu-pill {
  position: relative;
  background: var(--card-bg);
  border-radius: 25px;
  padding: 4px;
  border: 1px solid var(--border-color);
  backdrop-filter: blur(10px);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.menu-pill:hover {
  background: var(--hover-bg);
  transform: translateX(4px);
  box-shadow: 0 4px 12px var(--shadow-color);
}

.menu-pill.active {
  background: var(--gradient-accent);
  border-color: var(--accent-color);
  box-shadow: 0 4px 16px var(--shadow-color), 
              0 0 20px rgba(0, 191, 255, 0.4),
              inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.menu-pill-content {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 20px;
  transition: all 0.3s ease;
}

.menu-icon {
  font-size: 18px;
  color: var(--secondary-text);
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.menu-text {
  font-size: 14px;
  color: var(--secondary-text);
  font-weight: 500;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.menu-pill.active .menu-icon,
.menu-pill.active .menu-text {
  color: var(--primary-bg);
  font-weight: 600;
}

.menu-pill:hover:not(.active) .menu-icon,
.menu-pill:hover:not(.active) .menu-text {
  color: var(--accent-color);
}

.menu-pill.active .menu-icon {
  transform: scale(1.1);
}

/* 添加微妙的渐变效果 */
.menu-pill::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, transparent 0%, var(--accent-color) 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: 25px;
}

.menu-pill.active::before {
  opacity: 0.1;
}

.main-content {
  flex: 1;
  height: calc(100vh - 60px);
  overflow-y: auto;
  background: var(--primary-bg);
  padding: 16px;
  transition: all 0.3s ease;
}

.breadcrumb {
  margin-bottom: 20px;
  padding: 12px 20px;
  background: var(--card-bg);
  border-radius: 8px;
  backdrop-filter: blur(10px);
  border: 1px solid var(--border-color);
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 191, 255, 0.1),
              inset 0 1px 0 rgba(255, 255, 255, 0.05);
}

.breadcrumb-text {
  font-size: 15px;
  padding: 4px 12px;
  border-radius: 4px;
  color: var(--secondary-text);
  transition: all 0.3s ease;
}

.breadcrumb-text.is-link {
  cursor: pointer;
}

.breadcrumb-text.is-link:hover {
  color: var(--accent-color);
  background: var(--hover-bg);
}

.breadcrumb-text.is-last {
  color: var(--primary-text);
  cursor: default;
}

:deep(.el-breadcrumb__separator) {
  transform: scale(1.15);
  margin: 0 8px;
  color: var(--secondary-text) !important;
  transition: all 0.3s;
}

:deep(.el-breadcrumb__item) {
  display: inline-flex;
  align-items: center;
  padding: 4px 0;
  
  &:hover {
    .el-breadcrumb__separator {
      color: var(--accent-color) !important;
      transform: scale(1.3);
    }
  }
}

:deep(.el-breadcrumb__inner) {
  display: inline-flex;
  align-items: center;
}

/* 箭头图标样式 */
:deep(.el-icon) {
  font-size: 16px;
  margin: 0 8px;
  color: var(--secondary-text);
  transition: all 0.3s;
}

/* 当鼠标悬停在面包屑项上时，箭头的动画效果 */
:deep(.el-breadcrumb__item:hover) {
  .el-icon {
    color: var(--accent-color);
    transform: translateX(3px) scale(1.2);
  }
}

.page-container {
  background: var(--card-bg);
  border-radius: 12px;
  padding: 20px;
  min-height: calc(100vh - 180px);
  border: 1px solid var(--border-color);
  transition: all 0.3s ease;
  box-shadow: 0 8px 32px rgba(0, 191, 255, 0.1),
              inset 0 1px 0 rgba(255, 255, 255, 0.05),
              0 0 0 1px rgba(0, 191, 255, 0.1);
  backdrop-filter: blur(20px);
}

/* 主题覆盖 */
:deep(.el-dropdown-menu) {
  background: var(--secondary-bg) !important;
  border: 1px solid var(--border-color) !important;
}

:deep(.el-dropdown-menu__item) {
  color: var(--primary-text) !important;
}

:deep(.el-dropdown-menu__item:hover) {
  background: var(--hover-bg) !important;
}

/* 滚动条样式 */
.main-content::-webkit-scrollbar,
.menu-container::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

.main-content::-webkit-scrollbar-thumb,
.menu-container::-webkit-scrollbar-thumb {
  background: var(--accent-color);
  border-radius: 3px;
  opacity: 0.7;
}

.main-content::-webkit-scrollbar-thumb:hover,
.menu-container::-webkit-scrollbar-thumb:hover {
  background: var(--accent-hover);
  opacity: 1;
}

.main-content::-webkit-scrollbar-track,
.menu-container::-webkit-scrollbar-track {
  background: var(--secondary-bg);
}

/* 页面切换动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style> 