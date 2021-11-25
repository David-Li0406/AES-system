// 存储token相关信息

import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

const store = new Vuex.Store({
    state: {
        // 存储token
        token: ''
    },
    mutations: {
        // 设置token，并将token存入localStorage
        set_token (state, token) {
            state.token = token;
            localStorage.token = token;
        },
        // 删除token
        del_token (state) {
            state.token = '';
            localStorage.removeItem('token');
        }
    }
});

export default store;

