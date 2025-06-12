import { createRouter, createWebHistory } from 'vue-router';
import SignUp from '../components/SignUp.vue';
import Hero from '../components/Hero.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: Hero,
  },
  {
    path: '/sign-up',
    name: 'signup',
    component: SignUp,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
