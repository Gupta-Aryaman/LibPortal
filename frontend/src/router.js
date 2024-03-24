import { createRouter, createWebHistory } from 'vue-router';
import SignupForm from './components/SignupForm.vue';
import UserLoginPage from './components/UserLoginPage.vue';
import LibrarianLoginPage from './components/LibrarianLoginPage.vue';
import UserDashboard from './components/UserDashboard.vue';
import UserMyBooks from './components/UserMyBooks.vue';
import LibrarianDashboard from './components/LibrarianDashboard.vue';

const routes = [
    {
        path: '/',
        redirect: '/signup',
    },
    {
        path: '/signup',
        component: SignupForm,
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
    },
    {
        path: '/mybooks',
        component: UserMyBooks,
    },
    {
        path: '/librarian/dashboard',
        component: LibrarianDashboard,
    }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
