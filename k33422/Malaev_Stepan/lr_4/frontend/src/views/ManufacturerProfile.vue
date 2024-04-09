<template>
  <v-container v-if="isManufacturer">
    <v-row>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title class="blue-grey darken-4 white--text">Manufacturer Information</v-card-title>
          <v-card-text>
            <div class="my-2">
              <v-chip class="ma-2" color="green" text-color="white">
                <v-icon left>mdi-cube-scan</v-icon>
                Products Count: {{ manufacturerInfo.products_count }}
              </v-chip>
            </div>
            <v-card class="mt-4" outlined>
              <v-card-title>
                <v-icon left>mdi-factory</v-icon>
                Details
              </v-card-title>
              <v-card-text>
                <div class="d-flex flex-column">
                  <div><strong>Firm Name:</strong> {{ manufacturerInfo.firm_name }}</div>
                  <div><strong>Address:</strong> {{ manufacturerInfo.address }}</div>
                  <div><strong>Contact Info:</strong> {{ manufacturerInfo.contact_info }}</div>
                </div>
              </v-card-text>
            </v-card>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Update Manufacturer Information</v-card-title>
          <v-card-text>
            <v-form ref="updateManufacturerForm">
              <v-text-field
                  v-model="updateForm.address"
                  label="Address"
                  required
              ></v-text-field>

              <v-text-field
                  v-model="updateForm.contact_info"
                  label="Contact Info"
                  required
              ></v-text-field>

              <v-btn color="primary" @click="updateManufacturerInfo">
                Update
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>


    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-text>
            <v-data-table
                :footer-props="{
                'items-per-page-options': [5, 10, 15, -1]
              }"
                :headers="headers"
                :items="products"
                class="elevation-1"
                hide-default-footer
                hover
                item-key="id"
            >
              <template v-slot:top>
                <v-toolbar flat>
                  <v-toolbar-title>My Products</v-toolbar-title>
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
                  <td>
                    <v-btn
                        :disabled="item.status === 'closed'"
                        color="blue"
                        size="small"
                        @click.stop="openEditDialog(item)"
                    >
                      <v-icon>mdi-pencil</v-icon>
                    </v-btn>
                    <v-btn color="red" size="small" @click.stop="deleteProduct(item.id)">
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

    <v-dialog v-model="showAddProductDialog" max-width="600px">
      <v-card>
        <v-card-title>
          Add Product
        </v-card-title>
        <v-card-text>
          <v-form>
            <v-text-field v-model="newProduct.name" label="Name" required></v-text-field>
            <v-text-field v-model="newProduct.category" label="Category" required></v-text-field>
            <v-text-field v-model="newProduct.weight" label="Weight" required type="number"></v-text-field>
            <v-text-field v-model="newProduct.production_date" label="Production Date" required
                          type="date"></v-text-field>
            <v-text-field v-model="newProduct.expiry_date" label="Expiry Date" required type="date"></v-text-field>
            <v-text-field v-model="newProduct.measurement_unit" label="Measurement Unit" required></v-text-field>
          </v-form>

          <v-alert
              v-if="productAddError"
              class="mb-3"
              type="error"
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

    <v-dialog v-model="editDialog" max-width="600px">
      <v-card>
        <v-card-title>
          Edit Product
        </v-card-title>
        <v-card-text>
          <v-form>
            <v-text-field v-model="newProduct.name" label="Name" required></v-text-field>
            <v-text-field v-model="newProduct.category" label="Category" required></v-text-field>
            <v-text-field v-model="newProduct.weight" label="Weight" required type="number"></v-text-field>
            <v-text-field v-model="newProduct.production_date" label="Production Date" required
                          type="date"></v-text-field>
            <v-text-field v-model="newProduct.expiry_date" label="Expiry Date" required type="date"></v-text-field>
            <v-text-field v-model="newProduct.measurement_unit" label="Measurement Unit" required></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" @click="closeEditDialog">Cancel</v-btn>
          <v-btn color="blue darken-1" @click="submitEdit">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>

  <v-container v-else>
    <v-row>
      <v-col cols="12">
        <v-card class="mb-4">
          <v-card-title>Welcome to Your Manufacturer Profile</v-card-title>
          <v-card-text>
            Sorry, but now you are not a manufacturer.
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
      isManufacturer: false,
      manufacturerInfo: {},
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
        {title: 'Actions', key: 'actions'},
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
      editDialog: false,
      editForm: {
        id: null,
        name: '',
        category: '',
        weight: 0,
        production_date: '',
        expiry_date: '',
        measurement_unit: '',
      },
      updateForm: {
        address: '',
        contact_info: '',
      },
    };
  },
  async created() {
    await this.fetchManufacturerInfo();
    await this.fetchProducts();
    await this.checkUserRole();
  },
  methods: {
    async fetchManufacturerInfo() {
      try {
        const response = await api.get('/manufacturers/me/');
        this.manufacturerInfo = response.data;
        this.updateForm = {...this.manufacturerInfo};
      } catch (error) {
        console.error("Error fetching manufacturer information:", error);
      }
    },
    async fetchProducts() {
      try {
        const response = await api.get(`/products/?manufacturer=${this.manufacturerInfo.id}`);
        this.products = response.data.results;
      } catch (error) {
        console.error("Error fetching manufacturer's trades:", error);
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
    openEditDialog(product) {
      this.editDialog = true;
      this.editForm = {...product};
    },
    closeEditDialog() {
      this.editDialog = false;
    },
    async submitEdit() {
      try {
        await api.patch(`/products/${this.editForm.id}/`, this.editForm);
        await this.fetchProducts();
        this.closeEditDialog();
      } catch (error) {
        console.error("Error updating trade:", error);
      }
    },
    async deleteProduct(tradeId) {
      try {
        await api.delete(`/products/${tradeId}/`);
        await this.fetchProducts();
      } catch (error) {
        console.error('Error deleting trade:', error);
      }
    },
    async updateManufacturerInfo() {
      try {
        await api.patch('/manufacturers/me/', this.updateForm);
        await this.fetchManufacturerInfo();
      } catch (error) {
        console.error("Error updating manufacturer information:", error);
      }
    },
    async checkUserRole() {
      try {
        const response = await api.get('/auth/users/me/');
        this.isManufacturer = response.data.is_manufacturer;
      } catch (error) {
        console.error("Error fetching user information:", error);
      }
    },
  },
};
</script>

<style scoped>
.my-2, .ma-2, .mt-4 {
  margin: auto;
}

.d-flex.flex-column {
  display: flex;
  flex-direction: column;
}

.v-icon {
  margin-right: 8px;
}
</style>
