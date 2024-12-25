import { createRouter, createWebHistory, type RouteLocationNormalized } from 'vue-router';
import useAuth from '@/stores/auth';
import useUser from '@/stores/user';

const VHomeView = () => import('@/views/VHomeView.vue');
const VOrderView = () => import('@/views/VOrderView.vue');
const VOrdersView = () => import('@/views/VOrdersView.vue');
const VNotAccessedView = () => import('@/views/VNotAccessedView.vue');

const isAuthorized = (): boolean => {
  const auth = useAuth();

  return Boolean(auth.token);
};

const authorize = async () => {
  const auth = useAuth();

  await auth.createToken();
};

const disallowAuthorized = () => {
  if (isAuthorized()) return { name: 'home' };
};

export const routes = [
  {
    path: '/',
    name: 'home',
    component: VHomeView,
  },
  {
    path: '/orders',
    name: 'orders',
    component: VOrdersView,
  },
  {
    path: '/orders/:id',
    name: 'order',
    component: VOrderView,
  },
  {
    path: '/not_accessed',
    name: 'not_accessed',
    component: VNotAccessedView,
    beforeEnter: [disallowAuthorized],
    meta: {
      isPublic: true,
    },
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

router.beforeEach(async (to: RouteLocationNormalized) => {
  // Пытаемся автоматически авторизировать пользователя.
  // В данный момент времени, приложение доступно только при использовании в Telegram mini app,
  // тем самым, благодаря запуску в окружении WebView, у нас есть доступ к данным о пользователе.
  // TODO: Это не верно, по сути мы будем люто спамить запросами по КД
  if (!(isAuthorized() || to.name === 'not_accessed')) {
    await authorize();
  }

  if (!(isAuthorized() || to.meta.isPublic)) {
    // Для не авторизированных пользователей доступны только публичные страницы.
    return { name: 'not_accessed' };
  }

  // Для авторизированных пользователей, подгружаем данные о пользователе для каждой страницы.
  if (isAuthorized()) {
    const user = useUser();
    if (!user.isLoaded()) user.getData();
  }

  if (!to.name) {
    // Все запросы по неизвестному uri пересылаем на начальную страницу
    return { name: 'home' };
  }
  if (to.name === 'orders' && 'tgWebAppStartParam' in to.query) {
    return { name: 'order', params: { id: to.query.tgWebAppStartParam?.toString() } };
  }
});

export default router;
