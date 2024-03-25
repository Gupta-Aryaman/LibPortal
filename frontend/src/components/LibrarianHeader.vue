<template>
    <nav class="navbar navbar-dark bg-dark navbar-expand-lg ">
        <div class="container-fluid">
            <router-link :to="{ path: '/librarian/dashboard' }" class="navbar-brand">Hey, {{ username }}! </router-link>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <router-link :to="{ path: '/librarian/dashboard' }" class="nav-link" :class="{ 'active': isActive('/librarian/dashboard') }">Sections</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link :to="{ path: '/librarian/requests' }" class="nav-link" :class="{ 'active': isActive('/librarian/requests') }">Requests</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link :to="{ path: '/librarian/stats' }" class="nav-link" :class="{ 'active': isActive('/librarian/stats') }">Stats</router-link>
                    </li>
                    
                    <li class="nav-item">
                        <button class="nav-link" v-on:click="logout">Logout</button>
                    </li>
                </ul>

            </div>
            <form class="d-flex p-3 search" role="search">
                <input class="form-control me-2" type="search" placeholder="Search for Sections" aria-label="Search" v-model="searchQuery">
                <button class="btn btn-outline-success" v-on:click="searchSection($event)">Search</button>
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
            // searchBook(event) {
            //     event.preventDefault();
            //     window.location.href = `/dashboard?title=${this.searchQuery}`;
            // },
            searchSection(event) {
                event.preventDefault();
                // window.location.href = `/librarian/dashboard?section=${this.searchQuery}`;
                this.$emit('search_section', this.searchQuery)
            }
        }
    }
</script>

<style scoped>
    .search {
        max-height: 70px;
    }
</style>