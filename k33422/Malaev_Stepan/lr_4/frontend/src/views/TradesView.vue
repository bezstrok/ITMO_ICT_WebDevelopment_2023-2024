<template>
  <v-container>
    <v-data-table
        :headers="headers"
        :items="trades"
        item-key="id"
        class="elevation-1"
        :footer-props="{
          'items-per-page-options': [5, 10, 15, -1]
        }"
        hide-default-footer
        hover
    >
      <template v-slot:top>
        <v-toolbar flat color="white">
          <v-toolbar-title>Trades Overview</v-toolbar-title>
          <v-spacer></v-spacer>
        </v-toolbar>
      </template>
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
        </tr>
      </template>
    </v-data-table>
  </v-container>
</template>


<script>
import api from "@/api";

export default {
  data() {
    return {
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
      ],
    };
  },
  created() {
    this.fetchTrades();
  },
  methods: {
    async fetchTrades() {
      try {
        const response = await api.get('/trades/');
        this.trades = response.data.results;
      } catch (error) {
        console.error('There was an error fetching the trades:', error);
      }
    },
    statusColor(status) {
      if (status === 'open') return 'green';
      else if (status === 'closed') return 'red';
      return 'grey';
    },
    goToTradeDetail(item) {
      this.$router.push({name: 'TradeDetail', params: {id: item.id}});
    },
  },
};
</script>

<style scoped>
.elevation-1 {
  border-radius: 8px;
  overflow: hidden;
}

.v-data-table-header th {
  background-color: #F5F5F5;
  color: #424242;
  font-weight: bold;
}

.v-data-table .v-data-table__wrapper table {
  border-collapse: separate;
  border-spacing: 0 10px;
}

.v-data-table .v-data-table__wrapper table tbody tr {
  background-color: #FFFFFF;
}

.v-chip {
  font-size: 0.875rem;
}

</style>
