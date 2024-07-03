<template>
	<div>
	  <div class="flex">
		<div class="min-h-screen flex-1">
		  <div class="flex h-full items-center py-8 px-5">
			<UserProfileInfo />
		  </div>
		</div>
		<div class="hidden min-h-screen flex-1 bg-gray-50 px-5 py-5 lg:flex" />
	  </div>
	</div>
  </template>

<script>
import UserProfileInfo from '../components/UserProfileInfo.vue';

export default {
  name: 'UserProfileView',
  components: {
    UserProfileInfo
  }
}
</script>