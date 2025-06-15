<template>
    <div>
        <section class="bg-gray-100 min-h-screen flex items-center justify-center">
            <div class="bg-white shadow-md rounded-lg p-8 max-w-md w-full">
                <h2 class="text-2xl font-bold text-center mb-6">Add Teacher</h2>
                
                <!-- Success Message -->
                <div v-if="successMessage" class="mb-4 p-3 bg-green-100 border border-green-400 text-green-700 rounded">
                    {{ successMessage }}
                </div>
                
                <!-- Error Message -->
                <div v-if="errorMessage" class="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
                    {{ errorMessage }}
                </div>
                
                <form @submit.prevent="addTeacher" class="space-y-4">
                    <div>
                        <label for="username" class="block text-sm font-medium text-gray-700">Username</label>
                        <input type="text" id="username" v-model="teacher.username" required
                               class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                    </div>
                    <div>
                        <label for="first_name" class="block text-sm font-medium text-gray-700">First Name</label>
                        <input type="text" id="first_name" v-model="teacher.first_name" required
                               class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                    </div>
                    <div>
                        <label for="last_name" class="block text-sm font-medium text-gray-700">Last Name</label>
                        <input type="text" id="last_name" v-model="teacher.last_name" required
                               class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                    </div>
                    <div>
                        <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
                        <input type="email" id="email" v-model="teacher.email" required
                               class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                    </div>
                    <div>
                        <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
                        <input type="password" id="password" v-model="teacher.password" required
                               class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                    </div>
                    
                    <!-- Subject Selection -->
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Assign Subjects</label>
                        <div v-if="isLoadingSubjects" class="text-sm text-gray-600">Loading subjects...</div>
                        <div v-else-if="subjects.length === 0" class="text-sm text-red-500">
                            No subjects available. Please create subjects first.
                        </div>
                        <div v-else class="space-y-2 max-h-60 overflow-y-auto border border-gray-300 rounded-md p-3">
                            <div v-for="subject in subjects" :key="subject.id" class="flex items-center">
                                <input 
                                    type="checkbox" 
                                    :id="'subject-' + subject.id" 
                                    :value="subject.id" 
                                    v-model="selectedSubjects"
                                    class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                                >
                                <label :for="'subject-' + subject.id" class="ml-2 block text-sm text-gray-900">
                                    {{ subject.name }}
                                </label>
                            </div>
                        </div>
                        <div v-if="!isLoadingSubjects && selectedSubjects.length === 0" class="text-xs text-red-500 mt-1">
                            At least one subject must be assigned to the teacher.
                        </div>
                    </div>
                    
                    <button type="submit"
                            :disabled="isLoading || selectedSubjects.length === 0"
                            class="w-full bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-colors duration-200 disabled:opacity-50">
                        {{ isLoading ? 'Adding Teacher...' : 'Add Teacher' }}
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
    name: 'AddTeacher',
    data() {
        return {
            teacher: {
                username: '',
                first_name: '',
                last_name: '',
                email: '',
                password: '',
                role: 'teacher'
            },
            subjects: [],
            selectedSubjects: [],
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
            this.errorMessage = '';
            
            try {
                const token = localStorage.getItem('token') || sessionStorage.getItem('token');
                const response = await axios.get('http://127.0.0.1:8000/api/subjects/', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                
                this.subjects = response.data;
            } catch (error) {
                console.error('Error fetching subjects:', error);
                this.errorMessage = 'Failed to load subjects. Please try again.';
            } finally {
                this.isLoadingSubjects = false;
            }
        },
        async addTeacher() {
            if (this.selectedSubjects.length === 0) {
                this.errorMessage = 'Please assign at least one subject to the teacher';
                return;
            }
            
            this.isLoading = true;
            this.successMessage = '';
            this.errorMessage = '';
            
            try {
                const token = localStorage.getItem('token') || sessionStorage.getItem('token');
                
                // Add selected subjects to the teacher data
                const teacherData = {
                    ...this.teacher,
                    subjects: this.selectedSubjects
                };
                
                const response = await axios.post('http://127.0.0.1:8000/api/users/', teacherData, {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                });
                
                this.successMessage = 'Teacher added successfully!';
                this.teacher = { 
                    username: '', 
                    first_name: '', 
                    last_name: '', 
                    email: '', 
                    password: '', 
                    role: 'teacher' 
                };
                this.selectedSubjects = [];
            } catch (error) {
                console.error('Error adding teacher:', error);
                
                if (error.response) {
                    const status = error.response.status;
                    const errorData = error.response.data;
                    
                    if (status === 400) {
                        if (errorData.username) {
                            this.errorMessage = `Username error: ${errorData.username[0]}`;
                        } else if (errorData.email) {
                            this.errorMessage = `Email error: ${errorData.email[0]}`;
                        } else if (errorData.error) {
                            this.errorMessage = errorData.error;
                        } else {
                            this.errorMessage = 'Invalid data. Please check your input.';
                        }
                    } else if (status === 401) {
                        this.errorMessage = 'Unauthorized. Please login again.';
                        this.$router.push('/login');
                    } else if (status === 403) {
                        this.errorMessage = 'Access denied. Only admins can add teachers.';
                    } else if (status >= 500) {
                        this.errorMessage = 'Server error. Please try again later.';
                    } else {
                        this.errorMessage = 'Failed to add teacher. Please try again.';
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