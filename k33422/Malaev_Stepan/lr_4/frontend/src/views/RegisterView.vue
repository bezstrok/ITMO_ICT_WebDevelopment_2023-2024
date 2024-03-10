<template>
  <v-container class="fill-height" fluid>
    <v-row justify="center" align="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="elevation-12" outlined>
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>Register</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form ref="form" @submit.prevent="onRegister">
              <v-text-field
                  label="Email"
                  prepend-icon="mdi-email"
                  type="email"
                  v-model="registerForm.email"
                  :rules="[rules.required, rules.email]"
                  outlined dense
              ></v-text-field>

              <v-text-field
                  label="Password"
                  prepend-icon="mdi-lock"
                  type="password"
                  v-model="registerForm.password"
                  :rules="[rules.required]"
                  outlined dense
              ></v-text-field>

              <!-- Add any additional fields here -->

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
            <v-btn type="submit" color="secondary" class="white--text" block @click="onRegister">
              Register
            </v-btn>
          </v-card-actions>

          <v-card-text class="text-center">
            Already have an account?
            <router-link to="/login" class="register-link">Login</router-link>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import {mapActions, mapState} from 'vuex';

export default {
  data() {
    return {
      registerForm: {
        email: '',
        password: '',
        // Add additional fields as necessary
      },
      rules: {
        required: value => !!value || 'Required.',
        email: value => /.+@.+\..+/.test(value) || 'E-mail must be valid.',
        // Add additional rules as necessary
      },
    };
  },
  computed: {
    ...mapState('auth', ['authError']),
  },
  methods: {
    ...mapActions('auth', ['register']),
    async onRegister() {
      try {
        await this.register(this.registerForm);
        this.$router.push({name: 'Trades'});
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>

<style scoped>
/* Include any styles from your Login component and adjust as necessary */
.fill-height {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.register-link {
  color: #1976D2; /* Primary color */
  text-decoration: underline;
  cursor: pointer;
}
</style>
