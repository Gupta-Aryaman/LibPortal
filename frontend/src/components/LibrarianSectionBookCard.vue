<template>
    <div class="card" style="width: 18rem;">
        <div class="card-body p-3">
            <h5 class="card-title">{{ book.title }}</h5>
            <h6 class="card-subtitle mb-2 text-body-secondary">{{ book.author }}</h6>
            
            <p class="card-text description">
                <b>Currently Issued By:</b>
                <div class="description" v-if="book.borrowed_by.length > 0" v-for="x in book.borrowed_by">
                    <p class="card-text" ><i>{{ x }}</i></p>
                </div>
                <div v-else>
                    <p class="card-text" ><i>None</i></p>
                </div>
            </p>
            

            

            <a class=""><b>Copies Available: {{ book.available_copies }}</b></a>
            
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
    }
}
</script>
