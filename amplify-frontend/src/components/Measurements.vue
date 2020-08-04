<template>
  <div class="measurements">
    <div class="measurements-flex-child oxygen">
      <p>%SpO<sub>2</sub></p>
      <p>{{oxygenLevel}}</p>
    </div>
  
    <div class="measurements-flex-child bpm">
      <p>PR<sub>bpm</sub><Icon name="heart" scale="2" /></p>
      <p>{{pulseRate}}</p>
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
  props: ['oxygenLevel', 'pulseRate'],
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

</style>