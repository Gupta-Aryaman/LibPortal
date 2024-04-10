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
                
                <div class="card-star" v-if="category == 'returned'">
                    <div class="card-star" v-if="category == 'returned'" ref="stars">
                        <span v-for="index in 5" :key="index" @click="gfg_update(index)" :class="{ 'filled_star': index <= feedback }" class="star">★</span>
                    </div>
                </div>
                               
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
            returnDate: String,
            book_id: Number,
            feedback: Number
        },
        data(){
            return {
                stars: [],
                output: [],
                cls: ""
            }
        },
        mounted(){
            if(this.category == 'returned'){
                this.stars = this.$refs.stars.getElementsByClassName("star");
                this.cls = "";
            }
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

            gfg_update(n){
                this.remove();
                for (let i = 0; i < n; i++) {
                    if (n == 1) this.cls = "filled_star";
                    else if (n == 2) this.cls = "filled_star";
                    else if (n == 3) this.cls = "filled_star";
                    else if (n == 4) this.cls = "filled_star";
                    else if (n == 5) this.cls = "filled_star";
                    this.stars[i].className = "star " + this.cls;
                }

                const myHeaders = new Headers();
                myHeaders.append("Content-Type", "application/json");
                myHeaders.append("Authorization", "Bearer " + localStorage.getItem('user_token'));

                const raw = JSON.stringify({
                    "book_id": this.book_id,
                    "feedback": n
                });

                const requestOptions = {
                    method: "POST",
                    headers: myHeaders,
                    body: raw,
                    redirect: "follow"
                };

                fetch("http://localhost:5000/add_feedback", requestOptions)
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
                    if(result === "Feedback submitted successfully"){
                        window.alert("Rating submitted successfully")
                    }
                })
                .catch((error) => console.error(error));
            },
            remove() {
                let i = 0;
                while (i < 5) {
                    this.stars[i].className = "star";
                    i++;
                }
            },
            logout() {
                localStorage.removeItem('user_token');
                this.isUserLoggedIn = false;
                window.location.href = '/login';
            },
        }
    };
</script>

<style>
.card-star{
    max-width: 33rem;
  margin: 0 1rem;
  width: 100%;
}

.star {
  font-size: 3vh;
  cursor: pointer;
}

.filled_star {
    color: rgb(255, 106, 0);
}

</style>