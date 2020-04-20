<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <div class="mb-4">
      <p>
        <b>Upload files:</b>
      </p>
      <div>
        <b-form-select
          v-model="uploadSelected"
          class="mb-4"
          style="max-width:20rem;"
          :options="uploadOptions"
        />
      </div>
      <b-form-file
        :state="Boolean(upload.files.length > 0)"
        style="max-width:35rem;"
        size="lg"
        :placeholder="'Choose ' + (uploadSelected == 'dir' ? 'directory' : 'files') + ' or drop it here...'"
        drop-placeholder="Drop here..."
        @change="filesChange($event.target.name, $event.target.files)"
        multiple
        :directory="uploadSelected == 'dir'"
        :file-name-formatter="formatNames"
        accept="text/*"
      >
        <template slot="file-name" slot-scope="{ names }">
          <b-badge variant="dark">{{ names[0] }}</b-badge>
          <b-badge v-if="names.length > 1" variant="dark" class="ml-1">
            + {{ names.length - 1 }} More files
          </b-badge>
        </template>
      </b-form-file>
    </div>
    <div class="mb-4">
      <p>
        <b>Keyword:</b>
      </p>
      <b-form-textarea
        :state="Boolean(keyword)"
        style="max-width: 40rem;margin-left: auto;margin-right:auto"
        type="text"
        name="keyword"
        id="keyword"
        v-model="keyword"
        placeholder="Enter something..."
        rows="3"
        max-rows="6"
      />
    </div>
    <div>
      <p>
        <b>Algorithm:</b>
      </p>
      <b-form-select
        v-model="algorithm"
        :state="Boolean(algorithm)"
        class="mb-4"
        style="max-width:20rem;"
        :options="algorithmOptions"
      />
    </div>

    <h3>
      <b-button @click="onUploadHandler()" variant="success">
        Upload
      </b-button>
    </h3>

    <template v-if="data">
    <h3>Extraction Result: </h3>
      <h4>{{ `${renderKeyword} (${data.length})` }}</h4>
      <b-card
        v-for="(el, idx) in data"
        :key="idx"
        :header="el.filename"
        border-variant="primary"
        header-bg-variant="dark"
        header-text-variant="white"
        style="max-width: 40rem;margin-left: auto;margin-right:auto"
        class="mb-4"
        body-class="text-center"
      >
        <b-card-text v-html="el.date" />
        <b-card-text v-html="el.number" />
        <b-card-text v-html="el.text" />
      </b-card>
    </template>
    <footer class="mt-4 mb-4">
      copyright ®2020 ilhamsyahids
      <ul>
        <li>
          <a
            href="https://www.linkedin.com/in/ilhamsyahids/"
            target="_blank"
            rel="noopener"
          >
            <font-awesome-icon size="lg" :icon="['fab', 'linkedin']" />
          </a>
        </li>
        <li>
          <a
            href="https://ilhamsyahids.codes/"
            target="_blank"
            rel="noopener"
          >
            <b-icon-person-fill />
          </a>
        </li>
      </ul>
    </footer>
  </div>
</template>

<script>
import axios from 'axios';
import { BIconPersonFill } from 'bootstrap-vue'

export default {
  name: "Uploader",
  props: {
    msg: String
  },
  components: {
    BIconPersonFill
  },
  data() {
    return {
      uploadOptions: [
        { value: 'files', text: 'Multiple Files' },
        { value: 'dir', text: 'Directory' }
      ],
      algorithmOptions: [
        { value: 'Regex', text: 'Regex' },
        { value: 'Boyer', text: 'Boyer-Moore' },
        { value: 'KMP', text: 'Knuth Morris Pratt' }
      ],
      uploadSelected: 'files',
      data: null,
      upload: {
        files:[]
      },
      keyword: null,
      renderKeyword: null,
      algorithm: "Regex"
    };
  },
  methods: {
    formatNames(files) {
      if (files.length === 1) {
        return files[0].name
      } else {
        return `${files.length} files selected`
      }
    },
    filesChange(name, files) {
      if (!files.length) return;
      this.upload.files = []
      for (let i = 0; i < files.length; i++) {
        this.readFileContent(files[i]).then(res => {
          let file = {
            name: files[i].name,
            text: res.split("\n").filter(e => e !== '')
          }
          this.upload.files.push(file)
        })
      }
    },
    readFileContent(file) {
      const reader = new FileReader();
      return new Promise((resolve, reject) => {
        reader.onload = event => resolve(event.target.result);
        reader.onerror = error => reject(error);
        reader.readAsText(file);
      });
    },
    onUploadHandler() {
      this.upload.algorithm = this.algorithm
      this.upload.keyword = this.keyword
      axios.post(process.env.VUE_APP_API_URL || "http://localhost:5000", this.upload)
        .then(res => {
          String.prototype.splice = function(idx, rdx, str1, str2) {
              return this.slice(0, idx) + str1 + this.slice(idx, idx + rdx) + str2 + this.slice(idx + rdx);
          };
          this.renderKeyword = this.keyword
          res.data.data.forEach(el => {
            el.text = el.text.splice(el.idx, this.renderKeyword.length, "<b>", "</b>")
          });
          this.data = res.data.data
        }).catch(() => {
          console.log("At least one data is missing")
        })
    }
  }
};
</script>

<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #4289b9;
}
</style>
