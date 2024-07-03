
<!-- App.vue -->
<script setup>

import { RouterLink, RouterView } from 'vue-router'
import { onMounted, onBeforeUnmount } from 'vue';
import { useCookies } from 'vue3-cookies';
import { postData } from '@/stores/api';

import NotificationService from '@/services/NotificationService';
import FloatingMenu from '@/components/FloatingMenu.vue'

const connectUser = async () => {
  const { cookies } = useCookies();

  const token = cookies.get('access_token');
  if (!token) {
    return;
  }

  const url = import.meta.env.VITE_APP_BACKEND_URL + '/users/connect/';
  const config = {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  };

  const { data, error } = await postData(url, {}, config);
  if (error) {
    //console.error('Error connecting user:', error);
  } else {
    //console.log('User connected successfully:', data.message);
  }
};

const disconnectUser = async () => {
  const { cookies } = useCookies();

  const token = cookies.get('access_token');
  //const token = useCookies.get('access_token');
  if (!token) {
    //console.error('No access token found.');
    return;
  }

  const url = import.meta.env.VITE_APP_BACKEND_URL + '/users/disconnect/';
  const config = {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  };

  const { data, error } = await postData(url, {}, config);
  if (error) {
    //console.error('Error disconnecting user:', error);
  }
};


// Cuando el componente se monta, iniciar la verificación de invitaciones
onMounted(() => {
  NotificationService.startCheckingInvitations();
  connectUser();
  window.addEventListener('beforeunload', disconnectUser);
});

// Cuando el componente se desmonta, detener la verificación de invitaciones
onBeforeUnmount(() => {
  NotificationService.stopCheckingInvitations();
  window.removeEventListener('beforeunload', disconnectUser);
});



</script>



<template>
  <div id="app">
    <!-- Contenido principal de tu aplicación -->
    <router-view />
    <FloatingMenu />

  </div>
</template>

<!-- Estilos, componentes, etc. -->
