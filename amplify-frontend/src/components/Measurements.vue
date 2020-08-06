<template>
  <div class="measurements">
    <div class="measurements-flex-child oxygen">
      <p>%SpO<sub>2</sub></p>
      <p v-if="!manual">{{oxygenLevel}}</p>
      <p v-if="manual">
        <input 
          type="number"
          v-model="manualOxygenLevel" 
        />
      </p>
    </div>
  
    <div class="measurements-flex-child bpm">
      <p>PR<sub>bpm</sub><Icon name="heart" scale="2" /></p>
      <p v-if="!manual">{{pulseRate}}</p>
      <p v-if="manual">
        <input 
          type="number" 
          v-model="manualPulseRate" 
        />
      </p>
    </div>
  </div>
</template>

<script>
import 'vue-awesome/icons/heart'
import Icon from 'vue-awesome/components/Icon'

export default {
  name: 'Measurments',
  components: {
    Icon
  },
  data() {
    return {
      manualOxygenLevel: 0,
      manualPulseRate: 0
    }
  },
  watch: { 
    manualOxygenLevel: function(val) { 
      this.$emit('manualoxygenlevels', parseInt(val));
    },
    manualPulseRate: function(val) { 
      this.$emit('manualbpm', parseInt(val));
    }
  },
  props: ['oxygenLevel', 'pulseRate', 'manual'],
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.measurements {
  padding: 0;
  margin: 0;
  font-family: "Tahoma", "Geneva", sans-serif;
  font-size: 200%;
  display: flex;
}

.measurements-flex-child {
    flex: 1;
}  

.oxygen {
  color: #F1948A;
}

.bpm {
  color: #85C1E9;
}

input { 
  border-color:#cccccc; 
  padding:7px; 
  text-align:center; 
  color:#ed1ded; 
  font-size:21px; 
  border-width:2px; 
  border-style:solid;  
  width: 70px;
} 

input:focus { 
  outline:none; 
}

.oxygen input {
  color: #F1948A;
}

.bpm input {
  color: #85C1E9;
}

</style>