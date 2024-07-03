import { createRouter, createWebHistory } from 'vue-router';
import RootView from '../views/RootView.vue';
import NotificationService from '@/services/NotificationService';
import store from '@/stores/vuex_store'

const avoidRoutes = ['root', 'register', 'login', 'game', 'not-found'];
const noRedirectRoutes = ['root', 'register', 'login', 'not-found'];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'root',
      component: RootView
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue')
    },
    {
      path: '/home',
      name: 'home',
      component: () => import('../views/HomeView.vue')
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/UserProfileView.vue')
    },
    {
      path: '/game/:game_id?',
      name: 'game',
      component: () => import('../views/GameView.vue'),
      props: route => ({ game_id: Number(route.params.game_id) || 0 })
    },
    {
      path: '/stats/:user_id?',
      name: 'stats',
      component: () => import('../views/StatisticsView.vue'),
      props: route => ({ user_id: Number(route.params.user_id) || 0 })
    },
    {
      path: '/community',
      name: 'community',
      component: () => import('../views/CommunityView.vue')
    },
    {
      path: '/tournaments',
      name: 'tournaments',
      component: () => import('../views/TournamentsView.vue')
    },
    {
      path: '/:pathMatch(.*)*', // Ruta para capturar todas las rutas no encontradas
      name: 'not-found',
      component: () => import('../views/NotFoundView.vue') // Vista para mostrar cuando no se encuentra la ruta
    },
  ]
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = !!store.state.authToken;

  NotificationService.stopCheckingInvitations();
  store.dispatch('setFloatingMenuVisible', false); // Hide floating menu

  if (!isAuthenticated && !noRedirectRoutes.includes(to.name)) {
    //console.log('Usuario no autenticado y ruta no en noRedirectRoutes. Redirigiendo a login.');
    next({ name: 'login' });
    return;
  }
  if (isAuthenticated && !avoidRoutes.includes(to.name)) {  
    //console.log('Usuario autenticado. Iniciando servicio de notificaciones y mostrando menú flotante.');
    NotificationService.startCheckingInvitations();
    store.dispatch('setFloatingMenuVisible', true); // Show floating menu
  }
  next();
});

export default router;