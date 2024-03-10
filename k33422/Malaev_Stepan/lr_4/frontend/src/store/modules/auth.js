import api from "@/api";

const state = {
    user: null,
    token: localStorage.getItem('token') || '',
    authError: null,
};

const getters = {
    isAuthenticated: state => !!state.token,
    user: state => state.user,
    isBroker: state => state.user ? state.user.is_broker : false,
    isManufacturer: state => state.user ? state.user.is_manufacturer : false,
};

const actions = {
    async login({commit}, user) {
        try {
            const response = await api.post('/auth/jwt/create/', user);
            if (response.data.access) {
                const token = response.data.access;
                localStorage.setItem('token', token);
                api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
                commit('auth_success', token);
                await this.dispatch('fetchUser');
                commit('set_auth_error', null);
            }
        } catch (error) {
            commit('set_auth_error', error.response.data.detail || 'Login failed');
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
            return response;
        } catch (error) {
            commit('set_auth_error', error.response.data.detail || 'Register failed');
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
    set_auth_error(state, error) {
        state.authError = error;
    },
};

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations,
};
