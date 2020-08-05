<template>
  <div class="userData">
    <div class="bluetoothElements">
      <ConnectDevice @bpm="onBPMChange" @oxygenlevels="onOxygenChange" />
      <Measurements 
        v-bind:oxygen-level="current_oxygen_level"
        v-bind:pulse-rate="current_pulse_rate"
      />
    </div>
    <div class="data-controls">
      <div class="data-controls-child upload">
        <Icon class="iconButton" name="cloud-upload-alt" scale="3" v-on:click="addLevels" />
      </div>
      <div class="data-controls-child sharedUsers">
        Show data for: 
        <select v-model="selected_user">
          <option v-for="user in shared_users" v-bind:key="user">
            {{ user }}
          </option>
        </select>
      </div>
      <div class="data-controls-child refresh">
        <Icon class="iconButton" name="sync" scale="2" v-on:click="fetchLevels" />
      </div>
      <div class="data-controls-child share">
        <ManageUsers 
          @action="shareWithUser" 
          v-bind:users-with-access="users_with_access"
        />
        <Icon class="iconButton" name="share" scale="3" v-on:click="$modal.show('manage-users')" />
      </div>
    </div>
    
    <HistoricalChart 
      v-bind:history="history"
    />
  </div>
</template>

<script>
import 'vue-awesome/icons/sync'
import 'vue-awesome/icons/share'
import 'vue-awesome/icons/cloud-upload-alt'
import ManageUsers from './ManageUsers.vue'
import Measurements from './Measurements.vue'
import Icon from 'vue-awesome/components/Icon'
import ConnectDevice from './ConnectDevice.vue'
import HistoricalChart from './HistoricalChart.vue'


import { API, Auth } from 'aws-amplify'

let apiName = 'OxygenMonitorApi';

export default {
  name: 'Interface',
  components: {
    Icon,
    ManageUsers,
    Measurements,
    ConnectDevice,
    HistoricalChart
  },
  data() {
    return {
      history: {
        oxygen_levels: [],
        pulse_rates: [],
        timestamps: []
      },
      username: "",
      selected_user: "",
      shared_users: [],
      users_with_access: [],
      current_oxygen_level: '--',
      current_pulse_rate: '--'
    }
  },
  async mounted() {
    let credentials = await Auth.currentAuthenticatedUser()
    let currentUser = credentials.username
    this.username = currentUser;
    this.selected_user = currentUser;
    this.shared_users = [currentUser];
    this.fetchLevels();
    this.getSharedUsers();
    this.getUsersWithAccess();
  },
  methods: {
    addLevels: async function () {
      this.selected_user = this.username;
      if(this.current_oxygen_level == '--' || this.current_pulse_rate == '--'){
        return;
      }

      let path = '/levels';
      let myInit = {
        body: {
          oxygen_level: this.current_oxygen_level,
          bpm: this.current_pulse_rate
        }
      }

      await API.post(apiName, path, myInit);
      return this.getLevels()
    },
    fetchLevels: function () {
      if (this.selected_user == this.username) {
        this.getLevels();
      }else {
        this.getsharedUserLevels();
      }
    },
    getLevels: function () {
      let path = '/levels';

      API
        .get(apiName, path, {})
        .then(response => {
          this.history = response;
        })
        .catch(error => {
          console.log(error.response);
        });
    },
    getsharedUserLevels: function () {
      let path = '/levels/shared';
      let myInit = {
        body: {
          shared_user: this.selected_user
        }
      }
      
      API
        .post(apiName, path, myInit)
        .then(response => {
          this.history = response
        })
        .catch(error => {
          console.log(error.response);
        });
    },
    shareWithUser: function (data) {
      let path = '/access';
      let self = this;
      let myInit = {
        body: data
      }
      API
        .post(apiName, path, myInit)
        .then(response => {
          console.log(response);
          self.getUsersWithAccess();
        })
        .catch(error => {
          console.log(error.response);
        });
    },
    getSharedUsers: function () {
      let path = '/access/shared';
      let self = this;
  
      API
        .get(apiName, path, {})
        .then(response => {
          self.shared_users = response.shared_users;
          self.selected_user = response.shared_users[0];
        })
        .catch(error => {
          console.log(error.response);
        });
    },
    getUsersWithAccess: function () {
      let path = '/access/users';
      let self = this;
  
      API
        .get(apiName, path, {})
        .then(response => {
          self.users_with_access = response.users_with_access;
        })
        .catch(error => {
          console.log(error.response);
        });
    },
    onBPMChange(value) {
      console.log("BPM: " + value) // someValue
      this.current_pulse_rate = value;
    },
    onOxygenChange(value) {
      console.log("Oxygen: " + value) // someValue
      this.current_oxygen_level = value;
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.button-container {
  padding: 0;
  margin: 0;
  display: flex;
}

.data-controls {
  padding: 0;
  margin: 0;
  font-family: "Tahoma", "Geneva", sans-serif;
  display: flex;
}

.data-controls-child {
    flex: 1;
}  

.iconButton {
  color: #f90;
}

.iconButton:active {
  opacity: 1;
  background-color: var(--button-click);
}
.iconButton:hover {
  opacity: 0.7;
}
    
</style>