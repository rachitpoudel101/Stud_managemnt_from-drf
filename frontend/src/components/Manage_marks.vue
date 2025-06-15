<template>
  <div class="bg-gray-100 min-h-screen p-6">
    <div class="max-w-4xl mx-auto bg-white rounded-lg shadow-md p-6">
      <h1 class="text-2xl font-bold text-center mb-6">Manage Student Marks</h1>
      
      <!-- Success & Error Messages -->
      <div v-if="successMessage" class="mb-4 p-3 bg-green-100 border border-green-400 text-green-700 rounded">
        {{ successMessage }}
      </div>
      
      <div v-if="errorMessage" class="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
        {{ errorMessage }}
      </div>
      
      <!-- Debug Info (Development only) -->
      <div v-if="debug" class="mb-4 p-3 bg-gray-100 border border-gray-300 text-gray-700 rounded text-xs">
        <h4 class="font-bold mb-1">Debug Info:</h4>
        <pre>{{ debugInfo }}</pre>
      </div>
      
      <!-- Subject Selection -->
      <div class="mb-6">
        <label class="block text-sm font-medium text-gray-700 mb-2">Select Subject</label>
        <div v-if="isLoading" class="text-gray-500">Loading subjects...</div>
        <div v-else-if="subjects.length === 0" class="text-red-500">
          You don't have any subjects assigned. Please contact an administrator.
        </div>
        <select 
          v-else
          v-model="selectedSubject" 
          @change="loadStudents"
          class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        >
          <option value="">-- Select a Subject --</option>
          <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
            {{ subject.name }}
          </option>
        </select>
      </div>
      
      <!-- Students & Marks Form -->
      <div v-if="selectedSubject && students.length > 0" class="mb-6">
        <h2 class="text-xl font-semibold mb-4">Enter Marks</h2>
        
        <div class="overflow-x-auto">
          <table class="min-w-full bg-white">
            <thead>
              <tr>
                <th class="py-2 px-4 border-b border-gray-200 bg-gray-50 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                  Student
                </th>
                <th class="py-2 px-4 border-b border-gray-200 bg-gray-50 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                  Marks
                </th>
                <th class="py-2 px-4 border-b border-gray-200 bg-gray-50 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                  Status
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="student in students" :key="student.id">
                <td class="py-2 px-4 border-b border-gray-200">
                  {{ student.first_name }} {{ student.last_name }}
                </td>
                <td class="py-2 px-4 border-b border-gray-200">
                  <input 
                    type="number" 
                    min="0" 
                    max="100" 
                    v-model.number="marksData[student.id]" 
                    class="w-full px-2 py-1 border border-gray-300 rounded-md"
                  >
                </td>
                <td class="py-2 px-4 border-b border-gray-200">
                  <span v-if="studentMarkStatus[student.id]" 
                        :class="{'text-green-600': studentMarkStatus[student.id].published, 'text-yellow-600': !studentMarkStatus[student.id].published}">
                    {{ studentMarkStatus[student.id].published ? 'Published' : 'Saved (Unpublished)' }}
                  </span>
                  <span v-else class="text-gray-400">Not saved</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div class="mt-6 flex flex-col sm:flex-row space-y-3 sm:space-y-0 sm:space-x-3 justify-center">
          <button 
            @click="saveMarks" 
            :disabled="isSaving"
            class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50">
            {{ isSaving ? 'Saving...' : 'Save Marks' }}
          </button>
          
          <button 
            @click="publishMarks" 
            :disabled="isPublishing || Object.keys(marksData).length === 0"
            class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 disabled:opacity-50">
            {{ isPublishing ? 'Publishing...' : 'Publish Results' }}
          </button>
        </div>
      </div>
      
      <div v-else-if="selectedSubject && isLoadingStudents" class="text-center py-8">
        <p class="text-gray-500">Loading students...</p>
      </div>
      
      <div v-else-if="selectedSubject && students.length === 0" class="text-center py-8">
        <p class="text-red-500">No students found for this subject.</p>
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
  name: 'ManageMarks',
  data() {
    return {
      subjects: [],
      students: [],
      selectedSubject: '',
      marksData: {},  // student_id -> marks
      studentMarkStatus: {}, // student_id -> {published: bool, mark_id: id}
      isLoading: false,
      isLoadingStudents: false,
      isSaving: false,
      isPublishing: false,
      successMessage: '',
      errorMessage: '',
      debug: process.env.NODE_ENV !== 'production', // Only enable in development
      debugInfo: ''
    };
  },
  mounted() {
    this.fetchSubjects();
  },
  methods: {
    async fetchSubjects() {
      this.isLoading = true;
      this.errorMessage = '';
      
      try {
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:8000/api/subjects/', {
          headers: { Authorization: `Bearer ${token}` }
        });
        
        this.subjects = response.data;
        if (this.debug) {
          this.debugInfo = `Fetched ${this.subjects.length} subjects`;
        }
      } catch (error) {
        console.error('Error fetching subjects:', error);
        this.errorMessage = 'Failed to load subjects. Please try again.';
      } finally {
        this.isLoading = false;
      }
    },
    
    async loadStudents() {
      if (!this.selectedSubject) return;
      
      this.students = [];
      this.marksData = {};
      this.studentMarkStatus = {};
      this.isLoadingStudents = true;
      this.errorMessage = '';
      this.debugInfo = '';
      
      try {
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        
        // Get the selected subject
        const subject = this.subjects.find(s => s.id === this.selectedSubject);
        if (!subject) {
          throw new Error('Subject not found');
        }
        
        if (this.debug) {
          this.debugInfo += `Selected subject: ${subject.name} (ID: ${subject.id})\n`;
        }
        
        // Fetch student profiles that have this subject
        const profilesResponse = await axios.get(`http://127.0.0.1:8000/api/student-profiles/?subject=${this.selectedSubject}`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        
        const studentProfiles = profilesResponse.data;
        
        if (this.debug) {
          this.debugInfo += `Fetched ${studentProfiles.length} student profiles\n`;
          if (studentProfiles.length > 0) {
            this.debugInfo += `Sample profile: ${JSON.stringify(studentProfiles[0])}\n`;
          }
        }
        
        // Process student profiles
        for (const profile of studentProfiles) {
          if (profile.user_details) {
            const user = profile.user_details;
            const student = {
              id: profile.id,
              userId: user.id,
              username: user.username,
              first_name: user.first_name || 'No name',
              last_name: user.last_name || '',
              email: user.email || ''
            };
            this.students.push(student);
          } else {
            console.warn('Student profile without user details:', profile);
          }
        }
        
        if (this.debug) {
          this.debugInfo += `Processed ${this.students.length} students\n`;
        }
        
        // Fetch existing marks for this subject
        if (this.students.length > 0) {
          const marksResponse = await axios.get(`http://127.0.0.1:8000/api/marks/?subject=${this.selectedSubject}`, {
            headers: { Authorization: `Bearer ${token}` }
          });
          
          const marks = marksResponse.data;
          
          if (this.debug) {
            this.debugInfo += `Fetched ${marks.length} marks records\n`;
          }
          
          // Add existing marks
          for (const mark of marks) {
            const studentId = mark.student;
            this.marksData[studentId] = mark.marks;
            this.studentMarkStatus[studentId] = {
              published: mark.published || false,
              mark_id: mark.id
            };
          }
        }
      } catch (error) {
        console.error('Error loading students:', error);
        this.errorMessage = 'Failed to load students. Please try again.';
        
        if (this.debug && error.response) {
          this.debugInfo += `Error response: ${JSON.stringify(error.response.data)}\n`;
          this.debugInfo += `Status: ${error.response.status}\n`;
        } else if (this.debug) {
          this.debugInfo += `Error: ${error.message}\n`;
        }
      } finally {
        this.isLoadingStudents = false;
      }
    },
    
    async saveMarks() {
      if (!this.selectedSubject || Object.keys(this.marksData).length === 0) return;
      
      this.isSaving = true;
      this.errorMessage = '';
      this.successMessage = '';
      
      try {
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        const marksData = [];
        
        // Format the data for the bulk create/update endpoint
        for (const studentId in this.marksData) {
          if (this.marksData[studentId] !== null && this.marksData[studentId] !== undefined) {
            marksData.push({
              student_id: parseInt(studentId),
              marks: parseFloat(this.marksData[studentId])
            });
          }
        }
        
        const response = await axios.post('http://127.0.0.1:8000/api/marks/bulk-create/', {
          subject_id: this.selectedSubject,
          marks_data: marksData
        }, {
          headers: { Authorization: `Bearer ${token}` }
        });
        
        this.successMessage = `Saved marks successfully. Created: ${response.data.created}, Updated: ${response.data.updated}`;
        
        // Refresh the students and marks data
        await this.loadStudents();
        
      } catch (error) {
        console.error('Error saving marks:', error);
        this.errorMessage = 'Failed to save marks. Please try again.';
      } finally {
        this.isSaving = false;
      }
    },
    
    async publishMarks() {
      if (!this.selectedSubject) return;
      
      this.isPublishing = true;
      this.errorMessage = '';
      this.successMessage = '';
      
      try {
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        
        // Get student IDs to publish
        const studentIds = Object.keys(this.marksData)
          .filter(id => this.marksData[id] !== null && this.marksData[id] !== undefined)
          .map(id => parseInt(id));
        
        if (studentIds.length === 0) {
          this.errorMessage = 'No marks to publish';
          this.isPublishing = false;
          return;
        }
        
        const response = await axios.post('http://127.0.0.1:8000/api/marks/publish/', {
          subject_id: this.selectedSubject,
          student_ids: studentIds,
          publish_all: false
        }, {
          headers: { Authorization: `Bearer ${token}` }
        });
        
        this.successMessage = `Published ${response.data.count} results successfully`;
        
        // Refresh the students and marks data
        await this.loadStudents();
        
      } catch (error) {
        console.error('Error publishing marks:', error);
        this.errorMessage = 'Failed to publish marks. Please try again.';
      } finally {
        this.isPublishing = false;
      }
    }
  }
};
</script>
