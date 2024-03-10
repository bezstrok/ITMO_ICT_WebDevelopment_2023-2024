import {createRouter, createWebHistory} from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from "@/views/LoginView.vue";
import RegisterView from "@/views/RegisterView.vue";
import TradesView from "@/views/TradesView.vue";
import TradeDetailView from "@/views/TradeDetailView.vue";
import ProductsView from "@/views/ProductsView.vue";
import ProductDetail from "@/views/ProductDetail.vue";
import ProfileView from "@/views/ProfileView.vue";
import BrokerProfile from "@/views/BrokerProfile.vue";

const routes = [
    {
        path: '/',
        name: 'home',
        component: HomeView
    },
    {
        path: '/login',
        name: 'Login',
        component: LoginView,
    },
    {
        path: '/register',
        name: 'Register',
        component: RegisterView,
    },
    {
        path: '/trades',
        name: 'Trades',
        component: TradesView
    },
    {
        path: '/trades/:id',
        name: 'TradeDetail',
        component: TradeDetailView,
        props: true
    },
    {
        path: '/products',
        name: 'Products',
        component: ProductsView
    },
    {
        path: '/products/:id',
        name: 'ProductDetail',
        component: ProductDetail,
        props: true
    },
    {
        path: '/profile',
        name: 'Profile',
        component: ProfileView
    },
    {
        path: '/broker',
        name: 'Broker',
        component: BrokerProfile
    },
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router
