<template>
    <nav class="navbar navbar-dark bg-dark navbar-expand-lg ">
        <div class="container-fluid">
            <router-link :to="{ path: '/dashboard' }" class="navbar-brand">Hey, {{ username }}! </router-link>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <router-link :to="{ path: '/mybooks' }" class="nav-link" :class="{ 'active': isActive('/mybooks') }">MyBooks</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link :to="{ path: '/dashboard' }" class="nav-link" :class="{ 'active': isActive('/dashboard') }">Books</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link :to="{ path: '/stats' }" class="nav-link" :class="{ 'active': isActive('/stats') }">Stats</router-link>
                    </li>
                    
                    <li class="nav-item">
                        <button class="nav-link" v-on:click="logout">Logout</button>
                    </li>
                </ul>

            </div>
            <form class="d-flex p-1 search" role="search">
                <input class="form-control me-2" type="search" placeholder="Search for books" aria-label="Search" v-model="searchQuery">
                <button class="btn btn-outline-success me-2" v-on:click="searchBook($event)">Search Books</button>
                <button class="btn btn-outline-success" v-on:click="searchSection($event)">Search Sections</button>
            </form>

        </div>
    </nav>
</template>

<script>
    import { useRoute } from 'vue-router';

    export default {
        name : 'UserHeader',
        setup() {
            const route = useRoute();

            function isActive(url) {
                return route.path === url;
            }

            return {
                isActive
            };
        },
        props: {
            activePage: String,
            queryString: String
        },
        data() {
            return {
                isUserLoggedIn: false,
                username: '',
                searchQuery: this.queryString
            };
        },
        mounted() {
            if (localStorage.getItem('user_token') && localStorage.getItem('user')) {
                this.isUserLoggedIn = true;
                this.username = localStorage.getItem('user');
            } else{
                this.logout();
            }
        },
        methods: {
            logout() {
                localStorage.removeItem('user_token');
                this.isUserLoggedIn = false;
                window.location.href = '/login';
            },
            searchBook(event) {
                event.preventDefault();
                window.location.href = `/dashboard?title=${this.searchQuery}`;
            },
            searchSection(event) {
                event.preventDefault();
                window.location.href = `/dashboard?section=${this.searchQuery}`;
            }
        }
    }
</script>

<style scoped>
    .search {
        max-height: 70px;
    }
</style>