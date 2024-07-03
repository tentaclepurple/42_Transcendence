<template>
	<div>
	  <div class="flex">
		<div class="min-h-screen flex-1">
		  <div class="flex h-full items-center">
			<RegisterForm />
		  </div>
		</div>
		<div class="hidden min-h-screen flex-1 bg-gray-50 lg:flex" />
	  </div>
	</div>
  </template>

<script>
import RegisterForm from '../components/UserRegister.vue';

export default {
  name: 'RegisterView',
  components: {
    RegisterForm
  }
}
</script>