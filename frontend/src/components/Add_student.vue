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
                        <label for="grade" class="block text-sm font-medium text-gray-700">Grade</label>
                        <select id="grade" v-model="studentProfile.grade" required
                                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                            <option value="">Select Grade</option>
                            <option value="1">Grade 1</option>
                            <option value="2">Grade 2</option>
                            <option value="3">Grade 3</option>
                            <option value="4">Grade 4</option>
                            <option value="5">Grade 5</option>
                            <option value="6">Grade 6</option>
                            <option value="7">Grade 7</option>
                            <option value="8">Grade 8</option>
                            <option value="9">Grade 9</option>
                            <option value="10">Grade 10</option>
                            <option value="11">Grade 11</option>
                            <option value="12">Grade 12</option>
                        </select>
                    </div>

                    <!-- Add subject selection before the password field -->
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Assign Subject</label>
                        <div v-if="isLoadingSubjects" class="text-sm text-gray-500">Loading subjects...</div>
                        <div v-else-if="availableSubjects.length === 0" class="text-sm text-red-500">
                            No subjects available. Please create subjects first.
                        </div>
                        <div v-else class="mt-1 space-y-2 max-h-60 overflow-y-auto border border-gray-300 rounded-md p-3">
                            <div v-for="subject in availableSubjects" :key="subject.id" class="flex items-center">
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
                        <p v-if="availableSubjects.length > 0 && selectedSubjects.length === 0" class="mt-1 text-sm text-red-500">
                            Please select at least one subject
                        </p>
                    </div>

                    <div>
                        <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
                        <input type="password" id="password" v-model="student.password" required
                               class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                    </div>
                    
                    <button type="submit"
                            :disabled="isLoading || (availableSubjects.length > 0 && selectedSubjects.length === 0)"
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
            studentProfile: {
                grade: '',
                education_level: 'School'
            },
            isLoading: false,
            successMessage: '',
            errorMessage: '',
            availableSubjects: [], // Add this to store available subjects
            isLoadingSubjects: false, // Flag for subject loading state
            selectedSubjects: [] // To store selected subjects
        };
    },
    mounted() {
        // Fetch available subjects when component mounts
        this.fetchSubjects();
    },
    methods: {
        // Add method to fetch subjects
        async fetchSubjects() {
            this.isLoadingSubjects = true;
            try {
                const token = localStorage.getItem('token') || sessionStorage.getItem('token');
                const response = await axios.get('http://127.0.0.1:8000/api/subjects/', {
                    headers: { Authorization: `Bearer ${token}` }
                });
                this.availableSubjects = response.data;
                
                // If there are subjects available, select the first one by default
                if (this.availableSubjects.length > 0) {
                    this.selectedSubjects = [this.availableSubjects[0].id];
                }
            } catch (error) {
                console.error('Error fetching subjects:', error);
            } finally {
                this.isLoadingSubjects = false;
            }
        },

        async addStudent() {
            this.isLoading = true;
            this.errorMessage = '';
            this.successMessage = '';
            
            // Check if we have subjects available
            if (this.availableSubjects.length === 0) {
                this.errorMessage = 'No subjects available. Please add subjects before creating a student.';
                this.isLoading = false;
                return;
            }
            
            try {
                // Get token from localStorage or sessionStorage
                const token = localStorage.getItem('token') || sessionStorage.getItem('token');
                
                // 1. Create the user first
                const userResponse = await axios.post('http://127.0.0.1:8000/api/users/', this.student, {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                });
                
                // 2. Now create the profile with the user ID and grade
                if (userResponse.data && userResponse.data.id) {
                    // Make sure grade is selected
                    if (!this.studentProfile.grade) {
                        this.errorMessage = 'Please select a grade for the student';
                        return;
                    }
                    
                    // Use selected subjects or default to first available subject
                    const subjectIds = this.selectedSubjects.length > 0 
                        ? this.selectedSubjects 
                        : [this.availableSubjects[0].id];
                    
                    // Add student profile with properly formatted data and at least one subject
                    const profileData = {
                        user: userResponse.data.id,
                        grade: this.studentProfile.grade,
                        education_level: this.studentProfile.education_level || 'School',
                        subjects: subjectIds // Include at least one subject ID
                    };
                    
                    console.log('Creating student profile with data:', profileData);
                    
                    try {
                        await axios.post('http://127.0.0.1:8000/api/student-profiles/', profileData, {
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
                        };
                        this.studentProfile = {
                            grade: '',
                            education_level: 'School'
                        };
                    } catch (profileError) {
                        console.error('Profile creation error:', profileError);
                        console.error('Profile error response:', profileError.response?.data);
                        
                        // If profile creation fails, try to delete the user we just created
                        try {
                            await axios.delete(`http://127.0.0.1:8000/api/users/${userResponse.data.id}/`, {
                                headers: { 'Authorization': `Bearer ${token}` }
                            });
                            console.log('Rolled back user creation');
                        } catch (deleteError) {
                            console.error('Could not roll back user creation:', deleteError);
                        }
                        
                        throw profileError;
                    }
                }
            } catch (error) {
                console.error('Error adding student:', error);
                
                if (error.response) {
                    console.error('Error response data:', error.response.data);
                    console.error('Error status:', error.response.status);
                    
                    const status = error.response.status;
                    const errorData = error.response.data;
                    
                    // More specific error messages
                    if (status === 400) {
                        if (errorData.username) {
                            this.errorMessage = `Username error: ${errorData.username[0]}`;
                        } else if (errorData.email) {
                            this.errorMessage = `Email error: ${errorData.email[0]}`;
                        } else if (errorData.subjects) {
                            this.errorMessage = `Subject error: ${errorData.subjects[0]}`;
                        } else if (errorData.grade) {
                            this.errorMessage = `Grade error: ${errorData.grade[0]}`;
                        } else if (typeof errorData === 'string') {
                            this.errorMessage = errorData;
                        } else {
                            this.errorMessage = 'Invalid data. Please check your input and try again.';
                            console.error('Full error data:', JSON.stringify(errorData));
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
