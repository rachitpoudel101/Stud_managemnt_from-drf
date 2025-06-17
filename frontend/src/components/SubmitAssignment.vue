<template>
  <div class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg p-6 w-full max-w-md mx-4">
      <h3 class="text-lg font-medium text-gray-900 mb-4">Submit Assignment</h3>
      
      <div class="mb-4 p-3 bg-blue-50 rounded-md">
        <h4 class="font-medium text-blue-900">{{ assignment.title }}</h4>
        <p class="text-sm text-blue-700 mt-1">{{ assignment.description }}</p>
        <p class="text-xs text-blue-600 mt-2">Due: {{ formatDate(assignment.due_date) }}</p>
      </div>
      
      <form @submit.prevent="submitAssignment" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">File *</label>
          <input 
            type="file" 
            @change="handleFileChange"
            required
            class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Comments (Optional)</label>
          <textarea 
            v-model="submissionData.comments" 
            rows="3"
            placeholder="Add any comments about your submission..."
            class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          ></textarea>
        </div>
        
        <div v-if="errorMessage" class="text-red-600 text-sm">
          {{ errorMessage }}
        </div>
        
        <div class="flex justify-end space-x-3">
          <button 
            type="button"
            @click="$emit('close')" 
            class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 border border-gray-300 rounded-md hover:bg-gray-200"
          >
            Cancel
          </button>
          <button 
            type="submit"
            :disabled="isSubmitting || !selectedFile"
            class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 disabled:opacity-50"
          >
            {{ isSubmitting ? 'Submitting...' : 'Submit Assignment' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SubmitAssignment',
  props: {
    assignment: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      submissionData: {
        comments: ''
      },
      selectedFile: null,
      isSubmitting: false,
      errorMessage: ''
    };
  },
  methods: {
    handleFileChange(event) {
      this.selectedFile = event.target.files[0];
      this.errorMessage = '';
    },
    
    async submitAssignment() {
      if (!this.selectedFile) {
        this.errorMessage = 'Please select a file to submit';
        return;
      }
      
      this.isSubmitting = true;
      this.errorMessage = '';
      
      try {
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        const formData = new FormData();
        
        formData.append('assignment', this.assignment.id);
        formData.append('file', this.selectedFile);
        if (this.submissionData.comments) {
          formData.append('comments', this.submissionData.comments);
        }
        
        await axios.post('http://127.0.0.1:8000/api/submissions/', formData, {
          headers: { 
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'multipart/form-data'
          }
        });
        
        this.$emit('submitted');
        this.$emit('close');
      } catch (error) {
        console.error('Error submitting assignment:', error);
        if (error.response?.data?.error) {
          this.errorMessage = error.response.data.error;
        } else {
          this.errorMessage = 'Failed to submit assignment. Please try again.';
        }
      } finally {
        this.isSubmitting = false;
      }
    },
    
    formatDate(dateString) {
      return new Date(dateString).toLocaleString();
    }
  }
};
</script>
