<template>
  <aside
      class="side"
      :class="{ expanded }"
      @mouseenter="expanded = true"
      @mouseleave="expanded = false"
  >
    <div class="brand">
      <img class="logo" :src="logo" alt="logo"/>
      <span class="brand-text">Echo-trace</span>
    </div>

    <nav class="nav">
      <button class="item" @click="$router.push('/watermark')">
        <span class="icon">
          <svg viewBox="0 0 24 24"><path fill="#fff"
                                         d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41L18.37 3.29c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/></svg>
        </span>
        <span class="label">Watermark</span>
      </button>

      <button class="item" @click="$router.push('/result')">
        <span class="icon">
          <svg viewBox="0 0 24 24"><path fill="#fff" d="M11 7h2v8h-2V7zm0 10h2v2h-2v-2z"/></svg>
        </span>
        <span class="label">Deepfake detection</span>
      </button>

      <button class="item" @click="$router.push('/tts')">
        <span class="icon">
          <svg viewBox="0 0 24 24"><path fill="#fff"
                                         d="M12 14a3 3 0 0 0 3-3V6a3 3 0 0 0-6 0v5a3 3 0 0 0 3 3zm5-3a5 5 0 0 1-10 0H5a7 7 0 0 0 6 6.92V20H8v2h8v-2h-3v-2.08A7 7 0 0 0 19 11h-2z"/></svg>
        </span>
        <span class="label">Text to speech</span>
      </button>
    </nav>

    <button class="signout" @click="$emit('signout')">
      <span>Sign Out</span>
    </button>
  </aside>
</template>

<script>
export default {
  name: 'SidePanel',
  props: {logo: {type: String, default: require('@/assets/logo.png')}},
  data() {
    return {expanded: false};
  }
};
</script>

<style lang="scss" scoped>
$rail: #000;
$text: #fff;

.side {
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  width: 72px;
  background: $rail;
  z-index: 10;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  border-right: 1px solid rgba(255, 255, 255, .06);
  transition: width .18s ease;

  &.expanded {
    width: 226px;
  }

  .brand {
    height: 56px;
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px 12px 8px;
  }

  .logo {
    width: 30px;
    height: 30px;
    object-fit: contain;
  }

  .brand-text {
    color: $text;
    font-family: 'Inria Sans', system-ui;
    font-size: 15px;
    white-space: nowrap;
    opacity: 0;
    width: 0;
    overflow: hidden;
    pointer-events: none;
    transform: translateX(-8px);
    transition: opacity .15s ease, width .15s ease, transform .15s ease;
  }

  &.expanded .brand-text {
    opacity: 1;
    width: auto;
    pointer-events: auto;
    transform: none;
  }

  .nav {
    margin-top: 200px;
    padding: 24px 8px;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .item {
    height: 44px;
    width: 100%;
    display: grid;
    grid-template-columns: 72px;
    align-items: center;
    background: transparent;
    border: none;
    color: $text;
    text-align: left;
    padding: 0;
    border-radius: 8px;
    cursor: pointer;
    transition: background .12s ease, grid-template-columns .18s ease;

    &:hover {
      background: rgba(255, 255, 255, .06);
    }

    &.active {
      background: rgba(255, 255, 255, .08);
    }

    .icon {
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .icon svg {
      width: 24px;
      height: 24px;
    }

    .label {
      font-family: 'Cabin', sans-serif;
      font-size: 16px;
      white-space: nowrap;
      opacity: 0;
      width: 0;
      overflow: hidden;
      pointer-events: none;
      transform: translateX(-8px);
      transition: opacity .15s ease, width .15s ease, transform .15s ease;
    }
  }

  &.expanded .item {
    grid-template-columns: 56px 1fr;

    .label {
      opacity: 1;
      width: auto;
      pointer-events: auto;
      transform: none;
    }
  }

  .signout {
    position: absolute;
    bottom: 10%;
    left: 30%;
    height: 44px;
    border: none;
    background: transparent;
    color: $text;
    font: 700 20px/24px 'Inter', system-ui;
    text-align: left;
    cursor: pointer;
    border-radius: 8px;

    span {
      opacity: 0;
      width: 0;
      overflow: hidden;
      display: inline-block;
      transition: opacity .15s ease, width .15s ease;
    }
  }

  &.expanded .signout span {
    opacity: 1;
    width: auto;
  }
}
</style>
