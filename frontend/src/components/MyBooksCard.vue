<template>
    <div class="card">
        <div class="card-body d-flex justify-content-between">
            <div class="fs-6" v-if="category == 'borrowed'">
                {{ title }}  | <i>by {{ author }}</i>  
            </div>
            <div class="fs-6" v-else>
                {{ title }}  |  <i>by {{ author }}</i>  |  {{ section }}
            </div>

            <div class="d-flex gap-2">
                <button v-if="category == 'approvalPending'" class="btn btn-danger" @click="cancelRequestHandler">Cancel Request</button>
                <p v-if="category == 'borrowed' || category == 'returned'" style="color: red;">{{ convert_date(returnDate) }}</p>
                <button v-if="category == 'borrowed'" class="btn btn-warning" @click="returnBookHandler">Return</button>
                <button v-if="category == 'returned'" class="btn btn-primary">View</button>
            </div>
            
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
            req_id: Number,
            returnDate: String
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
            },
            convert_date(dateString){
                const date = new Date(dateString);
                const formattedDate = date.toLocaleDateString();
                return formattedDate

            },
        }
    };
</script>