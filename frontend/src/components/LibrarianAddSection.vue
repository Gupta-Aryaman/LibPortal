<template>
    <LibrarianHeader />
    <!-- <form >
        <div class="form-group">
            <label for="exampleFormControlTextarea1">Description</label>
            <textarea class="form-control" id="exampleFormControlTextarea1" rows="3"></textarea>
        </div>
    </form> -->

    <div class="col-lg-8 m-auto d-block">
    <form style="padding-top: 200px;">
        <h1 v-if="!is_edit">New Section</h1>
        <h1 v-else>Edit Section</h1>
          
        <div class="form-group">
            <label class="form-label">Section Name<span class="text-danger">*</span></label>
            <input type="text" class="form-control" v-model="sectionName" :class="{'is-invalid': !isSectionValid}" required>
            <div class="invalid-feedback" v-if="!isSectionValid">
                Section name already exists.
            </div>
        </div>
          
        <br>
          
        <div class="form-group">
            <label for="exampleFormControlTextarea1" class="form-label">Description<span class="text-danger">*</span></label>
            <textarea class="form-control" id="exampleFormControlTextarea1" rows="3" name="desc" v-model="description"></textarea>
        </div>
        
        <br>
        <button v-if="!this.edit_id" class="btn btn-primary" @click="submitHandler($event)" :class="{'disabled': !isSubmitValid}">Submit</button>
        <button v-else class="btn btn-primary" @click="submitEditHandler($event)" :class="{'disabled': !isSubmitValid}">Submit</button>
      </form>
    </div>
</template>

<script>
import LibrarianHeader from './LibrarianHeader.vue';

export default{
    name: 'LibrarianAddSection',
    components: {
        LibrarianHeader
    },
    created(){
        if (this.$route.query.edit_id !== undefined) {
            this.edit_id = this.$route.query.edit_id;
            this.is_edit = true;
            this.fetchSections();
        }
        else{
            this.fetchSections();
        }
        
    },
    data(){
        return{
            sectionName: '',
            description: '',
            sections: [],
            edit_id: '',
            is_edit: false
        };
    },
    computed: {
        isSectionValid(){
            for (let i = 0; i < this.sections.length; i++) {
                if (this.sections[i].section == this.sectionName) {
                    // console.log('Section already exists');
                    return false;
                }
            } return true;
        },
        isSubmitValid(){
            return (this.isSectionValid && this.sectionName.length > 0 && this.description.length > 0);
        }
    },
    methods: {
        submitHandler(event){
            event.preventDefault();
            
            const myHeaders = new Headers();
            myHeaders.append("Content-Type", "application/json");
            myHeaders.append("Authorization", "Bearer " + localStorage.getItem('user_token'));

            const raw = JSON.stringify({
                "section": this.sectionName,
                "description": this.description
            });

            const requestOptions = {
                method: "POST",
                headers: myHeaders,
                body: raw,
                redirect: "follow"
            };

            fetch("http://localhost:5000/librarian/add_section", requestOptions)
            .then((response) => {
                if (response.status === 200) {
                    return (response.json())
                } else if (response.status === 401) {
                    window.alert('Token expired, please login again!');
                    this.logout();
                } else if (response.status === 500) {
                    window.alert('Internal server error');
                } else {
                    window.alert('Unexpected status code:', response.status);
                }
            })
            .then((result) => {
                if (result) {
                    window.alert('Section added successfully!');
                    setTimeout(() => {
                        window.location.href = '/librarian/dashboard';
                    }, 500);
                }
            })
            .catch((error) => console.error(error));
        },
        submitEditHandler(event){
            event.preventDefault();
            
            const myHeaders = new Headers();
            myHeaders.append("Content-Type", "application/json");
            myHeaders.append("Authorization", "Bearer " + localStorage.getItem('user_token'));

            const raw = JSON.stringify({
                "section": this.sectionName,
                "description": this.description,
                "section_id": this.edit_id
            });

            const requestOptions = {
                method: "POST",
                headers: myHeaders,
                body: raw,
                redirect: "follow"
            };

            fetch("http://localhost:5000/librarian/edit_section", requestOptions)
            .then((response) => {
                if (response.status === 200) {
                    return (response.json())
                } else if (response.status === 401) {
                    window.alert('Token expired, please login again!');
                    this.logout();
                } else if(response.status === 404) {
                    window.alert('Section not found.');
                }
                else if (response.status === 500) {
                    window.alert('Internal server error');
                } else {
                    window.alert('Unexpected status code:', response.status);
                }
            })
            .then((result) => {
                if (result) {
                    window.alert('Section edited successfully!');
                    setTimeout(() => {
                        window.location.href = '/librarian/dashboard';
                    }, 500);
                }
            })
            .catch((error) => console.error(error));

        },
        fetchSections(){
            const myHeaders = new Headers();
            myHeaders.append("Authorization", "Bearer " + localStorage.getItem('user_token'));

            const requestOptions = {
                method: "GET",
                headers: myHeaders,
                redirect: "follow"
            };

            fetch("http://localhost:5000/librarian/list_sections", requestOptions)
            .then((response) => {
                if (response.status === 200) {
                    return (response.json())
                } else if (response.status === 401) {
                    window.alert('Token expired, please login again!');
                    this.logout();
                } else if (response.status === 500) {
                    window.alert('Internal server error');
                } else {
                    window.alert('Unexpected status code:', response.status);
                }
            })
            .then((result) => {
                if (result) {
                    this.sections = result.Sections;
                }
                if (this.is_edit){
                    this.fetchExistingSection();
                }
            })
            .catch((error) => console.error(error));
        },
        fetchExistingSection(){
            for (let i = 0; i < this.sections.length; i++) {
                if (this.sections[i].id == this.edit_id) {
                    this.sectionName = this.sections[i].section;
                    this.description = this.sections[i].description;
                    console.log(this.sectionName, this.description);
                    this.sections.splice(i, 1);
                    break;
                }
            }
        },
        logout(){
            localStorage.removeItem('user_token');
            this.isUserLoggedIn = false;
            window.location.href = '/login';
        },
    }

}
</script>