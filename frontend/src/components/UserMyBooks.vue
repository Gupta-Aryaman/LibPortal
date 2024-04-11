<template>
    <UserHeader @search_book="search_book"/>

    <div class="container pt-5">

        <div>
            <h3>Approval Pending</h3>
            <div class="mt-2" v-if="approval_pending_books.length > 0" v-for="book in approval_pending_books" :key="book.id">
                <MyBooksCard :title="book.title" :author="book.author" :section="book.section" :category="'approvalPending'" :req_id="book.req_id" @cancelled="fetchData"/>
            </div>  
            <div class="d-flex justify-content-center align-items-center" v-else>
                <h4>No books found!</h4>
            </div>
        </div>
        
        <br> <br>

        <div>
            <h3>Borrowed</h3>
 
            <div class="mt-2" v-if="borrowed_books.length > 0" v-for="book in borrowed_books" :key="book.id">
                <MyBooksCard :book_id="book.book_id" :title="book.title" :author="book.author" :section="book.section" :returnDate="book.scheduled_return_date" :category="'borrowed'" :req_id="book.req_id" @returned="fetchData"/>
            </div>  
            <div class="d-flex justify-content-center align-items-center" v-else>
                <h4>No books found!</h4>
            </div>
        </div>

        <br> <br>

        <div>
            <h3>Returned/Revoked</h3>

            <div class="mt-2" v-if="returned_books.length > 0" v-for="book in returned_books" :key="book.id">
                <MyBooksCard :book_id="book.book_id" :title="book.title" :author="book.author" :section="book.section" :category="'returned'" :req_id="book.req_id" :returnDate="book.actual_return_date" :feedback="book.feedback"/>
            </div>  
            <div class="d-flex justify-content-center align-items-center" v-else>
                <h4>No books found!</h4>
            </div>
        </div>
        
    </div>
    
</template>

<script>
    import UserHeader from './UserHeader.vue';
    import MyBooksCard from './MyBooksCard.vue';

    export default {
        name: 'UserMyBooks',
        components: {
            UserHeader,
            MyBooksCard
        },
        data() {
            return {
                showOverflow: false, 
                approval_pending_books: [],
                borrowed_books: [],
                returned_books: [],
                original_approval_pending_books: [],
                original_borrowed_books: [],
                original_returned_books: [],
                queryString: '',
            };
        },
        created(){
            this.fetchData();
        },
        methods: {
            async fetchData() {
                try {
                    await Promise.all([
                        this.fetchApprovalPendingBooks(),
                        this.fetchBorrowedBooks(),
                        this.fetchReturnedBooks()
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

                fetch("http://localhost:5000/list_approval_pending_books", requestOptions)
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
                        this.approval_pending_books = result;
                        this.original_approval_pending_books = result;
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

                fetch("http://localhost:5000/list_borrowed_books", requestOptions)
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
                        this.borrowed_books = result;
                        this.original_borrowed_books = result;
                    })
                    .catch((error) => console.error(error));
            },
            async fetchReturnedBooks(){
                const myHeaders = new Headers();
                myHeaders.append("Authorization", "Bearer " + localStorage.getItem('user_token'));

                const requestOptions = {
                    method: "GET",
                    headers: myHeaders,
                    redirect: "follow"
                };

                fetch("http://localhost:5000/list_returned_books", requestOptions)
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
                        this.returned_books = result;
                        this.original_returned_books = result;
                    })
                    .catch((error) => console.error(error));
            },
            logout() {
                localStorage.removeItem('user_token');
                this.isUserLoggedIn = false;
                window.location.href = '/login';
            },
            search_book(query) {
                this.queryString = query;
                
                if (this.queryString === '') {
                    this.approval_pending_books = this.original_approval_pending_books;
                    this.borrowed_books = this.original_borrowed_books;
                    this.returned_books = this.original_returned_books;
                } else {
                    this.approval_pending_books = this.original_approval_pending_books.filter(book => (book.title.toLowerCase().includes(this.queryString.toLowerCase()) || book.section.toLowerCase().includes(this.queryString.toLowerCase())));
                    this.borrowed_books = this.original_borrowed_books.filter(book => (book.title.toLowerCase().includes(this.queryString.toLowerCase()) || book.section.toLowerCase().includes(this.queryString.toLowerCase())));
                    this.returned_books = this.original_returned_books.filter(book => (book.title.toLowerCase().includes(this.queryString.toLowerCase()) || book.section.toLowerCase().includes(this.queryString.toLowerCase())));
                }
            }
        }
    };
</script>