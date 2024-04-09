<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" lg="4" md="6" sm="8">
        <v-card class="elevation-12" outlined>
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>Login</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form ref="form" @submit.prevent="onLogin">
              <v-text-field
                  v-model="loginForm.email"
                  :rules="[rules.required, rules.email]"
                  dense
                  label="Email"
                  outlined
                  prepend-icon="mdi-email" type="email"
              ></v-text-field>

              <v-text-field
                  v-model="loginForm.password"
                  :rules="[rules.required]"
                  dense
                  label="Password"
                  outlined
                  prepend-icon="mdi-lock" type="password"
              ></v-text-field>

              <v-alert
                  v-if="authError"
                  class="mt-4"
                  dense
                  outlined
                  type="error"
              >
                {{ authError }}
              </v-alert>
            </v-form>
          </v-card-text>

          <v-card-actions class="pa-5 justify-center">
            <v-btn block class="white--text" color="secondary" type="submit" @click="onLogin">
              Sign in
            </v-btn>
          </v-card-actions>

          <v-card-text class="text-center">
            Don't have an account?
            <router-link class="register-link" to="/register">Register</router-link>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.fill-height {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.v-toolbar {
  border-radius: 4px 4px 0 0;
}

.v-btn {
  height: 48px;
  padding: 0 25px;
}

</style>

<script>
import {mapActions, mapState} from 'vuex';

export default {
  data() {
    return {
      loginForm: {
        email: '',
        password: '',
      },
      rules: {
        required: value => !!value || 'Required.',
        email: value => /.+@.+\..+/.test(value) || 'E-mail must be valid.',
      },
    };
  },
  computed: {
    ...mapState('auth', ['authError']),
  },
  methods: {
    ...mapActions('auth', ['login']),
    async onLogin() {
      try {
        await this.login(this.loginForm);
        this.$router.push({name: 'Trades'});
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>
