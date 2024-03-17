import { createRouter, createWebHistory } from 'vue-router';
import SignupForm from './components/SignupForm.vue';

const routes = [
    {
        path: '/',
        redirect: '/signup',
    },
    {
        path: '/signup', // Define the URL where your component will be shown
        component: SignupForm, // Specify the component to render
    }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
