<template>
  <div class="app-container" :class="themeClass">
    <router-view></router-view>
  </div>
</template>

<script setup>
import { ref, provide, computed } from 'vue'

// 主题状态管理
const isDarkTheme = ref(false) // 默认白天模式

// 计算主题类名
const themeClass = computed(() => isDarkTheme.value ? 'dark-theme' : 'light-theme')

// 切换主题
const toggleTheme = () => {
  isDarkTheme.value = !isDarkTheme.value
  // 保存主题偏好到localStorage
  localStorage.setItem('theme', isDarkTheme.value ? 'dark' : 'light')
}

// 从localStorage恢复主题设置
const savedTheme = localStorage.getItem('theme')
if (savedTheme) {
  isDarkTheme.value = savedTheme === 'dark'
} else {
  // 默认设置为白天模式
  isDarkTheme.value = false
}

// 提供给子组件使用
provide('theme', {
  isDarkTheme,
  toggleTheme
})
</script>

<style>
.app-container {
  width: 100%;
  height: 100%;
  overflow: hidden;
  transition: all 0.3s ease;
}

/* 夜间主题 - 深蓝科技风配色 */
.dark-theme {
  --primary-bg: #0a1428;
  --secondary-bg: #0f1b2e;
  --card-bg: rgba(20, 50, 90, 0.3);
  --hover-bg: rgba(0, 191, 255, 0.1);
  --primary-text: #ffffff;
  --secondary-text: rgba(255, 255, 255, 0.8);
  --accent-color: #00bfff; /* 科技蓝 */
  --accent-hover: #1e90ff;
  --border-color: rgba(0, 191, 255, 0.3);
  --shadow-color: rgba(0, 191, 255, 0.2);
  --gradient-primary: linear-gradient(135deg, #0a1428 0%, #1a2642 100%);
  --gradient-accent: linear-gradient(135deg, #00bfff 0%, #1e90ff 100%);
  
  background: var(--primary-bg);
  color: var(--primary-text);
}

/* 白天主题 - 米色和橙色配色 */
.light-theme {
  --primary-bg: #f5f5dc; /* 米色 */
  --secondary-bg: #ffffff;
  --card-bg: rgba(255, 255, 255, 0.8);
  --hover-bg: rgba(255, 140, 0, 0.1);
  --primary-text: #333333;
  --secondary-text: #666666;
  --accent-color: #ff8c00; /* 橙色 */
  --accent-hover: #ff7700;
  --border-color: rgba(255, 140, 0, 0.2);
  --shadow-color: rgba(255, 140, 0, 0.2);
  --gradient-primary: linear-gradient(135deg, #f5f5dc 0%, #faf0e6 100%);
  --gradient-accent: linear-gradient(135deg, #ff8c00 0%, #ffa500 100%);
  
  background: var(--primary-bg);
  color: var(--primary-text);
}


</style>
