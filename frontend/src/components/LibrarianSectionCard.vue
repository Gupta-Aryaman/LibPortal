<template>
    <div class="card" style="width: 18rem;" :class="{'text-bg-danger': is_deleted}">
        <div class="card-body p-3" >
            <h1 class="card-title text-center"><b>{{ title }}</b></h1>
            <h6 class="card-subtitle mb-2 text-body-secondary text-center">Created On: {{ date }}</h6>
            <button v-if="description.length > 30" class="btn " @click="toggleOverflow">
                <p class="card-text description text-center" :class="{ 'overflow-hidden': !showOverflow }"><i>{{ description }}</i></p>
            </button>
            <div class="text" v-if="!is_deleted">
                <div>
                    <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="blue" class="btn bi bi-pencil-fill" viewBox="0 0 16 16" @click="editHandler">
                        <path d="M12.854.146a.5.5 0 0 0-.707 0L10.5 1.793 14.207 5.5l1.647-1.646a.5.5 0 0 0 0-.708zm.646 6.061L9.793 2.5 3.293 9H3.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.207zm-7.468 7.468A.5.5 0 0 1 6 13.5V13h-.5a.5.5 0 0 1-.5-.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.5-.5V10h-.5a.5.5 0 0 1-.175-.032l-.179.178a.5.5 0 0 0-.11.168l-2 5a.5.5 0 0 0 .65.65l5-2a.5.5 0 0 0 .168-.11z"/>
                    </svg>
                    <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="red" class="btn bi bi-trash3-fill" viewBox="0 0 16 16" @click="deleteHandler">
                        <path d="M11 1.5v1h3.5a.5.5 0 0 1 0 1h-.538l-.853 10.66A2 2 0 0 1 11.115 16h-6.23a2 2 0 0 1-1.994-1.84L2.038 3.5H1.5a.5.5 0 0 1 0-1H5v-1A1.5 1.5 0 0 1 6.5 0h3A1.5 1.5 0 0 1 11 1.5m-5 0v1h4v-1a.5.5 0 0 0-.5-.5h-3a.5.5 0 0 0-.5.5M4.5 5.029l.5 8.5a.5.5 0 1 0 .998-.06l-.5-8.5a.5.5 0 1 0-.998.06m6.53-.528a.5.5 0 0 0-.528.47l-.5 8.5a.5.5 0 0 0 .998.058l.5-8.5a.5.5 0 0 0-.47-.528M8 4.5a.5.5 0 0 0-.5.5v8.5a.5.5 0 0 0 1 0V5a.5.5 0 0 0-.5-.5"/>
                    </svg>
                </div>

                <div>
                    <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="currentColor" class="bi bi-folder2-open btn" viewBox="0 0 16 16" @click="viewBookHandler">
                        <path d="M1 3.5A1.5 1.5 0 0 1 2.5 2h2.764c.958 0 1.76.56 2.311 1.184C7.985 3.648 8.48 4 9 4h4.5A1.5 1.5 0 0 1 15 5.5v.64c.57.265.94.876.856 1.546l-.64 5.124A2.5 2.5 0 0 1 12.733 15H3.266a2.5 2.5 0 0 1-2.481-2.19l-.64-5.124A1.5 1.5 0 0 1 1 6.14zM2 6h12v-.5a.5.5 0 0 0-.5-.5H9c-.964 0-1.71-.629-2.174-1.154C6.374 3.334 5.82 3 5.264 3H2.5a.5.5 0 0 0-.5.5zm-.367 1a.5.5 0 0 0-.496.562l.64 5.124A1.5 1.5 0 0 0 3.266 14h9.468a1.5 1.5 0 0 0 1.489-1.314l.64-5.124A.5.5 0 0 0 14.367 7z"/>
                    </svg>
                    <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="currentColor" class="bi bi-file-earmark-plus-fill btn" viewBox="0 0 16 16" @click="addBookHandler">
                        <path d="M9.293 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V4.707A1 1 0 0 0 13.707 4L10 .293A1 1 0 0 0 9.293 0M9.5 3.5v-2l3 3h-2a1 1 0 0 1-1-1M8.5 7v1.5H10a.5.5 0 0 1 0 1H8.5V11a.5.5 0 0 1-1 0V9.5H6a.5.5 0 0 1 0-1h1.5V7a.5.5 0 0 1 1 0"/>
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
                    <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="currentColor" class="bi bi-folder2-open btn" viewBox="0 0 16 16" @click="viewBookHandler">
                        <path d="M1 3.5A1.5 1.5 0 0 1 2.5 2h2.764c.958 0 1.76.56 2.311 1.184C7.985 3.648 8.48 4 9 4h4.5A1.5 1.5 0 0 1 15 5.5v.64c.57.265.94.876.856 1.546l-.64 5.124A2.5 2.5 0 0 1 12.733 15H3.266a2.5 2.5 0 0 1-2.481-2.19l-.64-5.124A1.5 1.5 0 0 1 1 6.14zM2 6h12v-.5a.5.5 0 0 0-.5-.5H9c-.964 0-1.71-.629-2.174-1.154C6.374 3.334 5.82 3 5.264 3H2.5a.5.5 0 0 0-.5.5zm-.367 1a.5.5 0 0 0-.496.562l.64 5.124A1.5 1.5 0 0 0 3.266 14h9.468a1.5 1.5 0 0 0 1.489-1.314l.64-5.124A.5.5 0 0 0 14.367 7z"/>
                    </svg>
                </div>
                
                
            </div>

        </div>
    </div>
</template>

<script>
    export default {
        name: 'BookCard',
        props: {
            title: String,
            description: String,
            date: String,
            sec_id: Number,
            is_deleted: Boolean
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
                window.location.href = '/librarian/add_book?section=' + this.title
            },
            viewBookHandler() {
                window.location.href = '/librarian/view_books?section=' + this.title
            },
            editHandler() {
                window.location.href = '/librarian/add_section?edit_id=' + this.sec_id
            },
            deleteHandler() {
                
                if(window.confirm('Are you sure you want to delete this section?')){
                    const myHeaders = new Headers();
                    myHeaders.append("Content-Type", "application/json");
                    myHeaders.append("Authorization", "Bearer " + localStorage.getItem("user_token"));

                    const raw = JSON.stringify({
                        "section_id": this.sec_id,
                    });

                    const requestOptions = {
                        method: "DELETE",
                        headers: myHeaders,
                        body: raw,
                        redirect: "follow"
                    };

                    fetch("http://localhost:5000/librarian/delete_section", requestOptions)
                    .then((response) => {
                        if (response.status === 200) {
                            window.alert('Section deleted successfully');
                            this.$emit('delete_section', this.sec_id)
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
                

                // this.$emit('delete-section', this.sec_id)
            },
            restoreHandler(){
                const myHeaders = new Headers();
                myHeaders.append("Content-Type", "application/json");
                myHeaders.append("Authorization", "Bearer " + localStorage.getItem("user_token"));

                const raw = JSON.stringify({
                    "section_id": this.sec_id,
                });

                const requestOptions = {
                    method: "POST",
                    headers: myHeaders,
                    body: raw,
                    redirect: "follow"
                };

                fetch("http://localhost:5000/librarian/restore_section", requestOptions)
                .then((response) => {
                    if (response.status === 200) {
                        this.$emit('restore_section', this.sec_id)
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