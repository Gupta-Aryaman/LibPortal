<template>
    <div class="card" style="width: 18rem;">
        <div class="card-body p-3">
            <h5 class="card-title">{{ title }}</h5>
            <button v-if="description.length > 30" class="btn " @click="toggleOverflow">
                <p class="card-text description" :class="{ 'overflow-hidden': !showOverflow }"><i>{{ description }}</i></p>
            </button>
            <div class="text">
                <!-- <a class="card-text"><b>Copies <br>Available: {{ copies }}</b></a> -->
                <button class="btn btn-light m-2 " @click="viewBookHandler">View Books</button>
                <button class="btn btn-primary m-2 " @click="addBookHandler">Add Book</button>
            </div>

        </div>
    </div>
</template>

<script>
    export default {
        name: 'BookCard',
        props: {
            title: String,
            description: String
        },
        data() {
            return {
                showOverflow: false
            };
        },
        methods: {
            toggleOverflow() {
                this.showOverflow = !this.showOverflow;
            },
            addBookHandler() {
                // window.location.href = '/librarian/add-book'
            },
            viewBookHandler() {
                // window.location.href = '/librarian/view-books'
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

</style>