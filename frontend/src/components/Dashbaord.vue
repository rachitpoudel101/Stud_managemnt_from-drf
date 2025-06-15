<template>
<section class="w-full min-h-[calc(100vh-67px)] bg-gray-100 flex items-center justify-center">
  <div class="max-w-md w-full bg-white p-10 rounded-lg shadow-lg">
    <h2 class="text-2xl font-bold text-center mb-6">Dashboard</h2>
    
    <!-- Success Message -->
    <div v-if="successMessage" class="mb-4 p-3 bg-green-100 border border-green-400 text-green-700 rounded">
      {{ successMessage }}
    </div>
    
    <!-- Error Message -->
    <div v-if="errorMessage" class="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
      {{ errorMessage }}
    </div>
    
    <p class="text-center text-gray-600 mb-4">Welcome to the Dashboard, {{ userRole }}!</p>
    <!-- Admin Only Actions -->
    <div v-if="userRole === 'admin'" class="space-y-4 mb-6">
      <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
        <p class="text-center text-blue-700 font-medium">
          Total Users: <span class="font-bold">{{ userCount !== null ? userCount : 'Loading...' }}</span>
        </p>
      </div>
      <h3 class="text-lg font-semibold text-gray-700 text-center">Admin Actions</h3>
      <button @click="addTeachers"
        class="w-full bg-blue-600 text-white py-3 px-6 rounded-md font-semibold hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors duration-200">
        Add Teacher
      </button>
      <button @click="addStudents"
        class="w-full bg-green-600 text-white py-3 px-6 rounded-md font-semibold hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-colors duration-200">
        Add Student
      </button>
    </div>
  </div>
</section>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Dashboard',
  data() {
    return {
      successMessage: '',
      errorMessage: '',
      userRole: '',
      userCount: null
    };
  },
  created() {
    // Get user role from storage first
    this.userRole = localStorage.getItem('userRole') || sessionStorage.getItem('userRole') || 'user';
    // Then fetch user count when component is created
    this.fetchUserCount();
  },
  mounted() {
    // User role is already set in created()
  },
  methods: {
    async logout() {
      try {
        // Clear all stored authentication data
        localStorage.removeItem('token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        localStorage.removeItem('userRole');
        sessionStorage.removeItem('token');
        sessionStorage.removeItem('refresh_token');
        sessionStorage.removeItem('user');
        sessionStorage.removeItem('userRole');
        
        this.successMessage = 'Successfully logged out!';
        this.errorMessage = '';
        
        // Navigate to login page with a slight delay to show success message
        setTimeout(() => {
          this.$router.push('/login');
        }, 10);
      } catch (error) {
        console.error('Logout error:', error);
        this.errorMessage = 'An error occurred during logout. Please try again.';
        this.successMessage = '';
      }
    },
    async addTeachers() {
      try {
        // Navigate to the add teachers page
        console.log("Navigating to add teacher");
        this.$router.push('/admin/add-teacher');
      } catch (error) {
        console.error('Error navigating to add teachers:', error);
        this.errorMessage = 'An error occurred while navigating to add teachers.';
      }
    },
    async addStudents() {
      try {
        // Navigate to the add students page
        console.log("Navigating to add student");
        this.$router.push('/admin/add-student');
      } catch (error) {
        console.error('Error navigating to add students:', error);
        this.errorMessage = 'An error occurred while navigating to add students.';
      }
    },
    async fetchUserCount() {
      // Only fetch if user is admin
      if (this.userRole === 'admin') {
        try {
          const token = localStorage.getItem('token') || sessionStorage.getItem('token');
          const response = await axios.get('http://127.0.0.1:8000/api/users/', {
            headers: {
              Authorization: `Bearer ${token}`
            }
          });
          this.userCount = response.data.user_count || response.data.length || 0;
        } catch (error) {
          console.error('Error fetching user count:', error);
          this.errorMessage = 'Failed to fetch user count.';
          this.userCount = 'Error';
        }
      }
    }
  }
};
</script>