<template>
  <div class="hello">
    <button class="connect" v-on:click="connect" v-if="!deviceConnected">
    Connect Pulse Oximeter
    </button>
    <button class="disconnect" v-on:click="disconnect" v-if="deviceConnected">
    Disconnect Pulse Oximeter
    </button>
  </div>
</template>

<script>

let receiveCharacteristic;
let device;
let last_bpm, last_spO2


export default {
  name: 'ConnectDevice',
  data() {
    return {
      deviceConnected: false
    }
  },
  methods: {
    connect: function () {
      let self = this;
      let serviceUuid = '49535343-fe7d-4ae5-8fa9-9fafd205e455'
      let options = {
        optionalServices: [serviceUuid],
        filters: [{
            name: 'BerryMed'
          }]}

      console.log('Requesting Bluetooth Device...');

      navigator.bluetooth.requestDevice(options)
      .then(foundDevice => {
        device = foundDevice;
        console.log('Got device', device.name);
        return device.gatt.connect();
      })
      .then(server => {
          console.log('Getting Service...');
          return server.getPrimaryService(serviceUuid);
        })
        .then(service => {
          console.log('Getting Characteristics...');
          return service.getCharacteristics();
        })
        .then(characteristics => {
          console.log('Got Characteristics');
          receiveCharacteristic = characteristics[2];
          receiveCharacteristic.addEventListener('characteristicvaluechanged', self.handleData);
          receiveCharacteristic.startNotifications()
          self.deviceConnected = true;
          device.addEventListener('gattserverdisconnected', self.onDisconnected);
        })
        .catch(error => {
          console.log('Argh! ' + error);
        });
    },
    disconnect: function () {
      receiveCharacteristic = null;
      last_spO2 = null;
      last_bpm = null;
      let self = this;
      
      if (device.gatt.connected) {
        device.gatt.disconnect();
        device == null
        self.deviceConnected = false;
      } else {
        console.log('Bluetooth Device is already disconnected');
      }
    },
    onDisconnected: function (event) {
      console.log(event);
      this.deviceConnected = false;
    },
    handleData: function (event) {
      let self = this
      let receivedData = new Uint8Array(event.target.value.byteLength);
      for (var i = 0; i < event.target.value.byteLength; i++) {
        receivedData[i] = event.target.value.getUint8(i);
      }
      // console.log(receivedData)
      let spO2 = receivedData[4];
      let bpm =  receivedData[8];

      if(spO2 != last_spO2 && spO2 != 127){
        self.$emit('oxygenlevels', spO2);
      }
      
      if(bpm != last_bpm && bpm != 127){
        self.$emit('bpm', bpm);
      }

      last_bpm = bpm;
      last_spO2 = spO2;
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
button {
  min-width: 45px;
  display: inline-block;
  margin-bottom: 0;
  margin: 3px;
  vertical-align: middle;
  touch-action: manipulation;
  cursor: pointer;
  user-select: none;
  color: #fff;
  background-color: #f90;
  border-color: #ccc;
  padding: 5px 5px;
  border: none;
  border-radius: 4px;
}
button:active {
  opacity: 1;
  background-color: var(--button-click);
}
button:hover {
  opacity: 0.8;
}

.connect {
  background-color: #85C1E9;
}

.disconnect {
  background-color: #F1948A;
}
</style>