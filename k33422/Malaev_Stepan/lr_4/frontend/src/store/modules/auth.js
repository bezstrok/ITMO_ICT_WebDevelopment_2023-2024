import api from "@/api";

const state = {
    user: null,
    token: localStorage.getItem('token') || '',
};

const getters = {
    isAuthenticated: state => !!state.token,
    user: state => state.user,
};

const actions = {
    async login({commit}, user) {
        const response = await api.post('/auth/jwt/create/', user);
        if (response.data.access) {
            const token = response.data.access;
            localStorage.setItem('token', token);
            api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
            commit('auth_success', token);
            await this.dispatch('fetchUser');
        }
    },
    async fetchUser({commit}) {
        const response = await api.get('/auth/users/me/');
        commit('user_profile', response.data);
    },
    async logout({commit}) {
        localStorage.removeItem('token');
        commit('logout');
        delete api.defaults.headers.common['Authorization'];
    },
    async register({dispatch, commit}, user) {
        try {
            const response = await api.post('/auth/users/', user);

            await dispatch('login', {
                email: user.email,
                password: user.password,
            });

            commit('register_success');
            return response;
        } catch (error) {
            throw error;
        }
    },
};

const mutations = {
    auth_success(state, token) {
        state.token = token;
        state.user = null;
    },
    user_profile(state, user) {
        state.user = user;
    },
    logout(state) {
        state.token = '';
        state.user = null;
    },
    register_success(state) {

    },
};

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations,
};
