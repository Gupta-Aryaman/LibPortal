import { createRouter, createWebHistory } from 'vue-router';
import SignupForm from './components/SignupForm.vue';
import UserLoginPage from './components/UserLoginPage.vue';
import LibrarianLoginPage from './components/LibrarianLoginPage.vue';
import UserDashboard from './components/UserDashboard.vue';


const routes = [
    {
        path: '/',
        redirect: '/signup',
    },
    {
        path: '/signup', // Define the URL where your component will be shown
        component: SignupForm, // Specify the component to render
    },
    {
        path: '/login',
        component: UserLoginPage
    },
    {
        path: '/librarian/login',
        component: LibrarianLoginPage,
    },
    {
        path: '/dashboard',
        component: UserDashboard,
    }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
