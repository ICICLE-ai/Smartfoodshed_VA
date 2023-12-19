<template>
  <v-app>
    <v-app-bar app>
      <v-app-bar-nav-icon
        variant="text"
        @click.stop="drawer = !drawer"
      ></v-app-bar-nav-icon>
      <v-toolbar-title>ICICLE Visual Analytics V1</v-toolbar-title>
      <!-- <v-spacer></v-spacer> -->
      <div style="width: 14%; margin-left: 50%">
        <v-select
          v-model="selected_dataset"
          variant="solo"
          hint="Select A Dataset"
          persistent-hint
          :items="['ppod', 'cfs']"
        ></v-select>
      </div>
    </v-app-bar>

    <v-navigation-drawer :key="drawerKey" v-model="drawer" temporary app left>
      <v-layout column justify-center v-model="loggedIn">
        <p class="black--text subheading mt-1">
          {{ this.getCookieByName("username") }}
        </p>
      </v-layout>
      <v-list>
        <template v-for="item in items">
          <v-list-item
            :key="item.value"
            v-if="checkVisible(item.label)"
            @click="ClickEvent(item.value)"
          >
            <v-list-item-icon
              ><v-icon>{{ item.icon }}</v-icon></v-list-item-icon
            >
            <v-list-item-title>{{ item.label }}</v-list-item-title>
          </v-list-item>
        </template>
      </v-list>
    </v-navigation-drawer>
    <v-dialog v-model="dialog_load" max-width="600px" scrollable>
      <v-card>
        <v-card-title class="text-h5">
          Select a Source
          <v-btn @click="loadData" :loading="dialog_load_loading">Load</v-btn>
          <v-btn @click="deleteData" :loading="dialog_delete_loading"
            >Delete</v-btn
          >
        </v-card-title>
        <v-card-text>
          <v-data-table
            @click:row="rowClick"
            single-select
            item-key="uuid"
            :headers="tableHeaders"
            :loading="tableLoading"
            loading-text="Loading... Please wait"
            :items="tableData"
            :items-per-page="5"
            scrollable
            class="elevation-1"
          >
          </v-data-table>
        </v-card-text>
      </v-card>
    </v-dialog>

    <v-dialog v-model="dialog_save" max-width="600px" persistent scrollable>
      <v-card>
        <v-card-title>Dataset Profile</v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  label="Dataset Title"
                  required
                  v-model="inputDataTitle"
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12">
                <v-checkbox
                  v-model="publicData"
                  label="Public Data"
                ></v-checkbox>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="dialog_save = false">
            Close
          </v-btn>
          <v-btn
            color="blue darken-1"
            text
            @click="saveCloudData"
            :loading="dialog_save_loading"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="show_alert" max-width="300px">
      <v-alert :color="alertInfo.alert_color" variant="tonal" closable>
        {{ alertInfo.alert_text }}
      </v-alert>
    </v-dialog>

    <dashboard ref="dashboard" />
  </v-app>
</template>

<script>
import { mapState } from "vuex";
import Dashboard from "@/views/Dashboard.vue";
import axios from "axios";
import { getItemIndex } from "./utils/storehelp";
import { base_request_url, cloud_url } from "@/utils/base_url";
export default {
  data() {
    return {
      publicData: false,
      drawerKey: 0,
      selected_dataset: "ppod",
      load: false,
      drawer: false,
      items: [
        {
          value: "LogIn",
          label: "Log In",
          icon: "mdi-login",
        },
        {
          value: "LogOut",
          label: "Log Out",
          icon: "mdi-logout",
        },
        {
          value: "SaveData",
          label: "Save Data",
          icon: "mdi-cloud-upload",
        },
        {
          value: "LoadData",
          label: "Load Data",
          icon: "mdi-cloud-download",
        },
      ],
      tableHeaders: [
        {
          text: "Title",
          value: "title",
        },
        {
          text: "Owner",
          value: "owner",
        },
      ],
      tableData: [],
      tableLoading: false,

      inputDataTitle: "", // save data form
      alertInfo: {
        alert_color: "success",
        alert_title: "Successfully saved!",
        alert_text: "The uuid for saved data is:",
      },
      show_alert: false,
      loggedIn: false,
      selectedRow: undefined,
      dialog_save_loading: false,
      dialog_load_loading: false,
      dialog_delete_loading: false,
      dialog_load: false,
      dialog_save: false,
    };
  },
  components: {
    Dashboard,
  },
  methods: {
    forceRerender() {
      this.drawerKey += 1;
    },
    checkVisible(ele) {
      let visible = true;
      if (this.getCookieByName("token") == null) {
        // Not logged in
        if (ele == "Log Out" || ele == "Save Data") visible = false;
      } else {
        // Logged in
        if (ele == "Log In") {
          visible = false;
        }
      }
      return visible;
    },
    rowClick: function (item, row) {
      row.select(true);
      this.selectedRow = item;
    },
    // click save to save data to cloud
    getCookieByName(name) {
      const cookies = document.cookie.split(";"); // Split cookies by semicolon
      for (const cookie of cookies) {
        const [cookieName, cookieValue] = cookie.trim().split("=");
        if (cookieName === name) {
          return decodeURIComponent(cookieValue); // Return decoded value
        }
      }
      return null; // Return null if cookie not found
    },
    // Delete cookie
    deleteCookieByName(name) {
      document.cookie =
        name +
        "=; Path=/; Domain=" +
        process.env.VUE_APP_COOKIE_DOMAIN +
        "; Expires=" +
        new Date(0).toUTCString() +
        ";";
    },
    saveCloudData() {
      const savedState = this.$store.state;

      var dataToSave = {
        title: this.inputDataTitle,
        owner: this.getCookieByName("username"), // TODO : to be dynamic
        json_data: savedState,
      };

      const config = {
        headers: {
          authorization: `Token ${this.getCookieByName("token")}`,
          public: this.publicData.toUTCString(),
        },
      };
      axios
        .post(cloud_url + "api/storage/json-object/create/", dataToSave, config)
        .then((response) => {
          this.alertInfo = {
            alert_color: "success",
            alert_title: "Successfully saved!",
            alert_text: "The uuid for saved data is: " + response.data.uuid,
          };
          // console.log(this.alertInfo)
          this.dialog_save_loading = false; // end spinning
          this.dialog_save = false; // hide the dialog
          this.show_alert = true; // show notification
        })
        .catch((error) => {
          this.alertInfo = {
            alert_color: "error",
            alert_title: "Error occured!",
            alert_text: error,
          };
          this.dialog_save_loading = false;
          this.dialog_save = false;
          this.show_alert = true;
        });
      this.publicData = false;
    },
    // click load to load data from cloud
    loadData() {
      // fetch the data
      this.dialog_load_loading = true;
      axios
        .get(
          cloud_url +
            "api/storage/json-object/" +
            this.selectedRow["uuid"] +
            "/"
        )
        .then((result) => {
          var temp = result["data"]["json_data"];
          temp["resetMode"] = true;
          this.$store.dispatch("resetState", temp);
          this.dialog_load_loading = false;
          this.dialog_load = false;
        });
    },
    deleteData() {
      this.dialog_delete_loading = true;
      axios
        .get(cloud_url + "api/storage/delete/" + this.selectedRow["uuid"] + "/")
        .then(() => {
          this.dialog_delete_loading = false;
          this.dialog_load = false;
        });
    },
    //change database
    async fetchData() {
      this.$store.dispatch("changeDB", { database: this.selected_dataset });
    },
    // click the left navigation panel
    async ClickEvent(clickedItem) {
      switch (clickedItem) {
        case "LogIn":
          // login event
          if (this.getCookieByName("token") == null) {
            await this.$store.dispatch("logIn");
            this.items[1]["visible"] = true; //Shows logout
            this.items[2]["visible"] = true; //Shows to save data
            this.loggedIn = true;
          }
          break;
        case "SaveData":
          // get the state data
          this.dialog_save = true;
          break;
        case "LoadData":
          this.dialog_load = true;
          this.tableLoading = true;
          if (this.getCookieByName("token") == null) {
            axios
              .get(cloud_url + "api/storage/json-objects-public/")
              .then((result) => {
                this.tableData = result["data"].map((obj) => {
                  return {
                    ...obj,
                  };
                });
              });
          } else {
            const config = {
              headers: {
                authorization: `Token ${this.getCookieByName("token")}`,
              },
            };
            axios
              .get(cloud_url + "api/storage/json-objects/", config)
              .then((result) => {
                this.tableData = result["data"].map((obj) => {
                  return {
                    ...obj, // Copy all key-value pairs from the original object
                  };
                });
              });
          }
          this.tableLoading = false;
          break;
        case "LogOut":
          this.deleteCookieByName("username");
          this.deleteCookieByName("token");
          this.items[1]["visible"] = false; // hide the log out button
          this.items[2]["visible"] = false; //hide the save data button
          this.loggedIn = false; // Show option to log in again
          this.forceRerender(); // rerender the navigation drawer
          break;
        default:
          break;
      }
    },
  },
  created() {
    this.load = true;
  },
  watch: {
    selectedRow: function () {
      console.log("select changes");
    },
    load: function () {
      this.fetchData();
    },
    selected_dataset: function () {
      // window.location.reload();
      // d3.select('#div_graph').html('')
      this.fetchData();
    },
    loginRedirect: function () {
      // alert(this.loginRedirect)
      if (this.loginRedirect != "/") {
        window.location.href = this.loginRedirect;
      }
    },
  },
  computed: {
    ...mapState(["BETA_ROUTE", "DASH_ROUTE", "loginRedirect"]),
    versionPrompt() {
      const currentRoute = this.$route.name;
      if (currentRoute == this.DASH_ROUTE.name) {
        return "Try Dashboard Beta";
      } else {
        return "Old Version";
      }
    },
  },
};
</script>

<style>
tr.v-data-table__selected {
  background: #7d92f5 !important;
}
/* .svg-canvas{
    position: absolute; 
    width: 100%; 
    height: 100%;
    z-index: -1;
  } */
</style>
