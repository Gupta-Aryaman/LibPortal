<template>
  <section class="p-3 p-md-4 p-xl-5 vh-100 d-flex justify-content-center align-items-center">
    <div class="container">
      <div class="row">
        <div class="col-12 col-md-6 bsb-tpl-bg-platinum">
          <div class="d-flex flex-column justify-content-between h-100 p-3 p-md-4 p-xl-5">
            <img class="img-fluid rounded mx-auto my-4" loading="lazy" src="../assets/lib.jpg" width="450" height="800" alt="BootstrapBrain Logo">

          </div>
        </div>
        <div class="col-12 col-md-6 bsb-tpl-bg-lotion">
          <div class="p-3 p-md-4 p-xl-5">
            <div class="row">
              <div class="col-12">
                <div class="mb-5">
                  <h2 class="h3">eLibrary</h2>
                  <h3 class="fs-6 fw-normal text-secondary m-0">Enter your details to register</h3>
                </div>
              </div>
            </div>
            <form>
              <div class="row gy-3 gy-md-4 overflow-hidden">

                <div class="col-12">
                  <label for="username" class="form-label">Username <span class="text-danger">*</span></label>
                  <input class="form-control" name="username" id="username" placeholder="username" v-model="username" required>
                </div>

                <div class="col-12">
                  <label for="email" class="form-label">Email <span class="text-danger">*</span></label>
                  <input type="email" class="form-control" name="email" id="email" v-model="email" :class="{ 'is-invalid': !isEmailValid && email.length > 0}" placeholder="name@example.com" required>
                  <div class="invalid-feedback" v-if="!isEmailValid">
                    Enter email.
                  </div>
                </div>

                <div class="col-12">
                  <label for="password" class="form-label">Password <span class="text-danger">*</span></label>
                  <input type="password" class="form-control" :class="{ 'is-invalid': !isPasswordValid && password.length > 0 }" name="password" id="password" value="" v-model="password" placeholder="password" required>
                  <div class="invalid-feedback" v-if="!isPasswordValid && password.length > 0">
                    Password must contain at least one capital letter, one number and should be atleast of 8 characters.
                  </div>
                </div>

                <div class="col-12">
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" value="" name="iAgree" id="iAgree" v-model="checkbox" required>
                    <label class="form-check-label text-secondary" for="iAgree">
                      I agree to the <a href="#!" class="link-primary text-decoration-none">terms and conditions</a>
                    </label>
                  </div>
                </div>

                <div class="col-12">
                  <div class="d-grid">
                    <button class="btn bsb-btn-xl btn-primary" v-on:click="submitForm($event)" :disabled="!isFormValid">Sign up</button>
                    
                  </div>
                </div>

              </div>
            </form>
            <div class="row">
              <div class="col-12">
                <hr class="mt-5 mb-4 border-secondary-subtle">
                <p class="m-0 text-secondary text-end">Already have an account? <a href="/login" class="link-primary text-decoration-none">Log in</a></p>
              </div>
            </div>
            
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
  
  <script>
  import axios from 'axios';

  export default {
    name: 'SignupForm',
    data() {
      return {
        username: '',
        email: '',
        password: '',
        checkbox: false
      };
    },
    computed: {
      isPasswordValid() {
        const capitalLetterRegex = /[A-Z]/;
        const numberRegex = /[0-9]/;
        return capitalLetterRegex.test(this.password) && numberRegex.test(this.password) && this.password.length >= 8;
      },
      isFormValid() {
        return this.username && this.isEmailValid && this.password && this.isPasswordValid && this.checkbox;
      },
      isEmailValid() {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(this.email);
      },
    },
    methods: {
      async submitForm(event) {
        event.preventDefault();
        
      
        const myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");

        const raw = JSON.stringify({
          "username": this.username,
          "email": this.email,
          "password": this.password
        });

        const requestOptions = {
          method: "POST",
          headers: myHeaders,
          body: raw,
          redirect: "follow"
        };

        fetch("http://127.0.0.1:5000/signup", requestOptions)
        .then((response) => {
          if (response.status === 200) {
            window.alert('Successful registration!');
            setTimeout(() => {
              window.location.href = '/login';
            }, 500);

          } else if (response.status === 403) {
            window.alert('User already exists');
          } else if (response.status === 500) {
            window.alert('Internal server error');
          } else {
            window.alert('Unexpected status code:', response.status);
          }
        })
        .catch((error) => {
          console.error('Fetch error:', error);
        });
               

        

        
      }
    }
  };
  </script>
  
  <style scoped>
  /* Add your CSS styles here */
  </style>
  