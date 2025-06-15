import { createRouter, createWebHistory } from 'vue-router'
import Hero from '../components/Hero.vue'
import SignUp from '../components/SignUp.vue'
import Login from '../components/Login.vue'
import Dashboard from '../components/Dashbaord.vue'
import AddTeacher from '../components/Add_teacher.vue'
import AddStudent from '../components/Add_student.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Hero
    },
    {
      path: '/sign-up',
      name: 'signup',
      component: SignUp
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path:'/dashboard',
      name: 'dashboard',
      component:Dashboard,
      meta: { requiresAuth: true }
    },
    {
      path: '/admin/add-teacher',
      name: 'add-teacher',
      component: AddTeacher,
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
      path: '/admin/add-student',
      name: 'add-student',
      component: AddStudent,
      meta: { requiresAuth: true, requiresAdmin: true }
    }

  ]
})

// Navigation guard for authentication
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token') || sessionStorage.getItem('token');
  const userRole = localStorage.getItem('userRole') || sessionStorage.getItem('userRole');
  
  console.log('Route guard - Token exists:', !!token, 'Going to:', to.name, 'User role:', userRole);
  
  if (to.meta.requiresAuth && !token) {
    console.log('No token found, redirecting to login');
    next('/login');
  } else if (to.meta.requiresAdmin && userRole !== 'admin') {
    console.log('Admin access required, user role is:', userRole);
    next('/dashboard'); // Redirect non-admin users to dashboard
  } else if (to.name === 'login' && token) {
    console.log('Already logged in, redirecting to dashboard');
    next('/dashboard');
  } else {
    next();
  }
});

export default router
