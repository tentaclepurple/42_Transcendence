<template>
  <div class="notification-page">
    <div class="page-content">
      <!-- Mostrar solo si no se ha aceptado la invitación -->
      <div v-if="!invitationAccepted">
        <p>Tienes una nueva invitación de chat.</p>
        <span @click="acceptInvitation(conversationId)" class="accept-btn">&#10003;</span>
        <span @click="declineInvitation" class="decline-btn">&#10005;</span>
      </div>
      
      <!-- Mostrar solo si se ha aceptado la invitación -->
      <div v-show="invitationAccepted">
        <ul v-if="messages.length > 0">
          <li v-for="(message, index) in messages" :key="index">{{ message }}</li>
        </ul>
        <div>
          <input type="text" v-model="newMessage" @keypress.enter="sendMessage" placeholder="Escribe tu mensaje y presiona Enter">
        </div>
      </div>

      <!-- Botón de rechazo siempre visible -->
      <span v-if="invitationAccepted" @click="declineInvitation" class="decline-btn">&#10005;</span>
    </div>
  </div>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router';
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { postData } from '@/stores/api';
import { useCookies } from 'vue3-cookies';

const router = useRouter();
const route = useRoute();
const conversationId = ref(null);
const socket = ref(null);
const messages = ref([]);
const newMessage = ref('');
const invitationAccepted = ref(false); // Variable de estado para controlar la aceptación

onMounted(() => {
  // Obtener el parámetro convoId de la ruta actual
  conversationId.value = route.params.convoId;
 // console.log('Conversation ID:', conversationId.value);
});

// Función para aceptar la invitación
const acceptInvitation = async (convoId) => {
  try {
    const { cookies } = useCookies();
    const token = cookies.get('token_auth');
    //console.log('Token de autorización:', token);
    //console.log("ConvoId:", convoId);
    const response = await postData(import.meta.env.VITE_APP_BACKEND_URL + '/conversations/accept_invitation/', { convoId }, {
      headers: { Authorization: `Token ${token}` }
    });
    //TODO wss
    const path = import.meta.env.VITE_WSS_APP_BACKEND_URL + `/ws/chat/${convoId}/?token=${token}`;
    //console.log(path);

    // Limpiar conexión WebSocket anterior si existe
    if (socket.value) {
      socket.value.close();
      socket.value = null;
    }

    // Establecer nueva conexión WebSocket
    socket.value = new WebSocket(path); 
    //console.log('Invitación aceptada:', response.data);
    
    invitationAccepted.value = true; // Cambiar el estado a aceptado

    // Manejar eventos de WebSocket
    socket.value.onmessage = (event) => {
      const data = JSON.parse(event.data);
      const receivedMessage = data.text; // Ajusta según la estructura de tu mensaje
      //console.log('Mensaje recibido:', receivedMessage);

      // Agregar mensaje solo si no está duplicado
      if (!messages.value.includes(receivedMessage)) {
        messages.value.push(receivedMessage);
      }
    };

    socket.value.onopen = () => {
      //console.log('Conexión WebSocket establecida');
    };

    socket.value.onclose = () => {
      //console.log('Conexión WebSocket cerrada');
      router.push('/home'); // Redirigir a la página de inicio al cerrar la conexión
    };

    socket.value.onerror = (error) => {
      //console.error('Error en la conexión WebSocket:', error);
    };

  } catch (error) {
    //console.error('Error al aceptar la invitación:', error);
  }
};

// Función para rechazar la invitación
const declineInvitation = async () => {
  try {
    const { cookies } = useCookies();
    const token = cookies.get('token_auth');
    //console.log('Token de autorización:', token);
    const response = await postData(import.meta.env.VITE_APP_BACKEND_URL + '/conversations/decline_invitation/', {}, {
      headers: { Authorization: `Token ${token}` }
    });

    //console.log('Invitación rechazada:', response.data);
    router.push('/home'); // Redirigir a la página de inicio
  } catch (error) {
    //console.error('Error al rechazar la invitación:', error);
  }
};

// Función para enviar un mensaje
const sendMessage = () => {
  if (newMessage.value.trim() === '') return; // Evitar enviar mensajes vacíos

  // Enviar el mensaje al WebSocket
  if (socket.value && socket.value.readyState === WebSocket.OPEN) {
    socket.value.send(JSON.stringify({ message: newMessage.value }));

    // Agregar el mensaje a la lista de mensajes locales
    messages.value.push(newMessage.value);
    newMessage.value = ''; // Limpiar el campo de nuevo mensaje
  }
};

// Limpia la conexión WebSocket antes de desmontar el componente
onBeforeUnmount(() => {
  if (socket.value) {
    socket.value.close();
    socket.value = null;
  }
});

</script>

<style scoped>
.notification-page {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f0f0f0; /* Color de fondo */
}

.page-content {
  text-align: center;
  width: 100%; /* Ajusta el ancho al 100% */
  padding: 20px;
  background-color: white;
  border: 1px solid #ccc;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.page-content button {
  margin: 5px;
}

.accept-btn,
.decline-btn {
  cursor: pointer;
  font-size: 1.5rem;
  margin: 10px;
}
</style>
