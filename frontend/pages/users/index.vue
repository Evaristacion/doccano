<template>
  <v-container>
    <!-- Botão para abrir o pop up -->
    <v-btn class="text-capitalize mt-4" color="primary" @click="dialog = true">
      {{ $t("generic.create") }}
    </v-btn>

    <!-- Tabela de Users -->
    <v-data-table
      :value="users"
      :headers="headers"
      :items="users"
      :options.sync="options"
      :server-items-length="total"
      :search="search"
      :loading="isLoading"
      :loading-text="$t('generic.loading')"
      :no-data-text="$t('vuetify.noDataAvailable')"
      :footer-props="{
        showFirstLastPage: true,
        'items-per-page-options': [10, 50, 100],
        'items-per-page-text': $t('vuetify.itemsPerPageText'),
        'page-text': $t('dataset.pageText')
      }"
    item-key="id"
    show-select
  >
    <!-- Barra de Pesquisa -->
    <template #top>
      <v-text-field
        v-model="search"
        :prepend-inner-icon="mdiMagnify"
        :label="$t('generic.search')"
        single-line
        hide-details
        filled
      />
    </template>

    <!-- Slot personalizado para a coluna "Actions" -->
    <template v-slot:[`item.actions`]="{ item }">
      <v-btn color="primary" text @click="openEditDialog(item)">
        {{ $t("generic.edit") }}
      </v-btn>  
      <v-btn color="red" text @click="deleteUser(item.id)">
          {{ $t("generic.delete") }}
        </v-btn>
      </template>
    </v-data-table>


    <!-- Pop Up para Editar Permissões -->
<v-dialog v-model="editDialog" max-width="500px">
  <v-card>
    <v-card-title class="headline">Edit Permissions</v-card-title>
    <v-card-text>
      <v-form ref="editForm">
        <v-checkbox
          v-model="editUser.is_active"
          label="Active"
          hint="Designates whether this user should be treated as active."
          persistent-hint
        />
        <v-checkbox
          v-model="editUser.is_staff"
          label="Staff status"
          hint="Designates whether the user can log into the admin site."
          persistent-hint
        />
        <v-checkbox
          v-model="editUser.is_superuser"
          label="Superuser status"
          hint="Designates that this user has all permissions without explicitly assigning them."
          persistent-hint
        />
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn color="red" text @click="editDialog = false">Cancel</v-btn>
      <v-btn color="primary" @click="savePermissions">Save</v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>

    <!-- Pop Up para Criar User -->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title class="headline">Add User</v-card-title>
        <v-card-text>
          <v-form ref="form">
            <v-text-field 
              v-model="username" 
              label="Username" 
              required
              hint="150 characters or fewer. Letter, digits and @/./+/-/_ only."
              persistent-hint
            />
            <v-text-field 
              v-model="password" 
              label="Password" 
              type="password" 
              required
              hint="Your password can’t be too similar to your other personal information. 
              Your password must contain at least 8 characters. 
              Your password can’t be a commonly used password."
              persistent-hint
            />
            <v-text-field 
              v-model="passwordConfirm" 
              label="Password confirmation" 
              type="password" 
              required
            />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="red" text @click="dialog = false">Cancel</v-btn>
          <v-btn color="primary" @click="saveUser">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
export default {
  layout: "projects",
  middleware: ["check-auth", "auth"],
  data() {
    return {
      editDialog: false,
      editUser: {
      id: null,
      is_active: false,
      is_staff: false,
      is_superuser: false,
    },
      dialog: false,
      users: [],
      headers: [
        { text: "Username", value: "username" },
        { text: "Email Address", value: "email" },
        { text: "First Name", value: "first_name" },
        { text: "Last Name", value: "last_name" },
        { text: "Staff Status", value: "is_staff" },
        { text: "Actions", value: "actions" },
      ],
      username: "",
      email: "",
      first_name: "",
      last_name: "",
      password: "",
      passwordConfirm: "",
      is_staff: false,
    };
  },
  mounted() {
    this.isAdminUserCheck();
    this.fetchUsers();
  },
  methods: {
    openEditDialog(user) {
    this.editUser = {
      id: user.id,
      is_active: user.is_active,
      is_staff: user.is_staff,
      is_superuser: user.is_superuser,
    };
    this.editDialog = true;
  },
  async savePermissions() {
    try {
      await this.$axios.patch(`/v1/users/update/${this.editUser.id}`, this.editUser);
      this.fetchUsers(); // Atualiza a lista de usuários
      this.editDialog = false;
      alert("Permissions updated successfully!");
    } catch (error) {
      console.error("Error updating permissions:", error.response?.data);
      alert("Error: " + JSON.stringify(error.response?.data));
    }
  },
    async fetchUsers() {
      try {
        const response = await this.$axios.get("/v1/users");
        this.users = response.data;
        console.log("Users:", this.users);
      } catch (error) {
        console.error("Error getting users:", error);
      }
    },
    async isAdminUserCheck(){
      const response = await this.$axios.get("/v1/me");
      const user = response.data;
      console.log("User:", user);
      if (!user.is_superuser) {
        alert("You don't have permission to access this page!");
        this.$router.push("/");
      }
    },
    async saveUser() {
      if (this.password !== this.passwordConfirm) {
        alert("The passowrds are different!");
        return;
      }

      try {
        const newUser = {
          username: this.username,
          password1: this.password,
          password2: this.passwordConfirm,
        };
        await this.$axios.post("/v1/users/create", newUser);

        this.fetchUsers();
        this.dialog = false;
        this.username = "";
        this.password = "";
        this.passwordConfirm = "";
        alert("User created with success!");
      } catch (error) {
        console.error("Error creating user:", error.response?.data);
        alert("Error creating user: " + JSON.stringify(error.response?.data));
      }
    },
    async deleteUser(userId) {
      if (confirm("Are you sure you want to delete this user?")) {
        try {
          await this.$axios.delete(`/v1/users/delete/${userId}`);
          this.fetchUsers();
          alert("User deleted successfully!");
        } catch (error) {
          console.error("Error deleting user:", error.response?.data);
          alert("Error deleting user: " + JSON.stringify(error.response?.data));
        }
      }
    }
  },
};
</script>