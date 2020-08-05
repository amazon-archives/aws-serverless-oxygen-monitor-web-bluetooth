<template>
  <div class="historicalChart">
    <TrendChart
      :datasets="datasets"
      :grid="grid"
      :labels="labels"
      :min="0"
      padding="5"
      :interactive="true"
      @mouse-move="onMouseMove"
      class="historical-chart"
      v-if="datasets.length"
    ></TrendChart>
    <div id="pop" role="tooltip" ref="tooltip" class="tooltip" :class="{'is-active': tooltipData}">
      <div class="tooltip-container" v-if="tooltipData">
        <strong>{{labels.xLabels[tooltipData.index]}}</strong>
        <div class="tooltip-data">
          <div class="tooltip-data-item tooltip-data-item--1"><p>SpO<sub>2</sub></p>: {{tooltipData.data[0]}}</div>
          <div class="tooltip-data-item tooltip-data-item--2">BPM/PR: {{tooltipData.data[1]}}</div>
        </div>
        <p>{{tooltipData.data[2]}}</p>
      </div>
    </div>
  </div>
</template>

<script>
import TrendChart from "vue-trend-chart";
import Popper from "popper.js";

export default {
  name: 'HistoricalChart',
  components: {
    TrendChart
  },
  data() {
    return {
      datasets: [
        {
          data: [0,127],
          smooth: true,
          showPoints: true,
          fill: true,
          className: "oxygenlevels"
        },
        {
          data: [0,99],
          smooth: true,
          showPoints: true,
          className: "pulserate"
        }
      ],
      grid: {
        verticalLines: true,
        horizontalLines: true
      },
      labels: {
        xLabels: ["0/00/0000, 00:00:00 PM", "0/00/0000, 00:00:01 PM"],
        yLabels: 5,
        yLabelsTextFormatter: val => Math.round(val * 100) / 100
      },
      tooltipData: null,
      popper: null,
      popperIsActive: false,
      timestamps: [0, 1]
    };
  },
  props: ['history'],
  watch: { 
    history: function(val) { 
      let oxygen_levels = val.oxygen_levels;
      let pulse_rates = val.pulse_rates;
      let timestamps = val.timestamps;

      if(oxygen_levels.length != 0){
        if(oxygen_levels.length < 2){
          this.datasets[0].data = [0,oxygen_levels[0]];
        }else {
          this.datasets[0].data = oxygen_levels;
        }
      }

      if(pulse_rates.length != 0){
        if(pulse_rates.length < 2){
          this.datasets[1].data = [0,pulse_rates[0]];
        }else {
          this.datasets[1].data = pulse_rates;
        }
      }

      if(timestamps.length != 0){
        this.timestamps = timestamps;
        let tsLength = timestamps.length
        if( tsLength > 1){
          this.labels.xLabels[0] = new Date(timestamps[0]).toLocaleString();
          this.labels.xLabels[1] = new Date(timestamps[tsLength - 1]).toLocaleString();
        }else {
          this.labels.xLabels[0] = "0/00/0000, 00:00:00 PM";
          this.labels.xLabels[1] = new Date(timestamps[0]).toLocaleString();
          this.timestamps = [1,timestamps[0]];
        }
      }    
    }
  },
  methods: {
    initPopper() {
      const chart = document.querySelector(".historical-chart");
      const ref = chart.querySelector(".active-line");
      const tooltip = this.$refs.tooltip;
      this.popper = new Popper(ref, tooltip, {
        placement: "right",
        modifiers: {
          offset: { offset: "0,10" },
          preventOverflow: {
            boundariesElement: chart
          }
        }
      });
    },
    onMouseMove(params) {
      this.popperIsActive = !!params;
      this.popper.scheduleUpdate();
  
      params.data[2] = new Date(this.timestamps[params.index]).toLocaleString()
      this.tooltipData = params || null;
    }
  },
  mounted() {
    this.initPopper();
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
* {
  box-sizing: border-box;
}
strong {
  font-weight: 600;
}
body {
  padding: 0;
  margin: 0;
  font-family: "Source Sans Pro", sans-serif;
  color: #2f4053;
}
#app {
  margin: 0 auto;
  max-width: 699px;
}
.historicalChart {
  width: 100%;
}
.historicalChart .vtc {
  height: 250px;
  font-size: 12px;
}
@media (min-width: 699px) {
  .historicalChart .vtc {
    height: 320px;
  }
}
.historicalChart .labels {
  stroke: rgba(0, 0, 0, 0.05);
}
.historicalChart .active-line {
  stroke: rgba(0, 0, 0, 0.2);
}
.historicalChart .point {
  stroke-width: 2;
  transition: stroke-width 0.2s;
}
.historicalChart .point.is-active {
  stroke-width: 5;
}
.historicalChart .oxygenlevels .stroke {
  stroke: #F1948A;
  stroke-width: 2;
}
.historicalChart .oxygenlevels .fill {
  fill: #F1948A;
  opacity: 0.05;
}
.historicalChart .oxygenlevels .point {
  fill: #F1948A;
  stroke: #F1948A;
}
.historicalChart .pulserate .stroke {
  stroke: #85C1E9;
  stroke-width: 2;
}
.historicalChart .pulserate .point {
  fill: #85C1E9;
  stroke: #85C1E9;
}

.historicalChart .tooltip {
  padding: 10px;
  background: #fff;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
  pointer-events: none;
}
.historicalChart .tooltip:not(.is-active) {
  display: none;
}
.historicalChart .tooltip-data {
  display: flex;
}
.historicalChart .tooltip-data-item {
  display: flex;
  align-items: center;
}
.historicalChart .tooltip-data-item:not(:first-child) {
  margin-left: 20px;
}
.historicalChart .tooltip-data-item:before {
  content: "";
  display: block;
  width: 15px;
  height: 15px;
  margin-right: 5px;
}
.historicalChart .tooltip-data-item--1:before {
  background: #F1948A;
}
.historicalChart .tooltip-data-item--2:before {
  background: #85C1E9;
}

</style>