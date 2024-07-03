import { getData } from '@/stores/api';
import { useCookies } from 'vue3-cookies';
import store from '@/stores/vuex_store';

const API_URL = import.meta.env.VITE_APP_BACKEND_URL;

const NotificationService = {
  checkInvitationInterval: null,

  startCheckingInvitations() {
    if (store.state.isCheckingInvitations) {
      // Already checking, so we skip starting again
      return;
    }

    // Start checking invitations
    store.dispatch('setCheckingInvitations', true);
    this.checkInvitations();
    this.checkInvitationInterval = setInterval(() => {
      this.checkInvitations();
    }, 5000); // Interval of 5 seconds
  },

  stopCheckingInvitations() {
    // Stop checking invitations
    clearInterval(this.checkInvitationInterval);
    this.checkInvitationInterval = null;
    store.dispatch('setCheckingInvitations', false);
  },

  async checkInvitations() {
    if (!store.state.isCheckingInvitations) {
      // If the checking has been stopped, skip the request
      return;
    }

    const { cookies } = useCookies();
    const token = cookies.get('access_token');
    if (!token)
      return ;
    const { data, error } = await getData(`${API_URL}/conversations/check_invitation/`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    
    if (data) {
      const chatInvitationId = data.chat_invitation;
      try {
        if (chatInvitationId !== 0) {
          const token = cookies.get('token_auth');
          const convoInfo = await getData(import.meta.env.VITE_APP_BACKEND_URL + "/conversations/" + chatInvitationId + "/", {
              headers: { Authorization: `Token ${token}` }
              });
          //console.log("convoInfo: ", convoInfo);
          const initiator = convoInfo.data['initiator'].username;
          //console.log("data: ", data);
          //console.log(`Invitación de chat pendiente: ${chatInvitationId}`);
          store.dispatch('addNotification', {
            type: 'chat',
            notification: {
              id: chatInvitationId,
              message: `Invitación de chat pendiente: ${initiator}`
            }
          });
          //router.push({ name: 'notification', params: { convoId: chatInvitationId } });
        }
      } catch (error) {
        //console.error(error);
      }
    } else {
      //console.error(error);
    }
  }
};

export default NotificationService;
