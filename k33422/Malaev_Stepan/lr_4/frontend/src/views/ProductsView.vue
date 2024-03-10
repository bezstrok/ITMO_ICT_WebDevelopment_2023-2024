<template>
  <v-container>
    <v-data-table
        :headers="headers"
        :items="products"
        item-key="id"
        class="elevation-1"
        :footer-props="{
        'items-per-page-options': [5, 10, 15, -1]
      }"
        hide-default-footer
        hover
    >
      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title>Products Overview</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="addProduct">Add Product</v-btn>
        </v-toolbar>
      </template>
      <template v-slot:item="{ item }">
        <tr @click="goToProductDetail(item)">
          <td>{{ item.id }}</td>
          <td>{{ item.name }}</td>
          <td>{{ item.unique_code }}</td>
          <td>{{ item.category }}</td>
          <td>{{ item.weight }} {{ item.measurement_unit }}</td>
          <td>{{ item.production_date }}</td>
          <td>{{ item.expiry_date }}</td>
          <td>{{ item.manufacturer }}</td>
        </tr>
      </template>
    </v-data-table>

    <v-dialog v-model="showAddProductDialog" max-width="600px">
      <v-card>
        <v-card-title>
          Add Product
        </v-card-title>
        <v-card-text>
          <v-form>
            <v-text-field v-model="newProduct.name" label="Name" required></v-text-field>
            <v-text-field v-model="newProduct.category" label="Category" required></v-text-field>
            <v-text-field v-model="newProduct.weight" label="Weight" type="number" required></v-text-field>
            <v-text-field v-model="newProduct.production_date" label="Production Date" type="date"
                          required></v-text-field>
            <v-text-field v-model="newProduct.expiry_date" label="Expiry Date" type="date" required></v-text-field>
            <v-text-field v-model="newProduct.measurement_unit" label="Measurement Unit" required></v-text-field>
          </v-form>

          <v-alert
              v-if="productAddError"
              type="error"
              class="mb-3"
          >
            {{ productAddError }}
          </v-alert>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="red darken-1" @click="closeAddProductDialog">Cancel</v-btn>
          <v-btn color="green darken-1" @click="submitNewProduct">Save</v-btn>
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
      products: [],
      headers: [
        {title: 'ID', key: 'id'},
        {title: 'Name', key: 'name'},
        {title: 'Unique Code', key: 'unique_code'},
        {title: 'Category', key: 'category'},
        {title: 'Weight', key: 'weight'},
        {title: 'Production Date', key: 'production_date'},
        {title: 'Expiry Date', key: 'expiry_date'},
        {title: 'Manufacturer', key: 'manufacturer'},
      ],
      showAddProductDialog: false,
      newProduct: {
        name: '',
        category: '',
        weight: 0,
        production_date: '',
        expiry_date: '',
        measurement_unit: '',
      },
      productAddError: '',
    };
  },
  created() {
    this.fetchProducts();
  },
  methods: {
    async fetchProducts() {
      try {
        const response = await api.get('/products/');
        this.products = response.data.results;
      } catch (error) {
        console.error('There was an error fetching the products:', error);
      }
    },
    goToProductDetail(item) {
      this.$router.push({name: 'ProductDetail', params: {id: item.id}});
    },
    addProduct() {
      this.productAddError = '';
      this.showAddProductDialog = true;
    },
    closeAddProductDialog() {
      this.showAddProductDialog = false;
      this.resetNewProductForm();
    },
    resetNewProductForm() {
      this.newProduct = {
        name: '',
        category: '',
        weight: 0,
        production_date: '',
        expiry_date: '',
        measurement_unit: '',
      };
    },
    async submitNewProduct() {
      this.productAddError = '';
      try {
        await api.post('/products/', this.newProduct);
        this.closeAddProductDialog();
        this.fetchProducts();
      } catch (error) {
        console.error('There was an error posting the new product:', error);

        if (error.response && error.response.data) {
          this.productAddError = error.response.data.detail || 'Failed to add the product. Please try again.';
        }
      }
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

</style>