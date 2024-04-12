<template>
    <LoginForm :title="'Login'" :isLibrarian="false"  @login = "handleChildSubmit"  class="vh-100 d-flex justify-content-center align-items-center"/>
</template>

<script>
import LoginForm from './LoginForm.vue';

export default {
    name: 'UserLoginPage',
    components: {
        LoginForm
    },
    methods: {
        handleChildSubmit(data){
            const myHeaders = new Headers();
            myHeaders.append("Content-Type", "application/json");

            const raw = JSON.stringify({
                "email": data.email,
                "password": data.password
            });

            const requestOptions = {
                method: "POST",
                headers: myHeaders,
                body: raw,
                redirect: "follow"
            };

            fetch("http://127.0.0.1:5000/login", requestOptions)
            .then((response) => {
                if (response.status === 200) {
                    return (response.json())
                } else if (response.status === 401) {
                    window.alert('Invalid Credentials');
                } else if (response.status === 500) {
                    window.alert('Internal server error');
                } else {
                    window.alert('Unexpected status code:', response.status);
                }
            })
            .then((data) => {
                if (data.role == "user") {
                    localStorage.setItem('user_token', data.token);
                    localStorage.setItem('user', data.user);

                    // window.alert('Successful Login!');
                    setTimeout(() => {
                        window.location.href = '/dashboard';
                    }, 500);
                } else if (data.role == "librarian"){
                    localStorage.setItem('user_token', data.token);
                    localStorage.setItem('user', data.user);

                    // window.alert('Successful Login!');
                    setTimeout(() => {
                        window.location.href = '/librarian/dashboard';
                    }, 500);
                }
            })
            .catch((error) => {
            console.error('Fetch error:', error);
            });
        }
    }
}
</script>