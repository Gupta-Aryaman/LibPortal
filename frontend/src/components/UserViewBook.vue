<template>
    <UserHeader />
    <div v-if="errorData != ''">
        <h2>{{ errorData }}</h2>
    </div>
    <div v-else class="mx-5 p-5" style="display: flex; align-items: center; justify-content: center;">
        <div style="max-width: 60%; text-align: center">
            <h2>{{ book.title }}</h2>
            <h4><i>{{ book.author }}</i></h4>
            <p v-if="book.content">{{ book.content }}</p>
            <p v-else>No content available</p>
        </div>
    </div>
    
</template>

<script>
import UserHeader from './UserHeader.vue';

export default {
    name: 'UserViewBook',
    components: {
        UserHeader,
    },
    data(){
        return {
            id: this.$route.params.id,
            errorData: "",
            book: {}
        }
    },
    mounted(){
        this.fetchData();
    },
    methods: {
        fetchData(){
            const myHeaders = new Headers();
            myHeaders.append("Authorization", "Bearer " + localStorage.getItem('user_token'));

            const requestOptions = {
                method: "GET",
                headers: myHeaders,
                redirect: "follow"
            };

            fetch("http://localhost:5000/fetch_book/" + this.id, requestOptions)
                .then(response => {
                    if (response.status === 200) {
                        return response.json();
                    } else if (response.status === 404) {
                        throw new Error("Book not found!");
                    } else if (response.status === 401) {
                        window.alert("Session expired. Please login again.");
                        this.logout();
                    } else if (response.status === 403){
                        throw new Error("Forbidden!");
                    } else {
                        throw new Error("Book not found!");
                    }
                })
                .then(data => {
                    this.book = data.Book;
                })
                .catch(error => {
                    errorData = error.message;
                });
        },
        logout() {
            localStorage.removeItem('user_token');
            this.isUserLoggedIn = false;
            window.location.href = '/login';
        },
    }

}
</script>