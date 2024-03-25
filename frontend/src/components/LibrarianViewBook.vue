<template>
    <LibrarianHeader @search_section="search_section"/>
    
    <div class="container pt-5">
        <h3 class="pb-4">{{ section }}</h3>
        <div class="row"  v-if="books.length">
            <div class="col-md-3 mb-3" v-for="book in books" :key="book.id">
                <LibrarianSectionBookCard :book="book" @logout="logout" @borrowed="borrowed"/>
            </div>
        </div>
        <div class="d-flex justify-content-center align-items-center" v-else>
            <h2>No books found!</h2>
        </div>
    </div>
</template>

<script>
import LibrarianHeader from './LibrarianHeader.vue';
import LibrarianSectionBookCard from './LibrarianSectionBookCard.vue';

export default{
    name: 'LibrarianViewBook',
    components: {
        LibrarianHeader,
        LibrarianSectionBookCard
    },
    data(){
        return{
            books: [],
            original_books: [],
            section: '',
            searchQuery: ''
        };
    },
    created() {
        // Check if parameter exists
        if (this.$route.query.section !== undefined) {
            this.section = this.$route.query.section;
        }

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

            fetch(`http://localhost:5000/librarian/list_books_in_section?section=${this.section}`, requestOptions)
            .then((response) => {
                if (response.status === 200) {
                    return (response.json())
                } else if (response.status === 401) {
                    window.alert('Token is expired, please login again!');
                    this.logout();
                } else if (response.status === 500) {
                    window.alert('Internal server error');
                } else {
                    window.alert('Unexpected status code:', response.status);
                }
            })
            .then((result) => {
                this.books = result.books;
                this.original_books = result.books;
            })
            .catch((error) => console.log('error', error));
        },
        logout(){
            localStorage.removeItem('user_token');
            this.isUserLoggedIn = false;
            window.location.href = '/login';
        },
        search_section(query){
            this.searchQuery = query;
            
            if (this.searchQuery === ''){
                this.books = this.original_books;
            } else {
                this.books = this.original_books.filter(book => book.title.toLowerCase().includes(this.searchQuery.toLowerCase()));
            }
        },
    }
    
}

</script>