<template>
  <div class="bg-white shadow rounded-lg">
    <div class="px-6 py-4 border-b border-gray-200">
      <h3 class="text-lg leading-6 font-medium text-gray-900">Create New Notice</h3>
    </div>
    <div class="px-6 py-4">
      <!-- Success Message -->
      <div v-if="successMessage" class="mb-4 p-3 bg-green-100 border border-green-400 text-green-700 rounded">
        {{ successMessage }}
      </div>
      
      <!-- Error Message -->
      <div v-if="errorMessage" class="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
        {{ errorMessage }}
      </div>
      
      <form @submit.prevent="submitNotice" class="space-y-4">
        <div>
          <label for="notice-title" class="block text-sm font-medium text-gray-700">Title</label>
          <input 
            type="text" 
            id="notice-title" 
            v-model="notice.title" 
            required
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          >
        </div>
        
        <div>
          <label for="notice-content" class="block text-sm font-medium text-gray-700">Content</label>
          <textarea 
            id="notice-content" 
            v-model="notice.content" 
            rows="4" 
            required
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          ></textarea>
        </div>
        
        <div>
          <label for="notice-audience" class="block text-sm font-medium text-gray-700">Audience</label>
          <select 
            id="notice-audience" 
            v-model="notice.audience" 
            required
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          >
            <option value="student">Students Only</option>
            <option v-if="userRole === 'admin'" value="teacher">Teachers Only</option>
            <option v-if="userRole === 'admin'" value="both">Both Students & Teachers</option>
          </select>
        </div>
        
        <div class="flex justify-end">
          <button 
            type="submit"
            :disabled="isSubmitting"
            class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50"
          >
            {{ isSubmitting ? 'Publishing...' : 'Publish Notice' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'CreateNotice',
  props: {
    userRole: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      notice: {
        title: '',
        content: '',
        audience: 'student', // Default value
        published: true // Default to published
      },
      isSubmitting: false,
      successMessage: '',
      errorMessage: ''
    };
  },
  methods: {
    async submitNotice() {
      this.isSubmitting = true;
      this.errorMessage = '';
      this.successMessage = '';
      
      try {
        // Validate audience based on role
        if (this.userRole === 'teacher' && this.notice.audience !== 'student') {
          this.errorMessage = 'Teachers can only create notices for students.';
          this.isSubmitting = false;
          return;
        }
        
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        await axios.post('http://127.0.0.1:8000/api/notices/', this.notice, {
          headers: { 
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });
        
        this.successMessage = 'Notice published successfully!';
        
        // Reset form
        this.notice = {
          title: '',
          content: '',
          audience: 'student',
          published: true
        };
        
        // Emit event to notify parent component
        this.$emit('notice-created');
      } catch (error) {
        console.error('Error creating notice:', error);
        if (error.response?.data) {
          this.errorMessage = typeof error.response.data === 'string' 
            ? error.response.data 
            : 'Failed to publish notice. Please check your input.';
        } else {
          this.errorMessage = 'Failed to publish notice. Please try again.';
        }
      } finally {
        this.isSubmitting = false;
      }
    }
  }
};
</script>
