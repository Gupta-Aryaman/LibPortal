<template>
    <section class="py-3 py-md-5 d-flex align-items-center ">
    <div class="container">
        <div class="row justify-content-center align-items-center align-items-center">
        <div class="col-12 col-sm-10 col-md-8 col-lg-6 col-xl-5 ">
            <div class="card border border-light-subtle rounded-3 shadow-sm">
            <div class="card-body p-3 p-md-4 p-xl-5">
                <div class="text-center mb-3">
                <a href="#!">
                    <img src="../assets/login.jpg" alt="BootstrapBrain Logo" width="350" height="250">
                </a>
                </div>
                <h1 class="fs-4 fw-bold text-center text-secondary mb-4">{{ title }}</h1>
                <form action="#!">
                <div class="row gy-2 overflow-hidden">
                    <div class="col-12">
                    <!-- <div class="form-floating mb-3" v-if="isLibrarian">
                        <input type="username" class="form-control" name="email" id="email" placeholder="" v-model="email" required>
                        <label for="email" class="form-label">Username</label>
                    </div> -->
                    <div class="form-floating mb-3">
                        <input type="username" class="form-control" name="email" id="email" placeholder="name@example.com" v-model="email" required>
                        <label for="email" class="form-label">Email</label>
                    </div>
                    </div>
                    <div class="col-12">
                    <div class="form-floating mb-3">
                        <input type="password" class="form-control" name="password" id="password" value="" placeholder="Password" v-model="password" required>
                        <label for="password" class="form-label">Password</label>
                    </div>
                    </div>
                    <div class="col-12">
                    <!-- <div class="d-flex gap-2 justify-content-between" v-if="isLibrarian">
                        
                        <a href="/login" class="link-primary text-decoration-none">Login as user?</a>
                    </div>
                    <div class="d-flex gap-2 justify-content-between" v-else>
                        
                        <a href="/librarian/login" class="link-primary text-decoration-none">Login as librarian?</a>
                    </div> -->
                    </div>
                    <div class="col-12">
                    <div class="d-grid my-3">
                        <button class="btn btn-primary btn-lg" type="submit" v-on:click="submitForm($event)" :disabled="!isFormValid">Log in</button>
                    </div>
                    </div>
                    <div class="col-12">
                    <p class="m-0 text-secondary text-center">Don't have an account? <a href="/signup" class="link-primary text-decoration-none">Sign up</a></p>
                    </div>
                </div>
                </form>
            </div>
            </div>
        </div>
        </div>
    </div>
    </section>
</template>

<script>
export default{
    name: 'LoginForm',
    props: {
        title: String,
        isLibrarian: Boolean
    },
    data(){
        return{
            email: '',
            password: ''
        }
    },
    computed: {
        isFormValid(){
            return this.email.length > 0 && this.password.length > 0;
        }
    },
    methods: {
        submitForm(event) {
            event.preventDefault();
            this.$emit('login', {email: this.email, password: this.password});
        }
        
    }
}
</script>