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
    
    <!-- Teacher's Section -->
    <div v-if="userRole === 'teacher'" class="space-y-4 mb-6">
      <!-- Teacher's Assigned Subjects -->
      <div class="mb-6">
        <h3 class="text-lg font-semibold text-gray-700 text-center mb-3">Your Assigned Subjects</h3>
        
        <div v-if="isLoadingSubjects" class="text-center text-gray-600">
          <p>Loading subjects...</p>
        </div>
        
        <div v-else-if="teacherSubjects.length === 0" class="bg-yellow-50 border border-yellow-200 rounded-lg p-4 text-center">
          <p class="text-yellow-700">You don't have any subjects assigned to you yet.</p>
        </div>
        
        <div v-else class="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <ul class="divide-y divide-blue-200">
            <li v-for="subject in teacherSubjects" :key="subject.id" class="py-2 flex justify-between">
              <span class="font-medium text-blue-800">{{ subject.name }}</span>
            </li>
          </ul>
        </div>
      </div>
      
      <h3 class="text-lg font-semibold text-gray-700 text-center">Teacher Actions</h3>
      <button @click="manageStudents"
        class="w-full bg-blue-600 text-white py-3 px-6 rounded-md font-semibold hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors duration-200">
        Manage Students & Subjects
      </button>
      <button @click="manageMarks"
        class="w-full bg-green-600 text-white py-3 px-6 rounded-md font-semibold hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-colors duration-200">
        Manage Student Marks
      </button>
    </div>
    
    <!-- Student's Section -->
    <div v-if="userRole === 'student'" class="space-y-4 mb-6">
      <!-- Student's Profile Info -->
      <div class="mb-6">
        <h3 class="text-lg font-semibold text-gray-700 text-center mb-3">Your Information</h3>
        
        <div v-if="isLoadingStudentProfile" class="text-center text-gray-600">
          <p>Loading profile...</p>
        </div>
        
        <div v-else-if="!studentProfile" class="bg-yellow-50 border border-yellow-200 rounded-lg p-4 text-center">
          <p class="text-yellow-700">Could not load your profile information.</p>
        </div>
        
        <div v-else class="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <!-- Grade Information -->
          <div class="mb-3 pb-3 border-b border-blue-200">
            <p class="font-medium text-blue-800">Your Grade: 
              <span class="text-blue-900 font-bold">
                {{ studentProfile.grade_display || `Grade ${studentProfile.grade}` }}
              </span>
            </p>
          </div>
          
          <!-- Assigned Subjects -->
          <div>
            <p class="font-medium text-blue-800 mb-2">Your Subjects:</p>
            <ul v-if="studentSubjects.length > 0" class="divide-y divide-blue-200">
              <li v-for="subject in studentSubjects" :key="subject.id" class="py-2 flex justify-between">
                <span class="font-medium">{{ subject.name }}</span>
                <span class="text-sm text-blue-700">
                  {{ subject.teacher_name ? `Teacher: ${subject.teacher_name}` : 'No teacher assigned' }}
                </span>
              </li>
            </ul>
            <p v-else class="text-center text-blue-700">No subjects assigned yet.</p>
          </div>
        </div>
      </div>

      <h3 class="text-lg font-semibold text-gray-700 text-center">Student Actions</h3>
      <button @click="viewResults"
        class="w-full bg-blue-600 text-white py-3 px-6 rounded-md font-semibold hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors duration-200">
        View My Results
      </button>
    </div>
    
    <!-- Admin Only Actions -->
    <div v-if="userRole === 'admin'" class="space-y-4 mb-6">
      <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
        <p class="text-center text-blue-700 font-medium">
          Total Users: <span class="font-bold">{{ userCount !== null ? userCount : 'Loading...' }}</span>
        </p>
      </div>
      <h3 class="text-lg font-semibold text-gray-700 text-center">Admin Actions</h3>
      <button @click="addSubject"
        class="w-full bg-purple-600 text-white py-3 px-6 rounded-md font-semibold hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 transition-colors duration-200">
        Add Subject
      </button>
      <button @click="addTeachers"
        class="w-full bg-blue-600 text-white py-3 px-6 rounded-md font-semibold hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors duration-200">
        Add Teacher
      </button>
      <button @click="addStudents"
        class="w-full bg-green-600 text-white py-3 px-6 rounded-md font-semibold hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-colors duration-200">
        Add Student
      </button>
      <button @click="manageStudents"
        class="w-full bg-yellow-600 text-white py-3 px-6 rounded-md font-semibold hover:bg-yellow-700 focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:ring-offset-2 transition-colors duration-200">
        Manage Students & Subjects
      </button>
      <button @click="logout" 
        class="w-full bg-red-600 text-white py-3 px-6 rounded-md font-semibold hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition-colors duration-200">
        Logout
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
      userCount: null,
      teacherSubjects: [],
      isLoadingSubjects: false,
      studentProfile: null,
      studentSubjects: [],
      isLoadingStudentProfile: false
    };
  },
  created() {
    // Get user role from storage first
    this.userRole = localStorage.getItem('userRole') || sessionStorage.getItem('userRole') || 'user';
    // Then fetch user count when component is created
    this.fetchUserCount();
    
    // Fetch teacher's subjects if the user is a teacher
    if (this.userRole === 'teacher') {
      this.fetchTeacherSubjects();
    }
    
    // Fetch student profile if the user is a student
    if (this.userRole === 'student') {
      this.fetchStudentProfile();
    }
  },
  methods: {
    async fetchTeacherSubjects() {
      this.isLoadingSubjects = true;
      
      try {
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:8000/api/subjects/', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        
        // The API should already filter subjects for the current teacher
        this.teacherSubjects = response.data;
        console.log('Teacher subjects:', this.teacherSubjects);
      } catch (error) {
        console.error('Error fetching teacher subjects:', error);
        this.errorMessage = 'Failed to load your subjects.';
      } finally {
        this.isLoadingSubjects = false;
      }
    },
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
        console.log("Navigating to add teacher");
        this.$router.push('/admin/add-teacher');
      } catch (error) {
        console.error('Error navigating to add teachers:', error);
        this.errorMessage = 'An error occurred while navigating to add teachers.';
      }
    },
    async addStudents() {
      try {
        console.log("Navigating to add student");
        this.$router.push('/admin/add-student');
      } catch (error) {
        console.error('Error navigating to add students:', error);
        this.errorMessage = 'An error occurred while navigating to add students.';
      }
    },
    async addSubject() {
      try {
        console.log("Navigating to add subject");
        this.$router.push('/admin/add-subject');
      } catch (error) {
        console.error('Error navigating to add subject:', error);
        this.errorMessage = 'An error occurred while navigating to add subject.';
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
    },
    manageStudents() {
      this.$router.push('/manage-students');
    },
    manageMarks() {
      this.$router.push('/teacher/manage-marks');
    },
    viewResults() {
      this.$router.push('/student/view-results');
    },
    async fetchStudentProfile() {
      this.isLoadingStudentProfile = true;
      
      try {
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        const userId = this.getUserId();
        
        if (!userId) {
          console.error('No user ID found');
          return;
        }
        
        // Get the student profile
        const profileResponse = await axios.get(`http://127.0.0.1:8000/api/users/${userId}/profile/`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        
        this.studentProfile = profileResponse.data;
        console.log('Student profile:', this.studentProfile);
        
        // Extract subjects from the profile
        if (this.studentProfile && this.studentProfile.subject_details) {
          this.studentSubjects = this.studentProfile.subject_details;
        } else if (this.studentProfile && this.studentProfile.subjects) {
          // Fetch full subject details if only IDs are provided
          await this.fetchStudentSubjects(this.studentProfile.subjects);
        }
      } catch (error) {
        console.error('Error fetching student profile:', error);
        this.errorMessage = 'Failed to load your profile information.';
      } finally {
        this.isLoadingStudentProfile = false;
      }
    },
    async fetchStudentSubjects(subjectIds) {
      if (!subjectIds || !subjectIds.length) return;
      
      try {
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:8000/api/subjects/', {
          headers: { Authorization: `Bearer ${token}` }
        });
        
        // Filter only the subjects assigned to the student
        this.studentSubjects = response.data.filter(subject => 
          subjectIds.includes(subject.id)
        );
      } catch (error) {
        console.error('Error fetching student subjects:', error);
      }
    },
    getUserId() {
      // Try to get user ID from stored user object
      const userStr = localStorage.getItem('user') || sessionStorage.getItem('user');
      if (userStr) {
        try {
          const user = JSON.parse(userStr);
          return user.id;
        } catch (e) {
          console.error('Error parsing user data:', e);
        }
      }
      return null;
    },
  }
};
</script>