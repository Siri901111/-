import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/overall'
  },
  {
    path: '/overall',
    name: 'Overall',
    component: () => import('../views/overall/index.vue'),
    children: [
      {
        path: '',
        redirect: '/overall/dashboard'
      },
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('../views/overall/dashboard/index.vue')
      },
      {
        path: 'map',
        name: 'Map',
        component: () => import('../views/overall/map/index.vue')
      },
      {
        path: 'analysis',
        name: 'Analysis',
        component: () => import('../views/overall/analysis/index.vue')
      },
      {
        path: 'time',
        name: 'TimeAnalysis',
        component: () => import('../views/overall/time/index.vue'),
        meta: {
          title: '时间维度分析'
        }
      },
      {
        path: 'aircraft',
        name: 'Aircraft',
        component: () => import('../views/overall/aircraft/index.vue'),
        meta: {
          title: '机型分析'
        }
      },
      {
        path: 'route',
        name: 'RouteAnalysis',
        component: () => import('../views/overall/route/index.vue'),
        meta: {
          title: '航线分析'
        }
      },
      {
        path: 'airport',
        name: 'Airport',
        component: () => import('../views/overall/airport/index.vue'),
        meta: {
          title: '机场分析'
        }
      },
      {
        path: 'operation', 
        name: 'Operation',
        component: () => import('../views/overall/operation/index.vue'),
        meta: {
          title: '运营效率'
        }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
