<template>
  <div v-if="isFloatingMenuVisible" :class="['floating-menu', { minimized: isMinimized }]">
    <div v-if="!isMinimized" class="menu-content">
      <h4>Chat Notifications</h4>
      <div v-for="notification in chatNotifications" :key="notification.id" class="notification">
        <p>{{ notification.message }}</p>
        <button @click="acceptChat(notification)" class="emoji-button">✔️</button>
        <button @click="rejectChat({ type: 'chat', id: notification.id })" class="emoji-button">❌</button>
      </div>
    </div>
    <div>
      <button class="toggle-button" @click="toggleMenu">
        {{ isMinimized ? 'Show' : 'Hide' }}
      </button>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions, mapMutations } from 'vuex';
import { useCookies } from 'vue3-cookies';
import { postData, getData } from '@/stores/api';

export default {
  computed: {
    ...mapState(['isFloatingMenuMinimized', 'notifications', 'isFloatingMenuVisible']),
    isMinimized() {
      return this.isFloatingMenuMinimized;
    },
    chatNotifications() {
      return this.notifications.chat;
    },
    gameNotifications() {
      return this.notifications.game;
    }
  },
  methods: {
    ...mapMutations(['setUserSelected']),
    ...mapActions(['toggleFloatingMenu', 'acceptNotification', 'denyNotification']),
    toggleMenu() {
      this.toggleFloatingMenu();
    },
    async acceptChat(notification) {
      // Add your logic here to accept the chat notification
      try {
        const { cookies } = useCookies();
        const convoId = notification.id;
        const token = cookies.get('token_auth');
        //console.log('Token de autorización:', token);
        //console.log("ConvoId:", convoId);
        const convoInfo = await getData(import.meta.env.VITE_APP_BACKEND_URL + "/conversations/" + convoId + "/", {
          headers: { Authorization: `Token ${token}` }
					});
        //console.log(convoInfo.data['initiator']);
        this.setUserSelected(convoInfo.data['initiator']);
        const response = await postData(import.meta.env.VITE_APP_BACKEND_URL + "/conversations/accept_invitation/", { convoId }, {
          headers: { Authorization: `Token ${token}` }
        });
        //console.log(response);
        this.$router.push('/community');
        this.acceptNotification({ type: 'chat', id: notification.id });
      } catch (error) {
        //console.error('Error al aceptar la invitación:', error);
      }

      
    },
    async rejectChat(notification) {
      this.denyNotification({ type: 'chat', id: notification.id });
      // Add your logic here to reject the chat notification
      try {
        const { cookies } = useCookies();
        const token = cookies.get('token_auth');
        //console.log('Token de autorización:', token);
        const response = await postData(import.meta.env.VITE_APP_BACKEND_UTL + "/conversations/decline_invitation/", {}, {
          headers: { Authorization: `Token ${token}` }
        });

        //console.log('Invitación rechazada:', response.data);
      } catch (error) {
        //console.error('Error al rechazar la invitación:', error);
      }
        }
      }
};
</script>

<style scoped>
.floating-menu {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 300px;
  background-color: white;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.minimized {
  height: 40px;
  width: 150px;
}

.menu-content {
  padding: 10px;
}

.notification {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.emoji-button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.5em;
}

.toggle-button {
  width: 100%;
  background: none;
  border: none;
  padding: 10px;
  cursor: pointer;
  text-align: center;
  background-color: #007bff;
  color: white;
  border-top: 1px solid #ccc;
}
</style>
