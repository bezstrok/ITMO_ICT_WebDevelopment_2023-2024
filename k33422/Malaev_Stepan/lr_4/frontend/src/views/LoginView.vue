<template>
  <v-container class="fill-height" fluid>
    <v-row justify="center" align="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="elevation-12" outlined>
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>Login</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form ref="form" @submit.prevent="onLogin">
              <v-text-field
                  label="Email"
                  prepend-icon="mdi-email"
                  type="email"
                  v-model="loginForm.email"
                  :rules="[rules.required, rules.email]"
                  outlined dense
              ></v-text-field>

              <v-text-field
                  label="Password"
                  prepend-icon="mdi-lock"
                  type="password"
                  v-model="loginForm.password"
                  :rules="[rules.required]"
                  outlined dense
              ></v-text-field>

              <v-alert
                  type="error"
                  v-if="authError"
                  dense
                  outlined
                  class="mt-4"
              >
                {{ authError }}
              </v-alert>
            </v-form>
          </v-card-text>

          <v-card-actions class="pa-5 justify-center">
            <v-btn type="submit" color="secondary" class="white--text" block @click="onLogin">
              Sign in
            </v-btn>
          </v-card-actions>

          <v-card-text class="text-center">
            Don't have an account?
            <router-link to="/register" class="register-link">Register</router-link>
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
        // this.$router.push({name: 'dashboard'}); // Redirect to dashboard or home page
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>
