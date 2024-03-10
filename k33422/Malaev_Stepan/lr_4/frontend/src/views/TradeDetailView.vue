<template>
  <v-container>
    <v-card v-if="!isLoading" class="mx-auto" max-width="800">
      <v-card-title class="blue-grey darken-4 white--text">Trade Detail</v-card-title>
      <v-card-text>
        <template v-for="(value, key) in tradeDetail" :key="key">
          <div v-if="typeof value === 'object' && value !== null && !Array.isArray(value)">
            <NestedCard :obj="value" :title="formatTitle(key)"/>
          </div>
          <v-list v-else two-line dense>
            <v-list-item>
                <v-list-item-title class="blue-grey--text">{{ formatTitle(key) }}</v-list-item-title>
                <v-list-item-subtitle>{{ formatValue(key, value) }}</v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </template>
      </v-card-text>
    </v-card>
    <v-progress-circular v-else indeterminate color="primary"></v-progress-circular>
  </v-container>
</template>

<script>
import api from "@/api";
import NestedCard from "@/components/NestedCard.vue";

export default {
  components: {
    NestedCard,
  },
  data() {
    return {
      tradeDetail: {},
      isLoading: true,
    };
  },
  created() {
    this.fetchTradeDetail();
  },
  methods: {
    async fetchTradeDetail() {
      this.isLoading = true;
      try {
        const response = await api.get(`/trades/${this.$route.params.id}/`);
        this.tradeDetail = response.data;
        this.isLoading = false;
      } catch (error) {
        console.error('There was an error fetching the trade detail:', error);
        this.isLoading = false;
      }
    },
    formatTitle(key) {
      return key.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
    },
    formatValue(key, value) {
      if (key.includes('time')) {
        return this.formatDate(value);
      }
      return value.toString();
    },
    formatDate(dateString) {
      const options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        timeZoneName: 'short'
      };
      return new Date(dateString).toLocaleDateString(undefined, options);
    },
  },
};
</script>
