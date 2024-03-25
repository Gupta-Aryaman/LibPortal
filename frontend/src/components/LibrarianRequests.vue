<template>
    <LibrarianHeader @search_section="search_section" />

    <div class="container pt-5">

        <div>
            <h3>Approval Pending</h3>
            <div class="mt-2" v-if="approval_pending_books.length > 0" v-for="book in approval_pending_books">
                <LibrarianRequestCard :book="book" :category="'approvalPending'" @reject="rejectSuccess" @approve = "approveSuccess"/>
            </div>  
            <div class="d-flex justify-content-center align-items-center" v-else>
                <h4>No books found!</h4>
            </div>
        </div>

        <br> <br>

        <div>
            <h3>Borrowed</h3>

            <div class="mt-2" v-if="borrowed_books.length > 0" v-for="book in borrowed_books">
                <LibrarianRequestCard :book="book" :category="'borrowed'" @revoke="revokeSuccess"/>
            </div>  
            <div class="d-flex justify-content-center align-items-center" v-else>
                <h4>No books found!</h4>
            </div>
        </div>

    </div>
    
</template>

<script>
import LibrarianHeader from './LibrarianHeader.vue';
import LibrarianRequestCard from './LibrarianRequestCard.vue';

export default{
    name: 'LibrarianRequests',
    components: {
        LibrarianHeader,
        LibrarianRequestCard
    },
    data() {
        return {
            searchQuery: '',
            approval_pending_books: [],
            borrowed_books: [],
            original_approval_pending_books: [],
            original_borrowed_books: []
        }
    },
    created() {
        if (localStorage.getItem('user_token') === null) {
            this.$router.push({ name: 'Login' });
        }
        this.fetchData();
    },
    methods: {
        search_section(query) {
            this.searchQuery = query;
            
            if (query === '') {
                this.approval_pending_books = this.original_approval_pending_books;
                this.borrowed_books = this.original_borrowed_books;
            } else {
                this.approval_pending_books = this.original_approval_pending_books.filter((book) => {
                    return book.title.toLowerCase().includes(query.toLowerCase()) || book.email.toLowerCase().includes(query.toLowerCase());
                });
                this.borrowed_books = this.original_borrowed_books.filter((book) => {
                    return book.title.toLowerCase().includes(query.toLowerCase()) || book.email.toLowerCase().includes(query.toLowerCase());
                });
            }
        },
        async fetchData() {
            try {
                await Promise.all([
                    this.fetchApprovalPendingBooks(),
                    this.fetchBorrowedBooks(),
                ]);
            } catch (error) {
                console.error(error);
            }
        },
        async fetchApprovalPendingBooks(){
            const myHeaders = new Headers();
            myHeaders.append("Authorization", "Bearer " + localStorage.getItem('user_token'));

            const requestOptions = {
                method: "GET",
                headers: myHeaders,
                redirect: "follow"
            };

            fetch("http://localhost:5000/librarian/list_pending_approval_books", requestOptions)
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
                this.approval_pending_books = result.Books;
                this.original_approval_pending_books = result.Books;
            })
            .catch((error) => console.error(error));
        },
        async fetchBorrowedBooks(){
            const myHeaders = new Headers();
            myHeaders.append("Authorization", "Bearer " + localStorage.getItem('user_token'));

            const requestOptions = {
                method: "GET",
                headers: myHeaders,
                redirect: "follow"
            };

            fetch("http://localhost:5000/librarian/list_borrowed_books_librarian", requestOptions)
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
                this.borrowed_books = result.Books;
                this.original_borrowed_books = result.Books;
            })
            .catch((error) => console.error(error));
        },
        logout() {
            localStorage.removeItem('user_token');
            this.isUserLoggedIn = false;
            window.location.href = '/login';
        },
        rejectSuccess(req_id){
            window.alert('Request rejected successfully');
            this.fetchData();
        },
        approveSuccess(req_id){
            window.alert('Request approved successfully');
            this.fetchData();
        },
        revokeSuccess(book_id){
            window.alert('Book revoked successfully');
            this.fetchData();
        }
    }
}
</script>