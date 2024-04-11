<template>
    <div class="card" style="width: 18rem;">
        <img v-if="picturePath" :src="'/images/' + picturePath" class="card-img-top">
        <img v-else src="https://via.placeholder.com/150" class="card-img-top" alt="...">
        <div class="card-body p-3">
            <h5 class="card-title">{{ title }}</h5>
            <h6 class="card-subtitle mb-2 text-body-secondary">{{ author }} - {{ section }}</h6>
            <button v-if="description.length > 30" class="btn " @click="toggleOverflow">
                <p class="card-text description" :class="{ 'overflow-hidden': !showOverflow }"><i>{{ description }}</i></p>
            </button>
            <div class="text">
                <a class="card-text"><b>Copies <br>Available: {{ copies }}</b></a>
                <button class="btn btn-primary m-2 req_button" :class="{'disabled': copies == 0 || isBorrowed}" v-on:click="borrow">Request</button>
            </div>
            <div>
                <span v-for="index in 5" :class="{ 'filled_star': index <= this.feedback }" class="star">★</span>
            </div>

        </div>
    </div>
</template>

<script>
    export default {
        name: 'BookCard',
        props: {
            title: String,
            section: String,
            author: String,
            description: String,
            copies: Number, 
            isBorrowed: Boolean,
            bookId: Number,
            picturePath: String,
            feedback: Number
        },
        data() {
            return {
                showOverflow: false,
                // icon: L.icon(),
            };
        },
        created() {
            // this.icon = L.icon({
            //     iconUrl: this.picturePath,
            //     iconSize: [50, 50],
            //     iconAnchor: [25, 25],
            //     popupAnchor: [0, -25],
            // });
        },
        methods: {
            toggleOverflow() {
                this.showOverflow = !this.showOverflow;
            },
            borrow() {
                const myHeaders = new Headers();
                myHeaders.append("Content-Type", "application/json");
                myHeaders.append("Authorization", "Bearer " + localStorage.getItem("user_token"));

                const raw = JSON.stringify({
                    "book_id": this.bookId
                });

                const requestOptions = {
                method: "POST",
                headers: myHeaders,
                body: raw,
                redirect: "follow"
                };

                fetch("http://localhost:5000/borrow_book", requestOptions)
                .then((response) => {
                    if (response.status === 200) {
                        this.$emit('borrowed');
                        this.isBorrowed = true;
                    } else if (response.status === 401) {
                        alert("You are not authorized to borrow books");
                        this.$emit('logout');
                    } else if (response.status === 403) {
                        alert("Book not available!");
                    } else if (response.status === 500) {
                        alert("Internal server error");
                    }
                })
                .catch((error) => console.error(error));
            
            
            }
        }
    };

</script>

<style scoped>
    .text {
        display: flex;
        justify-content: space-between;
    }
    .overflow-hidden {
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 4; /* Number of lines to show before truncating */
        -webkit-box-orient: vertical;
    }
    .description {
        text-align: left;
    }
    .filled_star {
        color: rgb(255, 106, 0);
    }
    .star {
        font-size: 2vh;
        cursor:default;
    }

</style>