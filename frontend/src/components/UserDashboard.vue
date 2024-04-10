<template>
    <UserHeader @search_book="search_book"/>

    <div class="container pt-5">
        <div class="row"  v-if="books.length">
            <div class="col-md-3 mb-3" v-for="book in books" :key="book.id">
                <BookCard :feedback="book.feedback" :title="book.title" :author="book.author" :section="book.section" :description="book.description" :copies="book.available_copies" :isBorrowed="book.is_borrowed" :bookId="book.id" :picturePath="book.image" @logout="logout" @borrowed="borrowed"/>
            </div>
        </div>
        <div class="d-flex justify-content-center align-items-center" v-else>
            <h2>No books found!</h2>
        </div>
    </div>

    
    
    
    
</template>

<script>
    import UserHeader from './UserHeader.vue';
    import BookCard from './BookCard.vue';
    import { useRoute } from 'vue-router'

    export default {
        name : 'UserDashboard',
        components: {
            UserHeader,
            BookCard
        },
        mounted() {
            if (localStorage.getItem('user_token') && localStorage.getItem('user')) {
                this.isUserLoggedIn = true;
                this.username = localStorage.getItem('user');
            } else{
                this.logout();
            }
        },
        data() {
            return {
                books: [],
                original_books: [],
                queryString: '',
                isSection: false,
                isTitle: false,
            };
        },
        created() {
            // Check if parameter exists
            // if (this.$route.query.section !== undefined) {
            //     this.isSection = true;
            //     this.queryString = this.$route.query.section;
            // } else if(this.$route.query.title !== undefined) {
            //     this.isTitle = true;
            //     this.queryString = this.$route.query.title;
            // }

            this.fetchBooks();
        },
        methods: {
            async fetchBooks() {
                const myHeaders = new Headers();
                myHeaders.append("Authorization", "Bearer " + localStorage.getItem('user_token'));

                const requestOptions = {
                    method: "GET",
                    headers: myHeaders,
                    redirect: "follow"
                };

                console.log(this.queryString);
                
                

                fetch("http://localhost:5000/list_books", requestOptions)
                .then((response) => {
                    if (response.status === 200) {
                        return response.json();
                    } else if (response.status === 401) {
                        window.alert("Session expired. Please login again.");
                        this.logout();
                    } else {
                        window.alert("An error occurred. Please try again later.");
                    }
                })
                .then((result) => {
                    result = result.Books;
                    this.books = result;
                    this.original_books = result;
                })
                .catch((error) => console.error(error));
                

                
            },
            borrowed(){
                window.alert('Book borrowed successfully');
                this.fetchBooks();
            },
            logout() {
                localStorage.removeItem('user_token');
                this.isUserLoggedIn = false;
                window.location.href = '/login';
            },
            search_book(query){
                this.queryString = query;
                
                if (query === '') {
                    this.books = this.original_books;
                } else {
                    this.books = this.original_books.filter(book => (book.title.toLowerCase().includes(query.toLowerCase()) || book.section.toLowerCase().includes(query.toLowerCase())));
                }
            }
        }
    }

</script>