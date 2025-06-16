<template>
  <div class="bg-gray-100 min-h-screen p-6">
    <div class="max-w-4xl mx-auto bg-white rounded-lg shadow-md p-6">
      <h1 class="text-2xl font-bold text-center mb-6">Manage Students</h1>
      
      <!-- Success & Error Messages -->
      <div v-if="successMessage" class="mb-4 p-3 bg-green-100 border border-green-400 text-green-700 rounded">
        {{ successMessage }}
      </div>
      
      <div v-if="errorMessage" class="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
        {{ errorMessage }}
      </div>
      
      <!-- Students and Subject Assignment -->
      <div v-if="isLoadingStudents" class="text-center py-8">
        <p class="text-gray-500">Loading students...</p>
      </div>
      <div v-else-if="students.length === 0" class="text-center py-8">
        <p class="text-gray-500">No students found.</p>
      </div>
      <div v-else class="mb-6">
        <h2 class="text-xl font-semibold mb-4">Students</h2>
        
        <!-- Student selection -->
        <div class="mb-4">
          <label for="studentSelect" class="block text-sm font-medium text-gray-700 mb-2">Select Student</label>
          <select 
            id="studentSelect"
            v-model="selectedStudentId" 
            @change="loadStudentSubjects"
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          >
            <option value="">-- Select a Student --</option>
            <option v-for="student in students" :key="student.id" :value="student.id">
              {{ student.first_name }} {{ student.last_name }} ({{ student.username }})
            </option>
          </select>
        </div>
        
        <!-- Subject assignment when student is selected -->
        <div v-if="selectedStudentId" class="mt-6">
          <h3 class="text-lg font-semibold mb-3">Manage {{ getSelectedStudentName() }}</h3>
          
          <!-- Student Grade section -->
          <div class="mb-6 bg-gray-50 p-4 rounded-lg border border-gray-200">
            <h4 class="font-medium mb-2">Student Grade</h4>
            <div class="flex items-center space-x-4">
              <select 
                v-model="selectedGrade"
                class="px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              >
                <option value="">Select Grade</option>
                <option v-for="grade in gradeOptions" :key="grade.value" :value="grade.value">
                  {{ grade.label }}
                </option>
              </select>
              
              <button 
                @click="updateStudentGrade" 
                :disabled="!selectedGrade || isSavingGrade"
                class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 disabled:opacity-50">
                {{ isSavingGrade ? 'Updating...' : 'Update Grade' }}
              </button>
            </div>
          </div>
          
          <!-- Subject assignment -->
          <div v-if="isLoadingSubjects" class="text-center py-4">
            <p class="text-gray-500">Loading subjects...</p>
          </div>
          <div v-else-if="availableSubjects.length === 0" class="text-center py-4">
            <p class="text-gray-500">No subjects available for assignment.</p>
          </div>
          <div v-else>
            <div class="bg-gray-50 p-4 rounded-lg">
              <div class="mb-3 font-medium">Available Subjects:</div>
              <div class="space-y-2">
                <div v-for="subject in availableSubjects" :key="subject.id" class="flex items-center">
                  <input 
                    type="checkbox" 
                    :id="`subject-${subject.id}`" 
                    :value="subject.id" 
                    v-model="selectedSubjects"
                    class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                  >
                  <label :for="`subject-${subject.id}`" class="ml-2 block text-sm text-gray-900">
                    {{ subject.name }} {{ subject.teacher_name ? `(Teacher: ${subject.teacher_name})` : '' }}
                  </label>
                </div>
              </div>
              
              <div class="mt-4">
                <button 
                  @click="assignSubjects" 
                  :disabled="isSaving || selectedSubjects.length === 0"
                  class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50">
                  {{ isSaving ? 'Saving...' : 'Save Subject Assignments' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="mt-6 text-center">
        <router-link to="/dashboard" class="text-indigo-600 hover:text-indigo-800">
          Back to Dashboard
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ManageStudents',
  data() {
    return {
      students: [],
      availableSubjects: [],
      selectedStudentId: '',
      selectedStudentProfile: null,
      selectedSubjects: [],
      isLoadingStudents: false,
      isLoadingSubjects: false,
      isSaving: false,
      successMessage: '',
      errorMessage: '',
      userRole: localStorage.getItem('userRole') || sessionStorage.getItem('userRole'),
      selectedGrade: '',
      isSavingGrade: false,
      gradeOptions: [
        { value: '1', label: 'Grade 1' },
        { value: '2', label: 'Grade 2' },
        { value: '3', label: 'Grade 3' },
        { value: '4', label: 'Grade 4' },
        { value: '5', label: 'Grade 5' },
        { value: '6', label: 'Grade 6' },
        { value: '7', label: 'Grade 7' },
        { value: '8', label: 'Grade 8' },
        { value: '9', label: 'Grade 9' },
        { value: '10', label: 'Grade 10' },
        { value: '11', label: 'Grade 11' },
        { value: '12', label: 'Grade 12' },
      ]
    };
  },
  mounted() {
    this.fetchStudents();
    this.fetchSubjects();
  },
  methods: {
    async fetchStudents() {
      this.isLoadingStudents = true;
      this.errorMessage = '';
      
      try {
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        // If admin, fetch all students, otherwise get teacher's students
        const endpoint = this.userRole === 'admin' ? 
          'http://127.0.0.1:8000/api/users/?role=student' : 
          'http://127.0.0.1:8000/api/student-profiles/list-students/';
        
        const response = await axios.get(endpoint, {
          headers: { Authorization: `Bearer ${token}` }
        });
        
        this.students = response.data;
      } catch (error) {
        console.error('Error fetching students:', error);
        this.errorMessage = 'Failed to load students. Please try again.';
      } finally {
        this.isLoadingStudents = false;
      }
    },
    
    async fetchSubjects() {
      try {
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:8000/api/subjects/', {
          headers: { Authorization: `Bearer ${token}` }
        });
        
        // If teacher, they can only see their own subjects
        // If admin, they can see all subjects
        this.availableSubjects = response.data;
      } catch (error) {
        console.error('Error fetching subjects:', error);
      }
    },
    
    async loadStudentSubjects() {
      if (!this.selectedStudentId) return;
      
      this.isLoadingSubjects = true;
      this.selectedSubjects = [];
      this.selectedGrade = '';
      this.errorMessage = '';
      
      try {
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        
        console.log("Fetching profile for user ID:", this.selectedStudentId);
        
        // Directly fetch the student profile by ID (more reliable)
        try {
          // First try to find an existing profile for this user
          const profilesResponse = await axios.get(`http://127.0.0.1:8000/api/users/${this.selectedStudentId}/profile/`, {
            headers: { Authorization: `Bearer ${token}` }
          });
          
          console.log("Profile response:", profilesResponse.data);
          
          if (profilesResponse.data) {
            this.selectedStudentProfile = profilesResponse.data;
            
            // Pre-select the subjects this student is already assigned to
            if (this.selectedStudentProfile.subjects) {
              this.selectedSubjects = Array.isArray(this.selectedStudentProfile.subjects) 
                ? this.selectedStudentProfile.subjects.map(id => parseInt(id))
                : [];
            }
            console.log("Selected subjects:", this.selectedSubjects);
          }
        } catch (profileError) {
          console.log("Could not find existing profile:", profileError);
          
          // If no profile exists yet, create one
          try {
            console.log("Creating new profile for student:", this.selectedStudentId);
            
            // Include empty subjects array in the request
            const createResponse = await axios.post(`http://127.0.0.1:8000/api/student-profiles/`, {
              user: parseInt(this.selectedStudentId),
              education_level: "Not specified",
              subjects: [] // Add empty subjects array to satisfy the requirement
            }, {
              headers: { 
                Authorization: `Bearer ${token}`,
                'Content-Type': 'application/json'
              }
            });
            
            console.log("Created profile:", createResponse.data);
            this.selectedStudentProfile = createResponse.data;
            this.selectedSubjects = [];
          } catch (createError) {
            console.error("Failed to create profile:", createError);
            if (createError.response?.data) {
              console.error("Create error details:", createError.response.data);
            }
            throw new Error("Could not create student profile");
          }
        }
        
        // If we got this far but still don't have a profile, something went wrong
        if (!this.selectedStudentProfile) {
          throw new Error("Failed to retrieve or create student profile");
        }
        
        // Set the selected grade if available
        this.selectedGrade = this.selectedStudentProfile.grade || '';
      } catch (error) {
        console.error('Error loading or creating student profile:', error);
        if (error.response?.status === 403) {
          this.errorMessage = 'You do not have permission to access this student profile.';
        } else if (error.response?.data) {
          this.errorMessage = `Error: ${JSON.stringify(error.response.data)}`;
        } else {
          this.errorMessage = 'Failed to load student profile. Please try again.';
        }
        this.selectedStudentProfile = null;
      } finally {
        this.isLoadingSubjects = false;
      }
    },
    
    async assignSubjects() {
      if (!this.selectedStudentProfile) {
        this.errorMessage = 'No student profile selected.';
        return;
      }
      
      this.isSaving = true;
      this.errorMessage = '';
      this.successMessage = '';
      
      try {
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        
        // Debug info
        console.log("Assigning subjects to profile:", {
          profileId: this.selectedStudentProfile.id,
          subjects: this.selectedSubjects
        });
        
        // Make sure subject_ids is an array of integers
        const subjectIds = this.selectedSubjects.map(id => 
          typeof id === 'string' ? parseInt(id, 10) : id
        ).filter(id => !isNaN(id));
        
        if (subjectIds.length === 0) {
          throw new Error("No valid subject IDs selected");
        }
        
        console.log("Sending subject IDs:", subjectIds);
        
        try {
          const response = await axios.post(
            `http://127.0.0.1:8000/api/student-profiles/${this.selectedStudentProfile.id}/assign-subjects/`, 
            { subject_ids: subjectIds },
            { 
              headers: { 
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
              } 
            }
          );
          
          console.log("Assignment response:", response.data);
          this.successMessage = 'Subject assignments updated successfully!';
        } catch (axiosError) {
          console.error("Axios error:", axiosError);
          
          if (axiosError.response) {
            console.error("Response data:", axiosError.response.data);
            console.error("Response status:", axiosError.response.status);
            console.error("Response headers:", axiosError.response.headers);
            
            const errorMsg = axiosError.response.data.error || 
                           `Server error (${axiosError.response.status})`;
            throw new Error(errorMsg);
          } else if (axiosError.request) {
            console.error("Request made but no response:", axiosError.request);
            throw new Error("Network error: No response from server");
          } else {
            throw axiosError;
          }
        }
      } catch (error) {
        console.error('Error in assignSubjects:', error);
        this.errorMessage = error.message || 'Failed to update subject assignments. Please try again.';
      } finally {
        this.isSaving = false;
      }
    },
    
    async updateStudentGrade() {
      if (!this.selectedStudentProfile || !this.selectedGrade) return;
      
      this.isSavingGrade = true;
      this.errorMessage = '';
      this.successMessage = '';
      
      try {
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        
        await axios.patch(
          `http://127.0.0.1:8000/api/student-profiles/${this.selectedStudentProfile.id}/`, 
          { grade: this.selectedGrade },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        
        this.successMessage = 'Student grade updated successfully!';
      } catch (error) {
        console.error('Error updating grade:', error);
        this.errorMessage = 'Failed to update student grade. Please try again.';
      } finally {
        this.isSavingGrade = false;
      }
    },
    
    getSelectedStudentName() {
      const student = this.students.find(s => s.id === this.selectedStudentId);
      if (student) {
        return `${student.first_name} ${student.last_name}`;
      }
      return 'Selected Student';
    }
  }
};
</script>
