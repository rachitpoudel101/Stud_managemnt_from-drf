<template>
    <div>
        <section class="bg-gray-100 min-h-screen flex items-center justify-center">
            <div class="bg-white shadow-md rounded-lg p-8 max-w-md w-full">
                <h2 class="text-2xl font-bold text-center mb-6">Add Student</h2>
                
                <!-- Success Message -->
                <div v-if="successMessage" class="mb-4 p-3 bg-green-100 border border-green-400 text-green-700 rounded">
                    {{ successMessage }}
                </div>
                
                <!-- Error Message -->
                <div v-if="errorMessage" class="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
                    {{ errorMessage }}
                </div>
                
                <form @submit.prevent="addStudent" class="space-y-4">
                    <div>
                        <label for="username" class="block text-sm font-medium text-gray-700">Username</label>
                        <input type="text" id="username" v-model="student.username" required
                               class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                    </div>
                    <div>
                        <label for="first_name" class="block text-sm font-medium text-gray-700">First Name</label>
                        <input type="text" id="first_name" v-model="student.first_name" required
                               class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                    </div>
                    <div>
                        <label for="last_name" class="block text-sm font-medium text-gray-700">Last Name</label>
                        <input type="text" id="last_name" v-model="student.last_name" required
                               class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                    </div>
                    <div>
                        <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
                        <input type="email" id="email" v-model="student.email" required
                               class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                    </div>
                    <div>
                        <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
                        <input type="password" id="password" v-model="student.password" required
                               class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                    </div>
                    <button type="submit"
                            :disabled="isLoading"
                            class="w-full bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-colors duration-200 disabled:opacity-50">
                        {{ isLoading ? 'Adding Student...' : 'Add Student' }}
                    </button>
                </form>
                
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
    name: 'AddStudent',
    data() {
        return {
            student: {
                username: '',
                first_name: '',
                last_name: '',
                email: '',
                password: '',
                role: 'student'
            },
            isLoading: false,
            successMessage: '',
            errorMessage: ''
        };
    },
    methods: {
        async addStudent() {
            this.isLoading = true;
            this.successMessage = '';
            this.errorMessage = '';
            
            try {
                // Get token from localStorage or sessionStorage
                const token = localStorage.getItem('token') || sessionStorage.getItem('token');
                
                const response = await axios.post('http://127.0.0.1:8000/api/users/', this.student, {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                });
                
                this.successMessage = 'Student added successfully!';
                this.student = { 
                    username: '', 
                    first_name: '', 
                    last_name: '', 
                    email: '', 
                    password: '', 
                    role: 'student' 
                }; // Reset form
            } catch (error) {
                console.error('Error adding student:', error);
                
                if (error.response) {
                    const status = error.response.status;
                    const errorData = error.response.data;
                    
                    if (status === 400) {
                        if (errorData.username) {
                            this.errorMessage = `Username error: ${errorData.username[0]}`;
                        } else if (errorData.email) {
                            this.errorMessage = `Email error: ${errorData.email[0]}`;
                        } else {
                            this.errorMessage = errorData.detail || errorData.error || 'Invalid data. Please check your input.';
                        }
                    } else if (status === 401) {
                        this.errorMessage = 'Unauthorized. Please login again.';
                        // Redirect to login if unauthorized
                        this.$router.push('/login');
                    } else if (status === 403) {
                        this.errorMessage = 'Access denied. Only admins can add students.';
                    } else if (status >= 500) {
                        this.errorMessage = 'Server error. Please try again later.';
                    } else {
                        this.errorMessage = errorData.detail || errorData.error || 'Failed to add student. Please try again.';
                    }
                } else if (error.code === 'ERR_NETWORK') {
                    this.errorMessage = 'Cannot connect to server. Please check if the backend is running on http://127.0.0.1:8000';
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

<style scoped>
/* Component-specific styles can go here if needed */
</style>
