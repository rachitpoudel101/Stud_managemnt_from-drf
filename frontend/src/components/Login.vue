<template>
    <section class="p-8">
        <div class="max-w-md mx-auto bg-white p-10 rounded-lg shadow-lg">
            <h2 class="text-2xl font-bold text-center mb-6">Login</h2>
            
            <!-- Success Message -->
            <div v-if="successMessage" class="mb-4 p-3 bg-green-100 border border-green-400 text-green-700 rounded">
                {{ successMessage }}
            </div>
            
            <!-- Error Message -->
            <div v-if="errorMessage" class="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
                {{ errorMessage }}
            </div>
            
            <form @submit.prevent="handleLogin" class="space-y-4">
                <div>
                    <label for="username" class="block text-sm font-medium text-gray-700 mb-1">Username</label>
                    <input 
                        type="text" 
                        id="username" 
                        v-model="loginData.username"
                        required
                        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-700 focus:border-indigo-700"
                    >
                </div>
                
                <div>
                    <label for="password" class="block text-sm font-medium text-gray-700 mb-1">Password</label>
                    <input 
                        type="password" 
                        id="password" 
                        v-model="loginData.password"
                        required
                        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                    >
                </div>
                
                <button 
                    type="submit"
                    :disabled="isLoading"
                    class="w-full bg-indigo-600 text-white py-3 px-6 rounded-md font-semibold hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-colors duration-200 disabled:opacity-50">
                    {{ isLoading ? 'Logging in...' : 'Login' }}
                </button>
            </form>
            
            <p class="mt-4 text-center text-sm text-gray-600">
                Don't have an account? 
                <router-link to="/sign-up" class="text-indigo-600 hover:text-indigo-500">Sign up here</router-link>
            </p>
        </div>
    </section>
</template>

<script>
import axios from 'axios';

export default {
    name: 'Login',
    data() {
        return {
            loginData: {
                username: '',
                password: ''
            },
            isLoading: false,
            successMessage: '',
            errorMessage: ''
        }
    },
    methods: {
        async handleLogin() {
            this.isLoading = true;
            this.successMessage = '';
            this.errorMessage = '';
            
            try {
                const response = await axios.post('http://127.0.0.1:8000/api/token/', this.loginData)

                console.log('Login response:', response.data);
                
                // Check for access token directly
                if (response.data.access) {
                    // Store user data if available
                    if (response.data.user) {
                        localStorage.setItem('user', JSON.stringify(response.data.user));
                        localStorage.setItem('userRole', response.data.user.role || 'user');
                    }
                    
                    // Store tokens
                    localStorage.setItem('token', response.data.access);
                    if (response.data.refresh) {
                        localStorage.setItem('refresh_token', response.data.refresh);
                    }
                    
                    this.successMessage = 'Login successful!';

                    setTimeout(() => {
                        this.$router.push('/dashboard');
                    }, 10);
                } else {
                    console.error('No access token found in response');
                    this.errorMessage = 'Login response missing token. Please check server configuration.';
                    console.log('Response data:', response.data);
                }
                
            } catch (error) {
                console.error('Login error:', error);
                console.error('Error response:', error.response?.data);
                console.error('Error status:', error.response?.status);
                
                if (error.response) {
                    const status = error.response.status;
                    const errorData = error.response.data;
                    
                    if (status === 401) {
                        this.errorMessage = 'Invalid username or password. Please try again.';
                    } else if (status === 400) {
                        this.errorMessage = errorData.detail || errorData.error || 'Invalid request. Please check your input.';
                    } else if (status >= 500) {
                        this.errorMessage = 'Server error. Please try again later.';
                    } else {
                        this.errorMessage = errorData.detail || errorData.error || 'Login failed. Please try again.';
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
}
</script>
