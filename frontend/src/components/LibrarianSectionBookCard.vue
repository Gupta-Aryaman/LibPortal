<template>
    <div class="card" :class="{'text-bg-danger': book.is_deleted}" style="width: 18rem;">
        <div class="card-body p-3">
            <h5 class="card-title">{{ book.title }}</h5>
            <h6 class="card-subtitle mb-2 text-body-secondary">{{ book.author }}</h6>
            
            <p class="card-text description" v-if="!book.is_deleted">
                <b>Currently Issued By:</b>
                <div class="description" v-if="book.borrowed_by.length > 0" v-for="x in book.borrowed_by">
                    <p class="card-text" ><i>{{ x }}</i></p>
                </div>
                <div v-else>
                    <p class="card-text" ><i>None</i></p>
                </div>
            </p>

            <a class="" v-if="!book.is_deleted"><b>Copies Available: {{ book.available_copies }}</b></a>

            <div class="text" v-if="!book.is_deleted">
                <div>
                    <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="blue" class="btn bi bi-pencil-fill" viewBox="0 0 16 16" @click="editHandler">
                        <path d="M12.854.146a.5.5 0 0 0-.707 0L10.5 1.793 14.207 5.5l1.647-1.646a.5.5 0 0 0 0-.708zm.646 6.061L9.793 2.5 3.293 9H3.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.207zm-7.468 7.468A.5.5 0 0 1 6 13.5V13h-.5a.5.5 0 0 1-.5-.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.5-.5V10h-.5a.5.5 0 0 1-.175-.032l-.179.178a.5.5 0 0 0-.11.168l-2 5a.5.5 0 0 0 .65.65l5-2a.5.5 0 0 0 .168-.11z"/>
                    </svg>
                    
                </div>

                <div>
                    <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="red" class="btn bi bi-trash3-fill" viewBox="0 0 16 16" @click="deleteHandler">
                        <path d="M11 1.5v1h3.5a.5.5 0 0 1 0 1h-.538l-.853 10.66A2 2 0 0 1 11.115 16h-6.23a2 2 0 0 1-1.994-1.84L2.038 3.5H1.5a.5.5 0 0 1 0-1H5v-1A1.5 1.5 0 0 1 6.5 0h3A1.5 1.5 0 0 1 11 1.5m-5 0v1h4v-1a.5.5 0 0 0-.5-.5h-3a.5.5 0 0 0-.5.5M4.5 5.029l.5 8.5a.5.5 0 1 0 .998-.06l-.5-8.5a.5.5 0 1 0-.998.06m6.53-.528a.5.5 0 0 0-.528.47l-.5 8.5a.5.5 0 0 0 .998.058l.5-8.5a.5.5 0 0 0-.47-.528M8 4.5a.5.5 0 0 0-.5.5v8.5a.5.5 0 0 0 1 0V5a.5.5 0 0 0-.5-.5"/>
                    </svg>
                </div>
                
            </div>

            <div class="text" v-else>
                <div>
                    <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="currentColor" class="bi bi-arrow-counterclockwise btn" viewBox="0 0 16 16" @click="restoreHandler">
                        <path fill-rule="evenodd" d="M8 3a5 5 0 1 1-4.546 2.914.5.5 0 0 0-.908-.417A6 6 0 1 0 8 2z"/>
                        <path d="M8 4.466V.534a.25.25 0 0 0-.41-.192L5.23 2.308a.25.25 0 0 0 0 .384l2.36 1.966A.25.25 0 0 0 8 4.466"/>
                    </svg>
                </div>
                <div>

                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default{
    name: 'LibrarianSectionBookCard',
    props: {
        book: Object
    },
    data(){
        return{
            showOverflow: false
        };
    },
    methods: {
        toggleOverflow() {
            this.showOverflow = !this.showOverflow;
        },
        editHandler(){
            window.location.href = `/librarian/add_book?book_id=${this.book.book_id}`;
        },
        deleteHandler(){
            if(window.confirm('Are you sure you want to delete this book?')){
                const myHeaders = new Headers();
                myHeaders.append("Content-Type", "application/json");
                myHeaders.append("Authorization", "Bearer " + localStorage.getItem("user_token"));

                const raw = JSON.stringify({
                    "book_id": this.book.book_id,
                });

                const requestOptions = {
                    method: "DELETE",
                    headers: myHeaders,
                    body: raw,
                    redirect: "follow"
                };

                fetch("http://localhost:5000/librarian/delete_book", requestOptions)
                .then((response) => {
                    if (response.status === 200) {
                        window.alert('Book deleted successfully');
                        this.$emit('delete_book', this.book.book_id)
                        return (response.json())
                    } else if (response.status === 401) {
                        window.alert('Token is expired, please login again!');
                        this.logout();
                    } else if (response.status === 500) {
                        window.alert('Internal server error');
                    } else if(response.status === 400) {
                        window.alert('Invalid Input:', response.status);
                    } else if(response.status === 404) {
                        window.alert('Section not found:', response.status);
                    }
                })
                .catch((error) => console.error(error));
            }
                
        },
        restoreHandler(){
            const myHeaders = new Headers();
            myHeaders.append("Content-Type", "application/json");
            myHeaders.append("Authorization", "Bearer " + localStorage.getItem("user_token"));

            const raw = JSON.stringify({
                "book_id": this.book.book_id,
            });

            const requestOptions = {
                method: "POST",
                headers: myHeaders,
                body: raw,
                redirect: "follow"
            };

            fetch("http://localhost:5000/librarian/restore_book", requestOptions)
            .then((response) => {
                if (response.status === 200) {
                    window.alert('Book restored successfully');
                    this.$emit('delete_book', this.book.book_id)
                    return (response.json())
                } else if (response.status === 401) {
                    window.alert('Token is expired, please login again!');
                    this.logout();
                } else if (response.status === 500) {
                    window.alert('Internal server error');
                } else if(response.status === 400) {
                    window.alert('Invalid Input:', response.status);
                } else if(response.status === 404) {
                    window.alert('Section not found:', response.status);
                }
            })
            .catch((error) => console.error(error));
        
        },
        logout() {
            localStorage.removeItem('user_token');
            this.isUserLoggedIn = false;
            window.location.href = '/login';
        },
    }
}
</script>

<style scoped>
    .text {
        display: flex;
        justify-content: space-between;
    }

</style>