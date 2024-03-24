<template>
    <LibrarianHeader />

    <div class="container pt-5">
        <div class="row"  v-if="sections.length">
            <div class="col-md-3 mb-3" v-for="section in sections" :key="section.id">
                <LibrarianSectionCard :title="section.section" :description="section.description"/>
            </div>
        </div>
        <div class="d-flex justify-content-center align-items-center" v-else>
            <h2>Add sections to view!</h2>
        </div>
    </div>

    <div class="d-flex justify-content-center mt-5">
        <svg xmlns="http://www.w3.org/2000/svg" width="70" height="70" fill="currentColor" class="bi bi-plus-circle btn" viewBox="0 0 16 16" @click="addSectionHandler">
            <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
            <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4"/>
        </svg>
    </div>
    
</template>

<script>

import LibrarianHeader from './LibrarianHeader.vue';
import LibrarianSectionCard from './LibrarianSectionCard.vue';

export default{
    name: 'LibrarianDashboard',
    components: {
        LibrarianHeader,
        LibrarianSectionCard
    },
    data(){
        return{
            username: '',
            sections: [],
            queryString: '',
        };
    },
    created(){
        if (this.$route.query.section !== undefined) {
            this.isSection = true;
            this.queryString = this.$route.query.section;
        }

        this.fetchSections();
    },
    methods: {
        logout(){
            localStorage.removeItem('user_token');
            this.isUserLoggedIn = false;
            window.location.href = '/login';
        },
        addSectionHandler(){
            // window.location.href = '/librarian/add-section';
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
                    window.alert('Invalid Credentials');
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
        }
    }
}

</script>