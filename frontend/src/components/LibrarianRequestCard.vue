<template>
    <div class="card">
        <div class="card-body d-flex justify-content-between">
            <div class="fs-6" v-if="category == 'approvalPending'">
                {{ book.title }}  <b>|</b> {{ book.email }}
            </div>
            <div class="fs-6" v-else>
                {{ book.title }}  <b>|</b> {{ book.email }} <b>|</b> Scheduled Return Date: {{ convert_date(book.scheduled_return_date) }}
            </div>
            <div class="d-flex gap-2">
                <button v-if="category == 'approvalPending'" class="btn btn-success" @click="approveHandler">Approve</button>
                <button v-if="category == 'approvalPending'" class="btn btn-danger" @click="rejectHandler">Reject</button>
                <button v-if="category == 'borrowed'" class="btn btn-warning" @click="revokeHandler">Revoke</button>
            </div>
            
        </div>
    </div>
</template>

<script>
    export default {
        name: 'LibrarianRequestCard',
        props: {
            book: Object,
            category: String
        },
        methods: {
            convert_date(dateString){
                const date = new Date(dateString);
                const formattedDate = date.toLocaleDateString();
                return formattedDate

            },
            approveHandler(){
                const myHeaders = new Headers();
                myHeaders.append("Content-Type", "application/json");
                myHeaders.append("Authorization", "Bearer " + localStorage.getItem("user_token"));

                const raw = JSON.stringify({
                    "user_id": this.book.user_id,
                    "book_id": this.book.book_id,
                    "req_id": this.book.req_id,
                });

                const requestOptions = {
                    method: "POST",
                    headers: myHeaders,
                    body: raw,
                    redirect: "follow"
                };

                fetch("http://localhost:5000/librarian/approve_book_borrow", requestOptions)
                .then((response) => {
                    if (response.status === 200) {
                        this.$emit('approve', this.book.req_id);
                    } else if (response.status === 401) {
                        window.alert('Token is expired, please login again!');
                        this.logout();
                    } else if (response.status === 500) {
                        window.alert('Internal server error');
                        return;
                    } else if (response.status === 403) {
                        window.alert('User already has 5 borrowed books');
                        return;
                    } else if (response.status === 404) {
                        window.alert('No copies of the book available for borrowing');
                        return;
                    } else {
                        window.alert('Unexpected status code:', response.status);
                        return;
                    }
                })
                .catch((error) => console.error(error));
            },
            rejectHandler(){
                const myHeaders = new Headers();
                myHeaders.append("Content-Type", "application/json");
                myHeaders.append("Authorization", "Bearer " + localStorage.getItem("user_token"));

                const raw = JSON.stringify({
                    "req_id": this.book.req_id,
                });

                const requestOptions = {
                    method: "POST",
                    headers: myHeaders,
                    body: raw,
                    redirect: "follow"
                };

                fetch("http://localhost:5000/librarian/reject_book_borrow", requestOptions)
                .then((response) => {
                    if (response.status === 200) {
                        this.$emit('reject', this.book.req_id);
                    } else if (response.status === 401) {
                        window.alert('Token is expired, please login again!');
                        this.logout();
                    } else if (response.status === 500) {
                        window.alert('Internal server error');
                        return;
                    } else {
                        window.alert('Unexpected status code:', response.status);
                        return;
                    }
                })
                .catch((error) => console.error(error));

            },
            revokeHandler(){
                const myHeaders = new Headers();
                myHeaders.append("Content-Type", "application/json");
                myHeaders.append("Authorization", "Bearer " + localStorage.getItem("user_token"));

                const raw = JSON.stringify({
                    "req_id": this.book.req_id,
                    "book_id": this.book.book_id,
                });

                const requestOptions = {
                    method: "POST",
                    headers: myHeaders,
                    body: raw,
                    redirect: "follow"
                };

                fetch("http://localhost:5000/librarian/revoke_borrowed_book", requestOptions)
                .then((response) => {
                    if (response.status === 200) {
                        this.$emit('revoke', this.book.req_id);
                    } else if (response.status === 401) {
                        window.alert('Token is expired, please login again!');
                        this.logout();
                    } else if (response.status === 500) {
                        window.alert('Internal server error');
                        return;
                    } else {
                        window.alert('Unexpected status code:', response.status);
                        return;
                    }
                })
                .catch((error) => console.error(error));
            }
        }
    };
</script>