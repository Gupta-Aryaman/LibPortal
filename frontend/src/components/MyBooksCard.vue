<template>
    <div class="card">
        <div class="card-body d-flex justify-content-between">
            <div class="fs-6">
                {{ title }}  |  {{ author }}  |  {{ section }}
            </div>
            <button v-if="category == 'approvalPending'" class="btn btn-danger" @click="cancelRequestHandler">Cancel Request</button>
            <button v-if="category == 'borrowed'" class="btn btn-warning" @click="returnBookHandler">Return</button>
            <button v-if="category == 'returned'" class="btn btn-primary">View</button>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'MyBooksCard',
        props: {
            title: String,
            author: String,
            section: String,
            category: String,
            req_id: Number
        },
        methods: {
            cancelRequestHandler() {
                const myHeaders = new Headers();
                myHeaders.append("Content-Type", "application/json");
                myHeaders.append("Authorization", "Bearer " + localStorage.getItem("user_token"));

                const raw = JSON.stringify({
                    "req_id": this.req_id
                });

                const requestOptions = {
                    method: "DELETE",
                    headers: myHeaders,
                    body: raw,
                    redirect: "follow"
                };

                fetch("http://localhost:5000/cancel_borrow_request", requestOptions)
                .then((response) => {
                    if (response.status === 200) {
                        this.$emit('cancelled');
                    } else if (response.status === 401) {
                        alert("Token expired! Please login again.");
                        this.$emit('logout');
                    } else if (response.status === 500) {
                        alert("Internal server error");
                    }
                })
                .catch((error) => console.error(error));

            },
            returnBookHandler() {
                const myHeaders = new Headers();
                myHeaders.append("Content-Type", "application/json");
                myHeaders.append("Authorization", "Bearer " + localStorage.getItem("user_token"));

                const raw = JSON.stringify({
                    "req_id": this.req_id
                });

                const requestOptions = {
                method: "POST",
                headers: myHeaders,
                body: raw,
                redirect: "follow"
                };

                fetch("http://localhost:5000/return_book", requestOptions)
                .then((response) => {
                    if (response.status === 200) {
                        this.$emit('returned');
                    } else if (response.status === 401) {
                        alert("Token expired! Please login again.");
                        this.$emit('logout');
                    } else if (response.status === 500) {
                        alert("Internal server error");
                    }
                })
                .catch((error) => console.error(error));
            }
        }
    };
</script>