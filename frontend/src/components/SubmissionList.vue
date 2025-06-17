<template>
  <div class="bg-white shadow rounded-lg">
    <div class="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
      <h3 class="text-lg leading-6 font-medium text-gray-900">
        {{ userRole === 'student' ? 'My Submissions' : 'Student Submissions' }}
      </h3>
      <button 
        @click="loadSubmissions" 
        class="text-sm text-blue-600 hover:text-blue-800"
      >
        Refresh
      </button>
    </div>
    <div class="px-6 py-4">
      <div v-if="isLoading" class="text-center py-4">
        <p class="text-gray-500">Loading submissions...</p>
      </div>
      
      <div v-else-if="submissions.length === 0" class="text-center py-4">
        <p class="text-gray-500">No submissions found.</p>
      </div>
      
      <div v-else class="space-y-4">
        <div v-for="submission in submissions" :key="submission.id" class="border border-gray-200 rounded-md p-4">
          <div class="flex justify-between items-start gap-4">
            <div class="flex-1 min-w-0">
              <h4 class="text-lg font-medium text-gray-900">{{ submission.assignment_title }}</h4>
              <p v-if="submission.comments" class="text-sm text-gray-600 mt-1">{{ submission.comments }}</p>
              <div class="mt-2 text-xs text-gray-500 flex flex-wrap gap-4">
                <span v-if="userRole !== 'student'">Student: {{ submission.student_name }}</span>
                <span>Submitted: {{ formatDate(submission.submitted_at) }}</span>
              </div>
              <!-- Display submission file info -->
              <div v-if="submission.file" class="mt-3 p-2 bg-gray-50 rounded border">
                <div class="flex items-center gap-2">
                  <div class="flex-1 min-w-0">
                    <span class="text-sm text-gray-700 block truncate">📎 {{ getFileName(submission.file) }}</span>
                  </div>
                  <div class="flex gap-1 flex-shrink-0">
                    <button 
                      @click="viewFile(submission.file)" 
                      class="px-2 py-1 text-xs bg-blue-100 text-blue-700 rounded hover:bg-blue-200 whitespace-nowrap"
                    >
                      View
                    </button>
                    <button 
                      @click="downloadFile(submission.file)" 
                      class="px-2 py-1 text-xs bg-green-100 text-green-700 rounded hover:bg-green-200 whitespace-nowrap"
                    >
                      Download
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <div class="flex flex-col gap-1 flex-shrink-0">
              <!-- Only students can edit/delete their submissions -->
              <button 
                v-if="userRole === 'student'"
                @click="editSubmission(submission)" 
                class="px-2 py-1 text-xs bg-blue-100 text-blue-700 rounded hover:bg-blue-200 whitespace-nowrap"
              >
                Edit
              </button>
              <button 
                v-if="userRole === 'student'"
                @click="deleteSubmission(submission.id)" 
                class="px-2 py-1 text-xs bg-red-100 text-red-700 rounded hover:bg-red-200 whitespace-nowrap"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Edit Submission Modal - Only for students -->
    <div v-if="showEditModal && userRole === 'student'" class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md mx-4">
        <h3 class="text-lg font-medium text-gray-900 mb-4">Edit Submission</h3>
        
        <div class="mb-4 p-3 bg-blue-50 rounded-md">
          <h4 class="font-medium text-blue-900">{{ editingSubmission.assignment_title }}</h4>
        </div>
        
        <!-- Show current file info -->
        <div v-if="editingSubmission.file" class="mb-4 p-3 bg-gray-50 rounded-md">
          <p class="text-sm text-gray-700">
            <strong>Current file:</strong> 
            <a :href="getFileUrl(editingSubmission.file)" target="_blank" class="text-blue-600 hover:text-blue-800 ml-1">
              📎 {{ getFileName(editingSubmission.file) }}
            </a>
          </p>
        </div>
        
        <form @submit.prevent="updateSubmission" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              {{ editingSubmission.file ? 'Replace File (Optional)' : 'Upload File' }}
            </label>
            <input 
              type="file" 
              @change="handleFileChange"
              class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
            />
            <p v-if="editingSubmission.file" class="text-xs text-gray-500 mt-1">
              Leave empty to keep current file
            </p>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Comments</label>
            <textarea 
              v-model="editSubmissionData.comments" 
              rows="3"
              placeholder="Add any comments about your submission..."
              class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            ></textarea>
          </div>
          
          <div v-if="errorMessage" class="text-red-600 text-sm">
            {{ errorMessage }}
          </div>
          
          <div class="flex justify-end space-x-3">
            <button 
              type="button"
              @click="closeEditModal" 
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 border border-gray-300 rounded-md hover:bg-gray-200"
            >
              Cancel
            </button>
            <button 
              type="submit"
              :disabled="isUpdating"
              class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 disabled:opacity-50"
            >
              {{ isUpdating ? 'Updating...' : 'Update Submission' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SubmissionList',
  props: {
    userRole: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      submissions: [],
      isLoading: false,
      userId: null,
      showEditModal: false,
      editingSubmission: null,
      editSubmissionData: {
        comments: ''
      },
      selectedFile: null,
      isUpdating: false,
      errorMessage: ''
    };
  },
  mounted() {
    this.getUserId();
    this.loadSubmissions();
  },
  methods: {
    getUserId() {
      const userStr = localStorage.getItem('user') || sessionStorage.getItem('user');
      if (userStr) {
        try {
          const user = JSON.parse(userStr);
          this.userId = user.id;
        } catch (e) {
          console.error('Error parsing user data:', e);
        }
      }
    },
    
    async loadSubmissions() {
      this.isLoading = true;
      
      try {
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:8000/api/submissions/', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        
        this.submissions = response.data;
      } catch (error) {
        console.error('Error loading submissions:', error);
      } finally {
        this.isLoading = false;
      }
    },
    
    editSubmission(submission) {
      this.editingSubmission = submission;
      this.editSubmissionData = {
        comments: submission.comments || ''
      };
      this.selectedFile = null;
      this.errorMessage = '';
      this.showEditModal = true;
    },
    
    closeEditModal() {
      this.showEditModal = false;
      this.editingSubmission = null;
      this.editSubmissionData = { comments: '' };
      this.selectedFile = null;
      this.errorMessage = '';
    },
    
    handleFileChange(event) {
      this.selectedFile = event.target.files[0];
    },
    
    async updateSubmission() {
      this.isUpdating = true;
      this.errorMessage = '';
      
      try {
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        
        // Only send fields that have changed
        const updateData = {};
        
        // Always include comments (even if empty)
        updateData.comments = this.editSubmissionData.comments || '';
        
        // Only include file if a new one was selected
        if (this.selectedFile) {
          const formData = new FormData();
          formData.append('comments', updateData.comments);
          formData.append('file', this.selectedFile);
          
          await axios.patch(`http://127.0.0.1:8000/api/submissions/${this.editingSubmission.id}/`, formData, {
            headers: { 
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'multipart/form-data'
            }
          });
        } else {
          // If no new file, just update comments (don't touch the file field)
          await axios.patch(`http://127.0.0.1:8000/api/submissions/${this.editingSubmission.id}/`, {
            comments: updateData.comments
          }, {
            headers: { 
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            }
          });
        }
        
        this.closeEditModal();
        this.loadSubmissions();
        alert('Submission updated successfully!');
      } catch (error) {
        console.error('Error updating submission:', error);
        if (error.response?.data?.detail) {
          this.errorMessage = error.response.data.detail;
        } else if (error.response?.data?.error) {
          this.errorMessage = error.response.data.error;
        } else {
          this.errorMessage = 'Failed to update submission. Please try again.';
        }
      } finally {
        this.isUpdating = false;
      }
    },
    
    getFileUrl(fileUrl) {
      if (fileUrl.startsWith('http://') || fileUrl.startsWith('https://')) {
        return fileUrl;
      } else {
        const baseUrl = 'http://127.0.0.1:8000';
        const cleanPath = fileUrl.startsWith('/') ? fileUrl : `/${fileUrl}`;
        return `${baseUrl}${cleanPath}`;
      }
    },
    
    getFileName(fileUrl) {
      // Extract filename from URL
      const parts = fileUrl.split('/');
      return parts[parts.length - 1];
    },
    
    viewFile(fileUrl) {
      const fullUrl = this.getFileUrl(fileUrl);
      window.open(fullUrl, '_blank');
    },
    
    downloadFile(fileUrl) {
      const fullUrl = this.getFileUrl(fileUrl);
      
      // Create a temporary anchor element to trigger download
      const link = document.createElement('a');
      link.href = fullUrl;
      link.download = this.getFileName(fileUrl);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    },
    
    async deleteSubmission(submissionId) {
      if (!confirm('Are you sure you want to delete this submission?')) return;
      
      try {
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        await axios.delete(`http://127.0.0.1:8000/api/submissions/${submissionId}/`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        
        this.submissions = this.submissions.filter(s => s.id !== submissionId);
        alert('Submission deleted successfully!');
      } catch (error) {
        console.error('Error deleting submission:', error);
        if (error.response?.data?.detail) {
          alert(`Failed to delete submission: ${error.response.data.detail}`);
        } else {
          alert('Failed to delete submission. Please try again.');
        }
      }
    },
    
    formatDate(dateString) {
      return new Date(dateString).toLocaleString();
    }
  }
};
</script>

<style scoped>
.flex-shrink-0 {
  flex-shrink: 0;
}

.min-w-0 {
  min-width: 0;
}

.whitespace-nowrap {
  white-space: nowrap;
}

.gap-1 {
  gap: 0.25rem;
}

.gap-2 {
  gap: 0.5rem;
}

.gap-4 {
  gap: 1rem;
}

.truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
