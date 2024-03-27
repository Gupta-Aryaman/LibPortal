<template>
    <UserHeader />


</template>

<script>
    import UserHeader from './UserHeader.vue';

    export default{
        name: 'UserStats',
        components: {
            UserHeader
        },
        mounted(){
            this.fetchStats();
        },
        data() {

        },
        methods: {
            
        }

    }

    
      

</script>