<template>
  <div>
    <section class="bg-gray-100 min-h-screen flex items-center justify-center">
      <div class="bg-white shadow-md rounded-lg p-8 max-w-md w-full">
        <h2 class="text-2xl font-bold text-center mb-6">Add Subject</h2>
        
        <!-- Success Message -->
        <div v-if="successMessage" class="mb-4 p-3 bg-green-100 border border-green-400 text-green-700 rounded">
          {{ successMessage }}
        </div>
        
        <!-- Error Message -->
        <div v-if="errorMessage" class="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
          {{ errorMessage }}
        </div>
        
        <form @submit.prevent="addSubject" class="space-y-4">
          <div>
            <label for="name" class="block text-sm font-medium text-gray-700">Subject Name</label>
            <input 
              type="text" 
              id="name" 
              v-model="subject.name" 
              required
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            >
          </div>
          
          <button 
            type="submit"
            :disabled="isLoading"
            class="w-full bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-colors duration-200 disabled:opacity-50"
          >
            {{ isLoading ? 'Adding Subject...' : 'Add Subject' }}
          </button>
        </form>
        
        <!-- List of existing subjects -->
        <div class="mt-8">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Existing Subjects</h3>
          <div v-if="isLoadingSubjects" class="text-sm text-gray-600">Loading subjects...</div>
          <div v-else-if="subjects.length === 0" class="text-sm text-gray-600">No subjects created yet.</div>
          <ul v-else class="mt-2 divide-y divide-gray-200 max-h-60 overflow-y-auto">
            <li v-for="subject in subjects" :key="subject.id" class="py-2 flex justify-between items-center">
              <span class="text-sm font-medium text-gray-900">{{ subject.name }}</span>
              <span class="text-xs text-gray-500">
                {{ subject.teacher_name ? `Teacher: ${subject.teacher_name}` : 'Unassigned' }}
              </span>
            </li>
          </ul>
        </div>
        
        <div class="mt-6 text-center">
          <router-link to="/dashboard" class="text-indigo-600 hover:text-indigo-800">
            Back to Dashboard
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AddSubject',
  data() {
    return {
      subject: {
        name: '',
      },
      subjects: [],
      isLoading: false,
      isLoadingSubjects: false,
      successMessage: '',
      errorMessage: ''
    };
  },
  mounted() {
    this.fetchSubjects();
  },
  methods: {
    async fetchSubjects() {
      this.isLoadingSubjects = true;
      
      try {
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:8000/api/subjects/', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        this.subjects = response.data;
        console.log('Fetched subjects:', this.subjects);
      } catch (error) {
        console.error('Error fetching subjects:', error);
        this.errorMessage = 'Failed to load subjects.';
      } finally {
        this.isLoadingSubjects = false;
      }
    },
    async addSubject() {
      if (!this.subject.name.trim()) {
        this.errorMessage = 'Subject name cannot be empty';
        return;
      }
      
      this.isLoading = true;
      this.successMessage = '';
      this.errorMessage = '';
      
      try {
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        
        console.log('Sending subject data:', this.subject);
        const response = await axios.post('http://127.0.0.1:8000/api/subjects/', this.subject, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });
        
        console.log('Subject added successfully:', response.data);
        this.successMessage = 'Subject added successfully!';
        this.subject = { name: '' };
        
        // Refresh the subject list
        await this.fetchSubjects();
      } catch (error) {
        console.error('Error adding subject:', error);
        
        if (error.response) {
          const status = error.response.status;
          const errorData = error.response.data;
          console.error('Error response data:', errorData);
          
          if (status === 400) {
            if (errorData.name) {
              this.errorMessage = `Subject error: ${errorData.name[0]}`;
            } else {
              this.errorMessage = 'Invalid subject data. Please check your input.';
            }
          } else if (status === 401) {
            this.errorMessage = 'Unauthorized. Please login again.';
            this.$router.push('/login');
          } else if (status === 403) {
            this.errorMessage = 'Access denied. Only admins can add subjects.';
          } else {
            this.errorMessage = errorData.detail || 'Failed to add subject. Please try again.';
          }
        } else if (error.code === 'ERR_NETWORK') {
          this.errorMessage = 'Cannot connect to server. Please check if the backend is running.';
        } else {
          this.errorMessage = 'Network error. Please try again.';
        }
      } finally {
        this.isLoading = false;
      }
    }
  }
};
</script>