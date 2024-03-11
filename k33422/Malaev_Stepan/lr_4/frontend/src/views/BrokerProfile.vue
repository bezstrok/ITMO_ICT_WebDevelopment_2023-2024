<template>
  <v-container v-if="isBroker">
    <v-row>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title class="blue-grey darken-4 white--text">
            Broker Information
          </v-card-title>
          <v-card-text>
            <div class="my-2">
              <v-chip class="ma-2" color="amber" text-color="black">
                <v-icon left>mdi-cash-multiple</v-icon>
                Profit Percentage: {{ brokerInfo.profit_percentage }}%
              </v-chip>
              <v-chip class="ma-2" color="light-blue" text-color="black">
                <v-icon left>mdi-currency-usd</v-icon>
                Fixed Monthly Amount: {{ brokerInfo.fixed_monthly_amount }}
              </v-chip>
            </div>
            <v-card class="mt-4" outlined>
              <v-card-title>
                <v-icon left>mdi-office-building</v-icon>
                Firm Details
              </v-card-title>
              <v-card-text v-if="brokerInfo.firm">
                <div class="d-flex flex-column">
                  <div><strong>Name:</strong> {{ brokerInfo.firm.name }}</div>
                  <div><strong>Address:</strong> {{ brokerInfo.firm.address }}</div>
                  <div><strong>Brokers Count:</strong> {{ brokerInfo.firm.brokers_count }}</div>
                </div>
              </v-card-text>
            </v-card>
          </v-card-text>
        </v-card>
      </v-col>


      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Update Broker Information</v-card-title>
          <v-card-text>
            <v-form>
              <v-text-field v-model="updateForm.profit_percentage" label="Profit Percentage"
                            type="number"></v-text-field>
              <v-text-field v-model="updateForm.fixed_monthly_amount" label="Fixed Monthly Amount"></v-text-field>
              <v-btn color="primary" @click="updateBrokerInfo">Update</v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="blue-grey darken-4 white--text">My Trades</v-card-title>
          <v-card-text>
            <v-data-table
                :footer-props="{
          'items-per-page-options': [5, 10, 15, -1]
        }"
                :headers="headers"
                :items="trades"
                class="elevation-1"
                hide-default-footer
                hover
                item-key="id"
            >
              <template v-slot:item="{ item }">
                <tr @click="goToTradeDetail(item)">
                  <td>{{ item.id }}</td>
                  <td>{{ item.start_time }}</td>
                  <td>{{ item.end_time }}</td>
                  <td>
                    <v-chip :color="statusColor(item.status)" dark small>
                      {{ item.status }}
                    </v-chip>
                  </td>
                  <td>{{ item.total_amount }}</td>
                  <td>{{ item.broker }}</td>
                  <td>{{ item.product }}</td>
                  <td>{{ item.quantity }}</td>
                  <td>
                    <v-btn
                        :disabled="item.status === 'closed'"
                        color="blue"
                        size="small"
                        @click.stop="openEditDialog(item)"
                    >
                      <v-icon>mdi-pencil</v-icon>
                    </v-btn>
                    <v-btn color="red" size="small" @click.stop="deleteTrade(item.id)">
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </td>
                </tr>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>

  <v-container v-else>
    <v-row>
      <v-col cols="12">
        <v-card class="mb-4">
          <v-card-title>Welcome to Your Broker Profile</v-card-title>
          <v-card-text>
            Sorry, but now you are not a broker.
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>

  <v-dialog v-model="editDialog" max-width="600px" persistent>
    <v-card>
      <v-card-title>
        Edit Trade
      </v-card-title>
      <v-card-text>
        <v-form>
          <v-text-field
              v-model="editForm.total_amount"
              label="Total Amount"
              type="number"
          ></v-text-field>
          <v-select
              v-model="editForm.status"
              :items="['open', 'closed', 'pending']"
              label="Status"
          ></v-select>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" @click="closeEditDialog">Cancel</v-btn>
        <v-btn color="blue darken-1" @click="submitEdit">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import api from "@/api";

export default {
  data() {
    return {
      isBroker: false,
      brokerInfo: {},
      updateForm: {
        profit_percentage: null,
        fixed_monthly_amount: '',
        firm: null,
      },
      trades: [],
      headers: [
        {title: 'ID', key: 'id'},
        {title: 'Start Time', key: 'start_time'},
        {title: 'End Time', key: 'end_time'},
        {title: 'Status', key: 'status'},
        {title: 'Total Amount', key: 'total_amount'},
        {title: 'Broker', key: 'broker'},
        {title: 'Product', key: 'product'},
        {title: 'Quantity', key: 'quantity'},
        {title: 'Actions', key: 'actions'},
      ],
      editDialog: false,
      editForm: {
        id: null,
        total_amount: '',
        status: '',
      },
    };
  },
  async created() {
    await this.fetchBrokerInfo();
    await this.fetchBrokerTrades();
    await this.checkUserRole();
  },
  methods: {
    async fetchBrokerInfo() {
      try {
        const response = await api.get('/brokers/me/');
        this.brokerInfo = response.data;
        this.updateForm = {...this.brokerInfo};
      } catch (error) {
        console.error("Error fetching broker information:", error);
      }
    },
    async updateBrokerInfo() {
      try {
        await api.patch('/brokers/me/', this.updateForm);
        // Refresh broker info after update
        await this.fetchBrokerInfo();
      } catch (error) {
        console.error("Error updating broker information:", error);
      }
    },
    statusColor(status) {
      if (status === 'open') return 'green';
      else if (status === 'closed') return 'red';
      return 'grey';
    },
    async fetchBrokerTrades() {
      try {
        const response = await api.get(`/trades/?broker=${this.brokerInfo.id}`);
        this.trades = response.data.results;
      } catch (error) {
        console.error("Error fetching broker's trades:", error);
      }
    },
    goToTradeDetail(item) {
      this.$router.push({name: 'TradeDetail', params: {id: item.id}});
    },
    async deleteTrade(tradeId) {
      try {
        await api.delete(`/trades/${tradeId}/`);
        await this.fetchBrokerTrades();
      } catch (error) {
        console.error('Error deleting trade:', error);
      }
    },
    openEditDialog(trade) {
      this.editDialog = true;
      this.editForm = {...trade};
    },
    closeEditDialog() {
      this.editDialog = false;
    },
    async submitEdit() {
      try {
        await api.patch(`/trades/${this.editForm.id}/`, this.editForm);
        await this.fetchBrokerTrades();
        this.closeEditDialog();
      } catch (error) {
        console.error("Error updating trade:", error);
      }
    },
    async checkUserRole() {
      try {
        const response = await api.get('/auth/users/me/');
        this.isBroker = response.data.is_broker;
      } catch (error) {
        console.error("Error fetching user information:", error);
      }
    },

  },
};
</script>

<style scoped>
</style>
