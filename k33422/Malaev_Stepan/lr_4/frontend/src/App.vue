<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>TradeFlow</v-toolbar-title>

      <v-tabs v-if="isAuthenticated" centered class="flex-grow-1">
        <v-tab to="/trades">Trades</v-tab>
        <v-tab to="/products">Products</v-tab>
      </v-tabs>

      <v-spacer></v-spacer>

      <template v-if="isAuthenticated">
        <v-menu offset-y>
          <template v-slot:activator="{ props }">
            <v-btn v-bind="props">My Account</v-btn>
          </template>
          <v-list>
            <v-list-item to="/profile">
              <v-list-item-title>My Profile</v-list-item-title>
            </v-list-item>
            <v-list-item to="/broker">
              <v-list-item-title>Broker</v-list-item-title>
            </v-list-item>
            <v-list-item to="/manufacturer">
              <v-list-item-title>Manufacturer</v-list-item-title>
            </v-list-item>
            <v-list-item @click="logout">
              <v-list-item-title>Logout</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </template>

      <template v-else>
        <v-btn to="/login">Login</v-btn>
        <v-btn to="/register">Register</v-btn>
      </template>
    </v-app-bar>

    <v-main>
      <router-view/>
    </v-main>

    <v-footer fixed padless>
      <v-col class="text-center" cols="12">
        © {{ new Date().getFullYear() }} Trading Platform
      </v-col>
    </v-footer>
  </v-app>
</template>

<script>
import {mapActions, mapGetters} from 'vuex';

export default {
  computed: {
    ...mapGetters('auth', ['isAuthenticated']),
  },
  methods: {
    ...mapActions('auth', ['logout']),
  },
};
</script>
