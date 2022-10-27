import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

import {
  Shop,
  StarFilled,
  BellFilled,
  Avatar,
  Tools,
  EditPen,
  Document,
  User
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const routes: Array<RouteRecordRaw> = [
  //自动重定向到login
  {
    path: '/test',
    name: 'test',
    component: () => import('@/views/testView.vue'),
  },
  {
    path: '/',
    redirect: '/student'
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/loginView.vue'),
  },
  // 学生端导航路由
  {
    path: '/student',
    name: 'student',
    component: () => import('@/views/StudentView.vue'),
    children: [
      {
        path: '',
        name: 'topicmarket',
        component: () => import('@/components/TopicsMarket.vue'),
        meta: {
          title: "题目市场",
          icon: Shop,
        }
      },
      {
        path: 'focustopics',
        name: 'focustopics',
        component: () => import('@/components/FocusTopics.vue'),
        meta: {
          title: "选题心愿单",
          icon: StarFilled,
        }
      },
      {
        path: 'mygroup',
        name: 'mygroup',
        component: () => import('@/components/MyGroup.vue'),
        meta: {
          title: "我的小组",
          icon: Avatar,
        }
      },
      {
        path: 'mynotice',
        name: 'mynotice',
        component: () => import('@/components/MyNotice.vue'),
        meta: {
          title: "消息",
          icon: BellFilled,
        }
      },
      {
        path: 'myinfo',
        name: 'myinfo',
        component: () => import('@/components/MyInfo.vue'),
        meta: {
          title: "个人信息",
          icon: Tools,
        }
      },
      {
        path: 'topic/:id',
        name: 'topic',
        component: () => import('@/components/TopicDetail.vue'),
        props: true
      }
    ],
  },

  // 导师端导航路由
  {
    path: '/teacher',
    name: 'teacher',
    component: () => import('@/views/TeacherView.vue'),
    children: [
      {
        path: 'addsubject',
        name: 'addsubject',
        component: () => import('@/components/AddSubject.vue'),
        meta: {
          title: "发布选题",
          icon: EditPen,
        }
      },
      {
        path: '',
        name: 'mysubjects',
        component: () => import('@/components/MySubjects.vue'),
        meta: {
          title: "我发布的课题",
          icon: Document,
        }
      },
      {
        path: 'info',
        name: 'info',
        component: () => import('@/components/TeacherInfo.vue'),
        meta: {
          title: "个人信息",
          icon: User,
        }
      },
      {
        path: 'mysubject/:id',
        name: 'mysubject',
        component: () => import('@/components/TeacherSubjectDetail.vue'),
        props: true
      }
    ],
  },
]

export const router = createRouter({
  history: createWebHistory(),
  routes: routes,
})

router.beforeEach((to) => {
  const isLogin = (sessionStorage['student'] != null) || (sessionStorage['teacher'] != null);
  if (isLogin || to.name == 'login') {
    return true;
  } else {
    ElMessage({
      message: "您尚未登录，请登录后访问！",
      type: "error"
    })
    return { name: 'login' }
  }
})

export default router
