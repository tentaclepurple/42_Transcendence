<template>
  <!--Main div-->
  <div class="bg-light vh-100 vw-100 container-fluid">
    <div class="row h-100">
      <!--left side--> 
      <div class="col-md-6 d-flex justify-content-center align-items-center bg-image">
        <h2></h2>
      </div>
      <!--right side--> 
      <div class="col-md-6 bg-pong d-flex justify-content-center align-items-center">
        <!-- center div-->
        <div>
            <!-- login/register 1-->
            <div>
              <h1 class="text-white">Transcendence</h1>
            </div>
            <div>
                <!-- login/register 2-->
                <div>
                  <!-- login-->
                  <button class="btn bg-btn-color text-white m-4" @click="handle_sign_in">
                      <div>
                        Login
                      </div>
                  </button>
                  <!-- register-->
                  <button class="btn bg-btn-color text-white m-2" @click="handle_register">
                    <div>
                      Register
                    </div>
                  </button>
                </div>
            </div>
          </div>

          <!-- info div-->
          <div>
          </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router';

export default {
  setup() {
    const router = useRouter();

    const handle_sign_in = () => {
      router.push('/login'); // Assuming you have a route named '/login'
      //console.log("Navigating to Login!");
    };

    const handle_register = () => {
      router.push('/register'); // Assuming you have a route named '/register'
      //console.log("Navigating to Register!");
    };

    return { handle_sign_in, handle_register };
  }
}
</script>

<style>
  .bg-pong {
    background-color: rgb(9 46 75);
  }
  .bg-image {
    background-image: url('@/assets/bg-pong.jpg');
    background-size: cover;
    background-position: center;
  }

  .bg-btn-color {
    background-color: #050609 !important;
    border-color: #e0c411 !important;
    margin-top: 10px !important;
  }

</style>