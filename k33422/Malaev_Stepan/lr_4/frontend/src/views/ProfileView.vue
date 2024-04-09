<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title class="blue-grey darken-4 white--text">My Profile</v-card-title>
          <v-card-text>
            <v-list dense>
              <v-list-item>
                <v-icon>mdi-email</v-icon>
                {{ userProfile.email }}
              </v-list-item>
              <v-list-item>
                <v-icon>mdi-account</v-icon>
                {{ fullName }}
              </v-list-item>
              <v-list-item>
                <v-icon>mdi-briefcase-check</v-icon>
                Broker
                <v-icon v-if="userProfile.is_broker" color="green" small>mdi-check-circle</v-icon>
              </v-list-item>
              <v-list-item>
                <v-icon>mdi-factory</v-icon>
                Manufacturer
                <v-icon v-if="userProfile.is_manufacturer" color="green" small>mdi-check-circle</v-icon>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Update Profile</v-card-title>
          <v-card-text>
            <v-form ref="form">
              <v-text-field v-model="form.firstName" label="First Name" required></v-text-field>
              <v-text-field v-model="form.lastName" label="Last Name" required></v-text-field>
              <v-btn color="primary" @click="updateProfile">
                Save Changes
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>


<script>
import api from "@/api";

export default {
  data() {
    return {
      userProfile: {},
      form: {
        firstName: '',
        lastName: '',
      },
    };
  },
  computed: {
    fullName() {
      return `${this.userProfile.first_name} ${this.userProfile.last_name}`;
    },
  },
  async created() {
    await this.fetchUserProfile();
  },
  methods: {
    async fetchUserProfile() {
      try {
        const response = await api.get('/auth/users/me/');
        this.userProfile = response.data;
        this.form.firstName = this.userProfile.first_name;
        this.form.lastName = this.userProfile.last_name;
      } catch (error) {
        console.error("There was an error fetching the user's profile:", error);
      }
    },
    async updateProfile() {
      try {
        const payload = {
          first_name: this.form.firstName,
          last_name: this.form.lastName,
        };
        await api.patch('/auth/users/me/', payload);
        this.fetchUserProfile();
      } catch (error) {
        console.error("There was an error updating the user's profile:", error);
      }
    },
  },
};
</script>

<style scoped>
</style>
