<template>
  <div>
    <h1 class="website-title">Spam or Ham Detector</h1>
    <header>
      <nav>
        <ul>
          <li v-for="tabName in tabNames" :key="tabName" @click="changeTab(tabName)">
            <button :class="{ tab: true, active: tabName === activeTab }">
              <span class="tab-copy">{{ tabName }}</span>
              <span class="tab-background"></span>
              <span class="tab-rounding left"></span>
              <span class="tab-rounding right"></span>
            </button>
          </li>
        </ul>
      </nav>
    </header>

    <article>
      <div class="container">
        <div class="content-wrapper">
          <div v-if="activeTab === 'Text Classification'" class="text-tab">
            <textarea class="text-input" placeholder="Enter text here" ref="textInput" v-model="textInput"></textarea>
            <div class="button-container">
              <button class="submit-button" @click="submitText">Submit</button>
              <button class="reset-button" @click="resetTextTab">Reset</button>
            </div>
          </div>
          <div v-else-if="activeTab === 'Image Classification'" class="image-tab">
            <div class="drag-zone"
                 @dragenter="handleDragEnter"
                 @dragover="handleDragOver"
                 @dragleave="handleDragLeave"
                 @drop="handleDrop"
            >
              <label for="file-input" class="file-label">
                <span v-if="selectedImage">{{ selectedImage.name }}</span>
                <span class="file-description" v-else>Drag and drop an image file here or click to upload.</span>
              </label>
              <input type="file" id="file-input" accept="image/*" @change="handleFileUpload" />
              <div class="button-container">
                <button class="submit-button" @click="submitImage">Submit</button>
                <button class="reset-button" @click="resetImageTab">Reset</button>
              </div>
            </div>
          </div>
        </div>
        <div class="result" :class="resultClass" v-if="result">
          <span class="result-icon" v-if="resultIcon">{{ resultIcon }}</span>
          <span class="result-text">{{ result }}</span>
        </div>
      </div>
    </article>
  </div>
</template>

<script>
// import axios from 'axios'; // Import the axios library here

export default {
  data() {
    return {
      activeTab: 'Text Classification',
      tabNames: ['Text Classification', 'Image Classification'],
      selectedImage: null,
      textInput: '', // Added data property for the text input
      apiEndpoint: 'https://localhost:5000',
      result: '', // Store the result received from the API
    };
  },
  methods: {
    changeTab(tabName) {
      this.activeTab = tabName;
      this.result = ''; // Clear the result while change tab
      this.textInput = '';
    },
    uploadImage() {
      document.getElementById('file-input').click();
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      this.selectedImage = file;
    },
    handleDragEnter(event) {
      event.preventDefault();
      event.stopPropagation();
    },
    handleDragOver(event) {
      event.preventDefault();
      event.stopPropagation();
      event.dataTransfer.dropEffect = 'copy';
    },
    handleDragLeave(event) {
      event.preventDefault();
      event.stopPropagation();
    },
    handleDrop(event) {
      event.preventDefault();
      event.stopPropagation();
      const file = event.dataTransfer.files[0];
      this.selectedImage = file;
    },
    resetTextTab() {
      this.textInput = ''; // Reset the text input
      this.result = ''; // Clear the result while reset
      this.$refs.textInput.style.height = '200px'; // Restore the default size of the text box
    },
    resetImageTab() {
      this.selectedImage = null; // Reset the selected image
      this.result = ''; // Clear the result while reset
      const fileInput = document.getElementById('file-input');
      fileInput.value = ''; // Reset the value of the file input element
    },
    submitText() {
      const trimmedText = this.textInput.trim(); // Trim the text input

      if (!trimmedText) {
        // Input is empty or contains only whitespace
        alert('Please enter some text.');
        return;
      }

      // Simulate a response from the backend
      setTimeout(() => {
        this.result = `Text submitted: ${trimmedText}`;
      }, 1000);

      // axios.post(this.apiEndpoint, textData)
      //   .then(response => {
      //     this.result = `The predict result is: ${response.data}`; // Update the result with the API response
      //   })
      //   .catch(error => {
      //     console.error(error);
      //   });
    },
    submitImage() {
      if (!this.selectedImage) {
        // No image selected
        alert('Please select an image.');
        return;
      }


      // Simulate a response from the backend
      setTimeout(() => {
        this.result = `Image submitted: ${this.selectedImage.name}`;
      }, 1000);

      // axios.post(this.apiEndpoint, formData)
      //   .then(response => {
      //     this.result = response.data; // Update the result with the API response
      //   })
      //   .catch(error => {
      //     console.error(error);
      //   });
    },
  },
  computed: {
  resultClass() {
    return this.result ? (this.result === 'Spam' ? 'spam' : 'non-spam') : '';
  },
  resultIcon() {
    return this.result ? (this.result === 'Spam' ? '🚫' : '✅') : '';
  },
},
};
</script>

<style lang="scss">
$azure-blue: #007bff;
// $pink: #D07FAF;
$cyan-blue: #75B8FF;

body {
  margin: 0;
  padding: 0;
  font-family: 'PT Sans', sans-serif;
  background-color: var(--azure-blue);
}

.website-title {
  background-color: $azure-blue;
  // background-image: linear-gradient(30deg, $azure-blue, $cyan-blue);
  text-align: center;
  color: white;
  font-size: 32px;
  padding: 45px 20px 20px 20px;
  margin: 0;
  border: none;
}

header {
  background-color: $azure-blue;
  // background-image: linear-gradient(30deg, $azure-blue, $cyan-blue);
  height: 12.5vh;
  // min-height: 180px;
  width: 100%;
  display: flex;
  align-items: flex-end;
  overflow: hidden;
}

nav {
  width: 100%;
  display: flex;
  justify-content: center;
  border-bottom: 20px solid #fff;
  filter: drop-shadow(0 -4px 4px rgba(darken($azure-blue, 30%), .3));
}

ul {
  display: flex;
  flex-direction: row;
  list-style: none;
  margin: 0;
  padding: 0;
}

.tab {
  $border-radius: 8px;
  $transition-duration: 0.24s;
  $transition-timing: cubic-bezier(0.86, 0, 0.07, 1);
  font-family: 'PT Sans', sans-serif;
  font-weight: bold;
  font-size: 20px;
  color: #fff;
  border: none;
  padding: 16px 40px;
  margin: 0 24px 0;
  outline: none;
  cursor: pointer;
  position: relative;
  background: none;

  &:hover {
    .tab-background {
      height: 16px;
    }

    .tab-rounding {
      transform: scaleY(1);
    }
  }

  &.active {
    color: $azure-blue;

    .tab-background {
      height: 100%;
    }

    .tab-rounding {
      transform: scaleY(1);
    }
  }

  &-copy {
    position: relative;
    z-index: 1;
  }

  &-background {
    display: block;
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background: #fff;
    z-index: 0;
    height: 0;
    border-radius: $border-radius $border-radius 0 0;
    transition: height $transition-timing $transition-duration;
  }

  &-rounding {
    $rounding-size: $border-radius;
    $background-color: #fff;
    padding: $rounding-size / 2 $rounding-size;
    display: block;
    position: absolute;
    overflow: hidden;
    bottom: 0;
    transform: scaleY(0);
    transform-origin: bottom;
    transition: transform $transition-timing $transition-duration;

    &:before {
      content: "";
      position: absolute;
      width: $rounding-size * 2;
      height: $rounding-size * 2;
      top: -$rounding-size;
      left: -$rounding-size;
      border-radius: 100%;
    }

    &.left {
      left: -$rounding-size;

      &:before {
        box-shadow: 0 0 0 10rem $background-color;
      }
    }

    &.right {
      right: -$rounding-size;

      &:before {
        left: $rounding-size;
        box-shadow: 0 0 0 10rem $background-color;
      }
    }
  }
}

article {
  .container {
    width: 100%;
    padding: 40px;
    max-width: 1024px;
    box-sizing: border-box;
    margin: 0 auto;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .text-tab {
    display: flex;
    flex-direction: column;
    align-items: center;

    .text-input {
      width: 70%;
      height: 200px;
      font-size: 20px;
      padding: 10px;
      resize: vertical;
    }

    .button-container {
      display: flex;
      justify-content: center;
      margin-top: 16px;
      margin-bottom: 20px;

      .submit-button,
      .reset-button {
        margin: 0 32px;
        font-size: 16px;
        font-family: 'PT Sans', sans-serif;
      }
    }
  }

  .image-tab {
    display: flex;
  flex-direction: column;
  justify-content: flex-start; /* Updated to align items from the top */
  align-items: center;
  position: relative; /* Added positioning for result */


    .drag-zone {
      width: 70%;
      height: 200px;
      border: 2px dashed #aaa;
      display: flex;
      justify-content: center;
      align-items: center;
      cursor: pointer;
      position: relative;

      .file-label {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);

        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: #aaa;
        font-size: 18px;

        .file-description {
          margin-top: 10px;
          color: #aaa;
          font-size: 18px;
        }
      }

      input[type="file"] {
        display: none;
      }
    }

    .button-container {
      position: absolute;
      bottom: -75px; /* Adjust the desired distance from the bottom */
      width: 100%;
      display: flex;
      justify-content: center;
      margin-top: 16px;
      margin-bottom: 20px;

      .submit-button,
      .reset-button {
        margin: 0 32px;
        font-size: 16px;
        font-family: 'PT Sans', sans-serif;
      }

      
    }
  }
}

.result {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 60px;
  font-size: 18px;
  text-align: center;
  font-weight: bold;
  padding: 10px;
  border-radius: 8px;
  transition: background-color 0.3s ease;
}

.result.spam {
  background-color: #ff5454;
}

.result.non-spam {
  background-color: #50d890;
}

.result-icon {
  margin-right: 10px;
}

.result-text {
  text-transform: uppercase;
}


</style>
