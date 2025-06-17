<template>
  <div class="bg-gray-100 min-h-screen p-6">
    <div class="max-w-4xl mx-auto bg-white rounded-lg shadow-md p-6">
      <h1 class="text-2xl font-bold text-center mb-6">
        {{ isAdmin ? 'Student Results' : 'My Results' }}
      </h1>
      
      <!-- Error Message -->
      <div v-if="errorMessage" class="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
        {{ errorMessage }}
      </div>
      
      <!-- Admin Controls -->
      <div v-if="isAdmin && students.length > 0" class="mb-6">
        <label for="student-select" class="block text-sm font-medium text-gray-700 mb-1">Select Student</label>
        <select
          id="student-select"
          v-model="selectedStudent"
          @change="selectedStudent && fetchResultsByStudent(selectedStudent)"
          class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        >
          <option value="">All Students</option>
          <option v-for="student in students" :key="student.id" :value="student.id">
            {{ student.first_name }} {{ student.last_name }} ({{ student.username }})
          </option>
        </select>
      </div>
      
      <div v-if="isLoading" class="text-center py-8">
        <p class="text-gray-500">Loading results...</p>
      </div>
      
      <div v-else-if="results.length === 0" class="text-center py-8">
        <p class="text-gray-500">No published results found.</p>
      </div>
      
      <div v-else>
        <div class="overflow-x-auto">
          <table class="min-w-full bg-white">
            <thead>
              <tr>
                <th class="py-2 px-4 border-b border-gray-200 bg-gray-50 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                  Subject
                </th>
                <th class="py-2 px-4 border-b border-gray-200 bg-gray-50 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                  Marks
                </th>
                <th class="py-2 px-4 border-b border-gray-200 bg-gray-50 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                  Grade
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="result in results" :key="result.id">
                <td class="py-2 px-4 border-b border-gray-200">
                  {{ result.subject_name }}
                </td>
                <td class="py-2 px-4 border-b border-gray-200">
                  {{ result.marks }}
                </td>
                <td class="py-2 px-4 border-b border-gray-200">
                  {{ getGrade(result.marks) }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div class="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4 text-center">
          <p class="text-blue-700 font-medium">
            Average Marks: <span class="font-bold">{{ averageMarks }}</span>
          </p>
          <p class="text-blue-700 font-medium">
            Overall Grade: <span class="font-bold">{{ overallGrade }}</span>
          </p>
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
  name: 'ViewResults',
  data() {
    return {
      results: [],
      isLoading: false,
      errorMessage: '',
      isAdmin: false,
      selectedStudent: null,
      students: []
    };
  },
  computed: {
    averageMarks() {
      if (this.results.length === 0) return 0;
      
      const sum = this.results.reduce((total, result) => total + result.marks, 0);
      return (sum / this.results.length).toFixed(2);
    },
    overallGrade() {
      return this.getGrade(this.averageMarks);
    }
  },
  mounted() {
    this.isAdmin = localStorage.getItem('userRole') === 'admin' || sessionStorage.getItem('userRole') === 'admin';
    
    // If admin, fetch all students first
    if (this.isAdmin) {
      this.fetchStudents();
    } else {
      // Regular student view - fetch their own results
      this.fetchResults();
    }
  },
  methods: {
    async fetchStudents() {
      try {
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:8000/api/users/', {
          params: { role: 'student' }, 
          headers: { Authorization: `Bearer ${token}` }
        });
        
        // Filter to only include students
        this.students = response.data.filter(user => user.role === 'student');
        
        // If we have a subjectId parameter, we're looking for results of a specific subject
        const subjectId = this.$route.query.subjectId;
        if (subjectId) {
          this.fetchResultsBySubject(subjectId);
        }
      } catch (error) {
        console.error('Error fetching students:', error);
        this.errorMessage = 'Failed to load students. Please try again.';
      }
    },
    
    async fetchResultsBySubject(subjectId) {
      this.isLoading = true;
      this.errorMessage = '';
      
      try {
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:8000/api/marks/', {
          headers: { Authorization: `Bearer ${token}` },
          params: { subject: subjectId }
        });
        
        this.results = response.data;
      } catch (error) {
        console.error('Error fetching results by subject:', error);
        this.errorMessage = 'Failed to load results for this subject. Please try again.';
      } finally {
        this.isLoading = false;
      }
    },
    
    async fetchResultsByStudent(studentId) {
      // Admin function to view a specific student's results
      this.isLoading = true;
      this.errorMessage = '';
      
      try {
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:8000/api/marks/', {
          headers: { Authorization: `Bearer ${token}` },
          params: { student: studentId }
        });
        
        this.results = response.data;
      } catch (error) {
        console.error('Error fetching results by student:', error);
        this.errorMessage = 'Failed to load results for this student. Please try again.';
      } finally {
        this.isLoading = false;
      }
    },
    
    async fetchResults() {
      // Existing function for students to view their own results
      this.isLoading = true;
      this.errorMessage = '';
      
      try {
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:8000/api/marks/', {
          headers: { Authorization: `Bearer ${token}` }
        });
        
        this.results = response.data;
      } catch (error) {
        console.error('Error fetching results:', error);
        this.errorMessage = 'Failed to load results. Please try again.';
      } finally {
        this.isLoading = false;
      }
    },
    getGrade(marks) {
      if (marks >= 90) return 'A+';
      if (marks >= 80) return 'A';
      if (marks >= 70) return 'B+';
      if (marks >= 60) return 'B';
      if (marks >= 50) return 'C+';
      if (marks >= 40) return 'C';
      return 'F';
    }
  }
};
</script>
