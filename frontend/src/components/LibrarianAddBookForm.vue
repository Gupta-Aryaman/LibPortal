<template class="">
    <!-- <LibrarianHeader /> -->
    <div class="vh-100 d-flex justify-content-center align-items-center">
        <form enctype="multipart/form-data" class="w-50 ">
            <h1 id="heading" v-if="isEdit==false">Add New Book</h1>
            <h1 id="heading" v-else>Edit Book</h1>
            <div class="form-group">
                <label class="form-label">Book Name<span class="text-danger">*</span></label>
                <input type="text" class="form-control" v-model="bookName" required>
            </div> <br>
            <div class="form-group">
                <label class="form-label">Author Name<span class="text-danger">*</span></label>
                <input type="text" class="form-control" v-model="authorName" required>
            </div> <br>
            <div class="form-group">
                <label class="form-label">Section Name<span class="text-danger">*</span></label>
                <input type="text" class="form-control" v-model="section" disabled>
            </div> <br>
            <div class="form-group">
                <label class="form-label">Available Copies<span class="text-danger">*</span></label>
                <input type="number" min="0" class="form-control" v-model="copies" oninput="validity.valid||(value='');" required>
            </div> <br>
            <div class="form-group">
                <label for="formFile" class="form-label">Choose picture</label>
                <input class="form-control" type="file" id="formFile" name="file" @change="handleFileUpload">
            </div> <br>
            <div class="form-group">
                <label for="exampleFormControlTextarea1" class="form-label">Description<span class="text-danger">*</span></label>
                <textarea class="form-control" id="exampleFormControlTextarea1" rows="3" name="desc" v-model="description"></textarea>
            </div>
            
            <br>
            <div class="form-group">
                <label for="content">Content</label>
                <textarea class="form-control" id="content" rows="3" name="content" v-model="content"></textarea>
            </div> <br>
            <button class="btn btn-primary" type="submit" @click="submitHandler($event)" :class="{'disabled': !isSubmitValid}">Submit form</button>
            <button class="btn btn-danger ms-2" @click="cancelHandler">Cancel</button>
        </form>
    </div>
</template>

<script>
import LibrarianHeader from './LibrarianHeader.vue';

export default {
    name: 'LibrarianAddBookForm',
    components: {
        LibrarianHeader
    },
    created() {
        if (localStorage.getItem('user_token') === null) {
            this.$router.push({ name: 'Login' });
        }
        if (this.$route.query.book_id !== undefined) {
            this.edit_book_id = this.$route.query.book_id;
            this.isEdit = true;
            this.fetchBook();
        }
        else if (this.$route.query.section !== undefined) {
            this.section = this.$route.query.section;
        }
    },
    data() {
        return {
            section: '',
            bookName: '',
            description: '',
            authorName: '',
            copies: 0,
            selectedFile: null,
            edit_book_id: '',
            isEdit: false,
            content: ''
        }
    },
    computed: {
        isSubmitValid() {
            return (this.bookName.length > 0 && this.description.length > 0 && this.authorName.length > 0 && this.copies > 0);
        }
    },
    methods: {
        cancelHandler() {
            this.$router.push('/librarian/dashboard');
        },
        submitHandler(event){
            event.preventDefault();

            const myHeaders = new Headers();
            myHeaders.append("Authorization", "Bearer " + localStorage.getItem('user_token'));

            if(this.isEdit == false){
                const formdata = new FormData();
                formdata.append("title", this.bookName);
                formdata.append("author", this.authorName);
                formdata.append("section", this.section);
                formdata.append("description", this.description);
                formdata.append("available_copies", this.copies);
                formdata.append("picture", this.selectedFile);
                formdata.append("content", this.content);

                const requestOptions = {
                    method: "POST",
                    headers: myHeaders,
                    body: formdata,
                    redirect: "follow"
                };

                fetch("http://localhost:5000/librarian/add_book", requestOptions)
                .then((response) => {
                    if (response.status === 200) {
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
                .then((result) => {
                    if (result !== undefined) {
                        window.alert('Book added successfully');
                        window.location.href = '/librarian/view_books?section=' + this.section;
                    }
                })
                .catch((error) => console.error(error));
            }
            else{
                const formdata = new FormData();
                formdata.append("title", this.bookName);
                formdata.append("author", this.authorName);
                formdata.append("description", this.description);
                formdata.append("available_copies", this.copies);
                formdata.append("picture", this.selectedFile);
                formdata.append("book_id", this.edit_book_id);
                formdata.append("content", this.content);

                const requestOptions = {
                    method: "PUT",
                    headers: myHeaders,
                    body: formdata,
                    redirect: "follow"
                };

                fetch(`http://localhost:5000/librarian/edit_book?book_id=${this.edit_book_id}`, requestOptions)
                .then((response) => {
                    if (response.status === 200) {
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
                .then((result) => {
                    if (result !== undefined) {
                        window.alert('Book edited successfully');
                        window.location.href = '/librarian/view_books?section=' + this.section;
                    }
                })
                .catch((error) => console.error(error));
            }
            

            

        },
        handleFileUpload(event) {
            this.selectedFile = event.target.files[0];
        },
        fetchBook() {
            const myHeaders = new Headers();
            myHeaders.append("Authorization", "Bearer " + localStorage.getItem('user_token'));

            const requestOptions = {
                method: "GET",
                headers: myHeaders,
                redirect: "follow"
            };

            fetch(`http://localhost:5000/librarian/get_edit_book?book_id=${this.edit_book_id}`, requestOptions)
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
                this.bookName = result.book.title;
                this.authorName = result.book.author;
                this.description = result.book.description;
                this.copies = result.book.available_copies;
                this.section = result.section;
                this.content = result.book.content;
            })
            .catch((error) => console.log('error', error));
        },
        logout(){
            localStorage.removeItem('user_token');
            this.isUserLoggedIn = false;
            window.location.href = '/login';
        }
    }
};
</script>
