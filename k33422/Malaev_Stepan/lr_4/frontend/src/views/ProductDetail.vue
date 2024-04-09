<template>
  <v-container>
    <v-card>
      <v-card-title>{{ productDetail.name }}</v-card-title>
      <v-card-text>
        <v-list two-line>
          <v-list-item v-for="(value, key) in productDetail" :key="key">
            <v-list-item-title>{{ formatKey(key) }}</v-list-item-title>
            <v-list-item-subtitle v-if="key !== 'manufacturer'">{{ value }}</v-list-item-subtitle>
            <v-list-item-subtitle v-else>{{ value.firm_name }}</v-list-item-subtitle>
          </v-list-item>
        </v-list>
      </v-card-text>
    </v-card>

    <v-divider class="my-4"></v-divider>

    <v-card>
      <v-card-title>Product Batches</v-card-title>
      <v-card-text>
        <v-row>
          <v-col
              v-for="batch in batches.results" :key="batch.id" cols="12" lg="3"
              md="4"
              sm="6"
          >
            <v-card class="pa-3" outlined>
              <v-card-title>Batch ID: {{ batch.id }}</v-card-title>
              <v-card-subtitle>
                <div>Quantity: {{ batch.quantity }}</div>
                <div>Price: {{ batch.price }}</div>
                <div>Available: {{ batch.is_available ? 'Yes' : 'No' }}</div>
              </v-card-subtitle>
              <v-card-actions>
                <v-btn
                    v-if="batch.is_available"
                    block
                    color="primary"
                    @click="initiateTrade(batch.id)"
                >
                  Trade
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <v-dialog v-model="tradeDialog" max-width="600px">
      <v-card>
        <v-card-title>
          Initiate Trade
        </v-card-title>
        <v-card-text>
          <v-form ref="tradeForm">
            <v-text-field
                v-model="tradeForm.total_amount"
                label="Total Amount"
                required
                type="number"
            ></v-text-field>
          </v-form>
          <v-alert
              v-if="tradeError"
              dense
              type="error"
          >
            {{ tradeError }}
          </v-alert>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" @click="closeDialog">Cancel</v-btn>
          <v-btn color="blue darken-1" @click="submitTrade">Submit</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import api from "@/api";

export default {
  data() {
    return {
      productDetail: {},
      batches: {results: []},
      tradeDialog: false,
      tradeForm: {
        total_amount: '',
        product_batch: null,
      },
      tradeError: ''
    };
  },
  created() {
    this.fetchProductDetail();
    this.fetchProductBatches();
  },
  methods: {
    async fetchProductDetail() {
      try {
        const response = await api.get(`/products/${this.$route.params.id}/`);
        this.productDetail = response.data;
      } catch (error) {
        console.error('There was an error fetching the product detail:', error);
      }
    },
    async fetchProductBatches() {
      try {
        const response = await api.get(`/products/${this.$route.params.id}/batches/`);
        this.batches = response.data;
      } catch (error) {
        console.error('There was an error fetching product batches:', error);
      }
    },
    formatKey(key) {
      return key.split('_').map(k => k.charAt(0).toUpperCase() + k.slice(1)).join(' ');
    },
    initiateTrade(batchId) {
      this.tradeError = '';
      this.tradeForm.product_batch = batchId;
      this.tradeDialog = true;
    },
    async submitTrade() {
      this.tradeError = '';
      try {
        await api.post('/trades/', this.tradeForm);
        this.closeDialog();
      } catch (error) {
        console.error('There was an error posting the trade:', error);
        this.tradeError = 'Failed to submit the trade. Please try again.';
      }
    },
    closeDialog() {
      this.tradeDialog = false;
      this.tradeForm.total_amount = '';
      this.tradeForm.product_batch = null;
    },
  },
};
</script>

<style scoped>
</style>
