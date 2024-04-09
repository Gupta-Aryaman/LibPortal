import { createRouter, createWebHistory } from 'vue-router';
import SignupForm from './components/SignupForm.vue';
import UserLoginPage from './components/UserLoginPage.vue';
import LibrarianLoginPage from './components/LibrarianLoginPage.vue';
import UserDashboard from './components/UserDashboard.vue';
import UserMyBooks from './components/UserMyBooks.vue';
import LibrarianDashboard from './components/LibrarianDashboard.vue';
import LibrarianAddSection from './components/LibrarianAddSection.vue';
import LibrarianViewBook from './components/LibrarianViewBook.vue';
import LibrarianAddBookForm from './components/LibrarianAddBookForm.vue';
import LibrarianRequests from './components/LibrarianRequests.vue';
import UserStats from './components/UserStats.vue';
import LibrarianStats from './components/LibrarianStats.vue';

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
    },
    {
        path: '/librarian/add_section',
        component: LibrarianAddSection,
    },
    {
        path: '/librarian/view_books',
        component: LibrarianViewBook,
    },
    {
        path: '/librarian/add_book',
        component: LibrarianAddBookForm,
    },
    {
        path: '/librarian/requests',
        component: LibrarianRequests,
    },
    {
        path: '/stats',
        component: UserStats,
    },
    {
        path: '/librarian/stats',
        component: LibrarianStats,
    }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
