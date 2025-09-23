<template>
  <div class="page detect">
    <side-panel/>

    <div class="looper"></div>

    <section class="panel-wrap">
      <div class="panel">
        <header class="head">
          <h2 class="title">AI Detection Bar</h2>
        </header>

        <p class="sub">The voice is likely cloned or modified using AI.</p>

        <div class="chart-row">
          <div class="donut">
            <svg :width="size" :height="size" :viewBox="`0 0 ${size} ${size}`" role="img"
                 aria-label="AI detection progress">
              <defs>
                <linearGradient :id="gradId" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%"  stop-color="#A855F7"/>
                  <stop offset="100%" stop-color="#3B82F6"/>
                </linearGradient>
              </defs>

              <circle
                  :cx="center" :cy="center" :r="radius"
                  :stroke="`url(#${gradId})`"
                  :stroke-width="stroke"
                  fill="none"
                  stroke-linecap="butt"
                  :stroke-dasharray="ringDash"
                  :stroke-dashoffset="dashOffset"
                  :transform="rotate"
              />

              <circle
                  :cx="center" :cy="center" :r="radius"
                  stroke="#ffffff"
                  :stroke-width="stroke"
                  fill="none"
                  stroke-linecap="butt"
                  :stroke-dasharray="gapDash"
                  :stroke-dashoffset="dashOffset"
                  :transform="rotate"
              />
            </svg>

            <div class="center-text">
              <div class="line1">Completed</div>
              <div class="line2">{{ score }}%</div>
            </div>
          </div>
          <div class="spacer"></div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import SidePanel from '@/components/SidePanel.vue';

export default {
  name: 'DetectionResult',
  components: {SidePanel},
  props: {
    score: {type: Number, default: 39}
  },
  data() {
    const size = 466;
    const stroke = 48;
    const center = size / 2;
    const radius = (size - stroke) / 2;
    const circum = 2 * Math.PI * radius;
    return {
      size, stroke, center, radius, circum,
      gradId: 'grad-donut-' + Math.random().toString(36).slice(2, 8),
      bgId: 'grad-bg-' + Math.random().toString(36).slice(2, 8),
      rotate: `rotate(-90 ${center} ${center})`,
      gapRatio: 0.06
    };
  },
  computed: {
    dashProgress() {
      const gap = this.circum * this.gapRatio;
      const effective = this.circum - gap;
      const show = Math.max(0, Math.min(1, this.score / 100)) * effective;
      const hide = this.circum - show;
      return `${show} ${hide}`;
    },
    gapDash() {
      const gap = this.circum * this.gapRatio;
      return `${gap} ${this.circum}`;
    }
  }
};
</script>

<style lang="scss" scoped>
$bg: #0A0A0A;
$panel: #000;
$border: rgba(255, 255, 255, .08);
$text: #E6E8EB;

.detect {
  min-height: 100vh;
  background: $bg;
  color: $text;
}

.panel-wrap {
  padding-left: 72px;
}

@media (min-width: 992px) {
  .side.expanded + .looper + .panel-wrap {
    padding-left: 226px;
  }
}

.looper {
  position: fixed;
  inset: 0 0 0 72px;
  background: url(~@/assets/looper-bg.png) center / 1600px auto no-repeat;
  background-size: 100%;
  background-position: 0px -300px;
  opacity: .5;
  transform: rotate(15deg);
  pointer-events: none;
}

.panel {
  max-width: 1077px;
  margin: 0 auto 80px;
  background: $panel;
  border: 1px solid $border;
  border-radius: 16px;
  box-shadow: 0 4px 50px rgba(33, 33, 33, .08), 0 4px 6px rgba(33, 33, 33, .04);
  padding: 24px 24px 32px;
  position: relative;
  top: 160px;
}

.head {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.title {
  margin: 0 0 8px 0;
  font: 800 36px/1.2 'Cabin', 'Segoe UI', Arial, sans-serif;
  color: #fff;
}

.close {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 8px;
  background: transparent;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;

  &:hover {
    background: rgba(255, 255, 255, .06);
  }

  svg {
    width: 20px;
    height: 20px;
  }
}

.sub {
  margin: 0 0 14px;
  font: 500 18px/1.6 'Cabin', sans-serif;
  color: #fff;
  opacity: .95;
}

.chart-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  align-items: center;
  min-height: 457px;
}

.donut {
  position: relative;
  width: 466px;
  height: 466px;
  margin: 4px 0 4px 0;
}

.center-text {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  text-align: center;
  pointer-events: none;

  .line1 {
    font: 700 32px/1 'Roboto', system-ui;
    color: #fff;
  }

  .line2 {
    font: 700 28px/1 'Roboto', system-ui;
    color: #fff;
    margin-top: 6px;
  }
}

.spacer {
  min-height: 300px;
}

@media (max-width: 1200px) {
  .chart-row {
    grid-template-columns: 1fr;
    justify-items: center;
  }
  .spacer {
    display: none;
  }
  .panel {
    margin-top: 80px;
  }
}

html, body {
  margin: 0;
}
</style>
