import { createRouter, createWebHistory } from 'vue-router'
import Hero from '../components/Hero.vue'
import Login from '../components/Login.vue'
import Dashboard from '../components/Dashbaord.vue'
import AddTeacher from '../components/Add_teacher.vue'
import AddStudent from '../components/Add_student.vue'
import AddSubject from '../components/Add_subject.vue'
import ManageMarks from '../components/Manage_marks.vue'
import ViewResults from '../components/View_results.vue'
import ManageStudents from '../components/Manage_students.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Hero
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
    },
    {
      path: '/admin/add-subject',
      name: 'add-subject',
      component: AddSubject,
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
      path: '/teacher/manage-marks',
      name: 'manage-marks',
      component: ManageMarks,
      meta: { requiresAuth: true, requiresTeacher: true }
    },
    {
      path: '/student/view-results',
      name: 'view-results',
      component: ViewResults,
      meta: { requiresAuth: true, requiresStudentOrAdmin: true }
    },
    {
      path: '/manage-students',
      name: 'manage-students',
      component: ManageStudents,
      meta: { requiresAuth: true, requiresTeacherOrAdmin: true }
    },
    {
      path: '/student-results',
      name: 'student-results',
      component: ViewResults,
      meta: { requiresAuth: true }
    }
  ]
})
router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('token') || sessionStorage.getItem('token');
  const userRole = localStorage.getItem('userRole') || sessionStorage.getItem('userRole');
  
  console.log('Route guard - Token exists:', !!token, 'Going to:', to.name, 'User role:', userRole);
  
  if (to.meta.requiresAuth && !token) {
    console.log('No token found, redirecting to login');
    next('/login');
  } else if (to.meta.requiresAdmin && userRole !== 'admin') {
    console.log('Admin access required, user role is:', userRole);
    next('/dashboard');
  } else if (to.meta.requiresTeacher && userRole !== 'teacher') {
    console.log('Teacher access required, user role is:', userRole);
    next('/dashboard');
  } else if (to.meta.requiresStudent && userRole !== 'student') {
    console.log('Student access required, user role is:', userRole);
    next('/dashboard');
  } else if (to.meta.requiresTeacherOrAdmin && userRole !== 'teacher' && userRole !== 'admin') {
    console.log('Teacher or Admin access required, user role is:', userRole);
    next('/dashboard');
  } else if (to.meta.requiresStudentOrAdmin && userRole !== 'student' && userRole !== 'admin') {
    console.log('Student or Admin access required, user role is:', userRole);
    next('/dashboard');
  } else if (to.name === 'login' && token) {
    console.log('Already logged in, redirecting to dashboard');
    next('/dashboard');
  } else {
    next();
  }
});

export default router
