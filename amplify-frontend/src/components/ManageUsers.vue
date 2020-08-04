<template>
  <modal name="manage-users" height="auto" width="300" >
    <div class="modal-content">
      <p>Add or remove an authorized viewer.</p>
      <p>
        <input v-model="shared_user" placeholder="some user">
        <Icon class="iconButton" name="user-check" scale="2" v-on:click="share" />
      </p>
      <p v-for="user in users" v-bind:key="user">
        {{user}} <Icon class="iconButton revoke" name="user-times" scale="1" v-on:click="revoke(user)" />
      </p>
    </div>
  </modal>
</template>

<script>

import 'vue-awesome/icons/user-check'
import 'vue-awesome/icons/user-times'
import Icon from 'vue-awesome/components/Icon'

export default {
  name: 'ManageUsers',
  components: {
    Icon
  },
  data() {
    return {
      users: []
    }
  },
  props: ['usersWithAccess'],
  watch: { 
    usersWithAccess: function(val) { 
      this.users = val;
    }
  },
  methods: {
    share: function () {
      let data = {
        action: 'share',
        shared_user: this.shared_user
      }
      this.$emit('action', data)
    },
    revoke: function (user) {
      let data = {
        action: 'revoke',
        shared_user: user
      }
      this.$emit('action', data)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

.modal-content {
  box-sizing: border-box;
  padding: 10px;
  font-size: 13px;
  line-height: 1.5;
  overflow: auto;
}

.iconButton {
  color: #A3E4D7;
  margin: 10px;
  margin-bottom: 0px;
}

.iconButton:active {
  opacity: 1;
  background-color: var(--button-click);
}
.iconButton:hover {
  opacity: 0.7;
}

.revoke {
  color: #F1948A;
}

</style>