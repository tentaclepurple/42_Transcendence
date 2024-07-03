import Vue from 'vue';
import Vuex from 'vuex';
import { useCookies } from 'vue3-cookies';

Vue.use(Vuex);
const { cookies } = useCookies();

export default new Vuex.Store({
  state: {
    userSelected: null,
    triggerChatSocketInit: false,
    triggerEnterChat: 0,
    showConnnectionnAlert: false,
    isFloatingMenuMinimized: false,
    notifications: {
      chat: {},
      game: {}
    },
    isCheckingInvitations: false,
    isFloatingMenuVisible: true,
    authToken: cookies.get('access_token') || null
  },
  mutations: {
    setUserSelected(state, user) {
      state.userSelected = user;
    },
    setTriggerChatSocketInit(state, payload) {
      state.triggerChatSocketInit = payload;
    },
    setTriggerEnterChat(state, payload) {
      state.triggerEnterChat = payload;
    },
    setConnAlert(state, payload) {
      state.showConnnectionnAlert = payload;
    },
    setFloatingMenuMinimized(state, isMinimized) {
      state.isFloatingMenuMinimized = isMinimized;
    },
    setNotifications(state, notifications) {
      state.notifications = notifications;
    },
    addNotification(state, { type, notification }) {
      if (state.notifications[type]) {
        // Directly assign the notification to the object
        state.notifications[type] = { ...state.notifications[type], [notification.id]: notification };
      } else {
        //console.error(`Notification type "${type}" not found`);
      }
    },
    acceptNotification(state, { type, id }) {
      if (!state.notifications[type]) {
        //console.error(`Notification type "${type}" not found`);
        return;
      }
      if (type === 'chat' && id) {
        setTimeout(function() {
          // Your code here
          state.triggerEnterChat = id;
        }, 1000);
      }
      // Directly delete the notification from the object
      const { [id]: removed, ...remaining } = state.notifications[type];
      state.notifications[type] = remaining;
    },
    removeNotification(state, { type, id }) {
      if (!state.notifications[type]) {
        //console.error(`Notification type "${type}" not found`);
        return;
      }
      // Directly delete the notification from the object
      const { [id]: removed, ...remaining } = state.notifications[type];
      state.notifications[type] = remaining;
      
    },
    setCheckingInvitations(state, isChecking) {
      state.isCheckingInvitations = isChecking; // New mutation
    },
    setFloatingMenuVisible(state, isVisible) {
      state.isFloatingMenuVisible = isVisible; // New mutation
    },
    setAuthToken(state, token) {
      //state.isAuthenticated = isAuthenticated;
      state.authToken = token;
    }
  },
  actions: {
    toggleFloatingMenu({ commit, state }) {
      commit('setFloatingMenuMinimized', !state.isFloatingMenuMinimized);
    },
    acceptNotification({ commit }, { type, id }) {
      //console.log(`Accepted notification of type ${type} with id ${id}`);
      commit('acceptNotification', { type, id });
    },
    denyNotification({ commit }, { type, id }) {
      //console.log(`Denied notification of type ${type} with id ${id}`);
      commit('removeNotification', { type, id });
    },
    setCheckingInvitations({ commit }, isChecking) {
      commit('setCheckingInvitations', isChecking); // New action
    },
    setFloatingMenuVisible({ commit }, isVisible) {
      commit('setFloatingMenuVisible', isVisible); // New action
    },
    addNotification({ commit }, payload) { // New action
      commit('addNotification', payload);
    },
    login({ commit }, token) {
      commit('setAuthToken', token);
    },
    logout({ commit }) {
      commit('setAuthToken', null);
    }
  }
});