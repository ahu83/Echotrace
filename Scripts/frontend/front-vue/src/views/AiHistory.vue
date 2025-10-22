<template>
  <div class="page history">
    <side-panel @signout="onSignout"/>

    <div class="looper"></div>

    <section class="panel-wrap">
      <div class="panel">
        <div class="head">
          <h2 class="title">AI Generation History</h2>
          <button class="pill" @click="exportCsv">Export CSV</button>
        </div>

        <div class="filters">
          <el-input
              v-model="q.keyword"
              placeholder="Search by title / id / model"
              clearable
              style="width:240px"
              @keyup.enter.native="applyFilters"
          />
          <el-select v-model="q.type" placeholder="Type" clearable style="width:150px">
            <el-option label="All" value=""/>
            <el-option label="Text-To-Speech" value="tts"/>
            <el-option label="Detection" value="detect"/>
            <el-option label="Watermark" value="wm"/>
          </el-select>
          <el-select v-model="q.status" placeholder="Status" clearable style="width:150px">
            <el-option label="All" value=""/>
            <el-option label="Processing" value="PROCESSING"/>
            <el-option label="Success" value="SUCCESS"/>
            <el-option label="Failed" value="FAILED"/>
          </el-select>
          <el-date-picker
              v-model="q.range"
              type="daterange"
              start-placeholder="Start"
              end-placeholder="End"
              range-separator="-"
              unlink-panels
              style="width:320px"
          />
          <el-button type="primary" @click="applyFilters">Search</el-button>
          <el-button @click="reset">Reset</el-button>
        </div>

        <el-table :data="pageItems" @selection-change="sels = $event" height="480" style="width:100%">
          <el-table-column type="selection" width="45"/>
          <el-table-column label="Type" width="140">
            <template slot-scope="s">
              <el-tag size="small" :type="typeTagType(s.row.type)">{{ typeLabel(s.row.type) }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="title" label="Title" min-width="220"/>
          <el-table-column prop="model" label="Model" min-width="160"/>
          <el-table-column label="Params" min-width="200">
            <template slot-scope="s">{{ s.row.params || '-' }}</template>
          </el-table-column>
          <el-table-column label="Status" width="140">
            <template slot-scope="s">
              <el-tag :type="statusType(s.row.status)">{{ s.row.status }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="Created" width="180">
            <template slot-scope="s">{{ formatDate(s.row.createdAt) }}</template>
          </el-table-column>
          <el-table-column label="Actions" width="220" fixed="right">
            <template slot-scope="s">
              <el-button type="text" @click="view(s.row)">View</el-button>
              <el-button type="text" @click="download(s.row)" :disabled="!s.row.url">Download</el-button>
              <el-button type="text" @click="remove(s.row)">Delete</el-button>
            </template>
          </el-table-column>
        </el-table>


      </div>
    </section>

    <el-dialog title="Preview" :visible.sync="dlg.visible" width="720px">
      <div v-if="dlg.item && dlg.item.type==='tts'">
        <audio :src="dlg.item.url" controls style="width:100%"></audio>
      </div>
      <div v-else-if="dlg.item && dlg.item.type==='detect'">
        <p style="margin:0 0 12px;">Open detection result page?</p>
        <el-button type="primary" @click="$router.push('/result')">Go to result</el-button>
      </div>
      <div v-else>
        <pre class="json">{{ pretty(dlg.item) }}</pre>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import SidePanel from '@/components/SidePanel.vue';

export default {
  name: 'AiHistory',
  components: {SidePanel},
  data() {
    return {
      q: {keyword: '', type: '', status: '', range: null, page: 1, size: 10},
      list: [],
      sels: [],
      dlg: {visible: false, item: null}
    };
  },
  created() {
    this.fetchData();
  },
  computed: {
    filtered() {
      const {keyword, type, status, range} = this.q;
      const kw = (keyword || '').toLowerCase();
      let arr = this.list.slice();

      if (kw) arr = arr.filter(r =>
          `${r.title} ${r.id} ${r.model}`.toLowerCase().includes(kw));
      if (type) arr = arr.filter(r => r.type === type);
      if (status) arr = arr.filter(r => r.status === status);
      if (range && range.length === 2) {
        const [s, e] = range;
        const end = new Date(e);
        end.setHours(23, 59, 59, 999);
        arr = arr.filter(r => new Date(r.createdAt) >= new Date(s) && new Date(r.createdAt) <= end);
      }
      return arr.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
    },
    pageItems() {
      const st = (this.q.page - 1) * this.q.size;
      return this.filtered.slice(st, st + this.q.size);
    }
  },
  methods: {
    onSignout() {
      this.$message('Sign out clicked');
    },
    async fetchData() {
      this.list = [
        {
          id: 'H24001',
          type: 'tts',
          title: 'Promo-line 001',
          model: 'resnet18-vocoder',
          params: 'voice=female,en-US',
          status: 'SUCCESS',
          createdAt: '2025-03-12T10:15:00Z',
          url: '/mock/audio1.mp3'
        },
        {
          id: 'H24002',
          type: 'detect',
          title: 'Call-sample 17',
          model: 'df-detector-x',
          params: 'thr=0.62',
          status: 'SUCCESS',
          createdAt: '2025-03-12T09:40:00Z'
        },
        {
          id: 'H24003',
          type: 'wm',
          title: 'Embed watermark',
          model: 'wm-echo-1',
          params: 'strength=0.2',
          status: 'PROCESSING',
          createdAt: '2025-03-11T16:22:00Z'
        },
        {
          id: 'H24004',
          type: 'tts',
          title: 'Narration-A',
          model: 'effnet-b0',
          params: 'voice=male,en-GB',
          status: 'FAILED',
          createdAt: '2025-03-10T08:02:00Z'
        }
      ];
    },
    applyFilters() {
      this.q.page = 1;
    },
    reset() {
      this.q = {keyword: '', type: '', status: '', range: null, page: 1, size: this.q.size};
    },
    view(row) {
      this.dlg.item = row;
      this.dlg.visible = true;
    },
    download(row) {
      if (!row.url) return;
      const a = document.createElement('a');
      a.href = row.url;
      a.download = row.title || 'file';
      a.click();
    },
    remove(row) {
      this.$confirm('Delete this record?', 'Confirm', {type: 'warning'})
          .then(() => {
            this.list = this.list.filter(r => r.id !== row.id);
            this.$message.success('Deleted');
          })
          .catch(() => {
          });
    },
    exportCsv() {
      const cols = ['id', 'type', 'title', 'model', 'params', 'status', 'createdAt', 'url'];
      const lines = [cols.join(',')].concat(
          this.filtered.map(r => cols.map(k => `"${(r[k] || '').toString().replace(/"/g, '""')}"`).join(','))
      );
      const blob = new Blob([lines.join('\n')], {type: 'text/csv;charset=utf-8;'});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'ai_history.csv';
      a.click();
      URL.revokeObjectURL(url);
    },

    formatDate(s) {
      const d = new Date(s);
      return d.toLocaleString();
    },
    typeLabel(t) {
      return {tts: 'Text-To-Speech', detect: 'Detection', wm: 'Watermark'}[t] || t;
    },
    typeTagType(t) {
      return {tts: 'success', detect: 'warning', wm: 'info'}[t] || 'info';
    },
    statusType(s) {
      return {SUCCESS: 'success', PROCESSING: 'warning', FAILED: 'danger'}[s] || 'info';
    },
    pretty(o) {
      try {
        return JSON.stringify(o, null, 2);
      } catch (e) {
        return String(o);
      }
    }
  }
};
</script>

<style lang="scss" scoped>
$bg: #0A0A0A;
$panel: #000;
$border: rgba(255, 255, 255, .08);
$text: #E6E8EB;

.history {
  min-height: 100vh;
  background: $bg;
  color: $text;
  position: relative;
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
  top: 200px;
  inset: 0 0 0 72px;
  background: url(~@/assets/looper-bg.png) center / 1600px auto no-repeat;
  opacity: .5;
  transform: rotate(15deg);
  pointer-events: none;
  background-size: 100%;
  background-position: 0px -300px;
}

.panel {
  max-width: 1120px;
  margin: 0 auto 80px;
  background: $panel;
  border: 1px solid $border;
  border-radius: 16px;
  box-shadow: 0 4px 50px rgba(33, 33, 33, .08), 0 4px 6px rgba(33, 33, 33, .04);
  padding: 18px 18px 10px;
  position: relative;
  top: 100px;
}

.head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 6px 12px;
}

.title {
  margin: 0;
  color: #fff;
  font: 800 28px/1.2 'Cabin', 'Segoe UI', Arial, sans-serif;
}

.pill {
  position: relative;
  height: 40px;
  padding: 0 18px 0 18px;
  border-radius: 100px;
  cursor: pointer;
  border: 1.5px solid transparent;
  background-image: linear-gradient(#000, #000),
  linear-gradient(91.06deg, #FF1CF7 2.26%, #00F0FF 100%);
  background-origin: border-box;
  background-clip: padding-box, border-box;
  color: #fff;
  font-weight: 600;

  &:hover {
    opacity: .95;
  }
}

.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  padding: 6px;
}

.foot {
  display: flex;
  justify-content: flex-end;
  padding: 8px 6px 12px;
}

.json {
  background: #111;
  color: #E6E8EB;
  padding: 12px;
  border-radius: 8px;
}
</style>
