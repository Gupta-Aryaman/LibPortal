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
        <h1>New Section</h1>
          
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
        <button class="btn btn-primary" @click="submitHandler($event)" :class="{'disabled': !isSubmitValid}">Submit form</button>
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
        this.fetchSections();
    },
    data(){
        return{
            sectionName: '',
            description: '',
            sections: []
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
                console.log(this.sections)
            })
            .catch((error) => console.error(error));
        },
        logout(){
            localStorage.removeItem('user_token');
            this.isUserLoggedIn = false;
            window.location.href = '/login';
        },
    }

}
</script>