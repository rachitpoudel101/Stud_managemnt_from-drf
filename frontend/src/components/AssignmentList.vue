<template>
  <div class="bg-white shadow rounded-lg">
    <div class="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
      <h3 class="text-lg leading-6 font-medium text-gray-900">Assignments</h3>
      <div class="flex space-x-2">
        <button 
          v-if="userRole === 'teacher' || userRole === 'admin'"
          @click="showCreateModal = true" 
          class="text-sm bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700"
        >
          Create Assignment
        </button>
        <button 
          @click="loadAssignments" 
          class="text-sm text-blue-600 hover:text-blue-800"
        >
          Refresh
        </button>
      </div>
    </div>
    <div class="px-6 py-4">
      <div v-if="isLoading" class="text-center py-4">
        <p class="text-gray-500">Loading assignments...</p>
      </div>
      
      <div v-else-if="assignments.length === 0" class="text-center py-4">
        <p class="text-gray-500">No assignments available.</p>
      </div>
      
      <div v-else class="space-y-4">
        <div v-for="assignment in assignments" :key="assignment.id" class="border border-gray-200 rounded-md p-4">
          <div class="flex justify-between items-start">
            <div class="flex-1">
              <h4 class="text-lg font-medium text-gray-900">{{ assignment.title }}</h4>
              <p class="text-sm text-gray-600 mt-1">{{ assignment.description }}</p>
              <div class="mt-2 text-xs text-gray-500 flex flex-wrap gap-4">
                <span>Subject: {{ assignment.subject_name }}</span>
                <span>Due: {{ formatDate(assignment.due_date) }}</span>
                <span>Created by: {{ assignment.created_by_name }}</span>
              </div>
              <!-- Display assignment file info -->
              <div v-if="assignment.file" class="mt-3 p-2 bg-blue-50 rounded border">
                <div class="flex items-center justify-between">
                  <div class="flex items-center">
                    <span class="text-sm text-blue-700">📁 Assignment File: {{ getFileName(assignment.file) }}</span>
                  </div>
                  <div class="flex space-x-2">
                    <button 
                      @click="viewFile(assignment.file)" 
                      class="text-blue-600 hover:text-blue-800 text-sm"
                    >
                      View
                    </button>
                    <button 
                      @click="downloadFile(assignment.file)" 
                      class="text-green-600 hover:text-green-800 text-sm"
                    >
                      Download
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <div class="flex space-x-2 ml-4">
              <button 
                v-if="userRole === 'student'"
                @click="submitAssignment(assignment)" 
                class="text-green-600 hover:text-green-800 text-sm"
              >
                Submit
              </button>
              <button 
                v-if="canEditAssignment(assignment)"
                @click="editAssignment(assignment)" 
                class="text-blue-600 hover:text-blue-800 text-sm"
              >
                Edit
              </button>
              <button 
                v-if="canEditAssignment(assignment)"
                @click="deleteAssignment(assignment.id)" 
                class="text-red-600 hover:text-red-800 text-sm"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Create Assignment Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-2xl mx-4 max-h-screen overflow-y-auto">
        <h3 class="text-lg font-medium text-gray-900 mb-4">Create Assignment</h3>
        <form @submit.prevent="createAssignment" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Title</label>
            <input 
              type="text" 
              v-model="newAssignment.title" 
              required
              class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
            <textarea 
              v-model="newAssignment.description" 
              rows="3"
              required
              class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            ></textarea>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Subject</label>
            <select 
              v-model="newAssignment.subject"
              required
              class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            >
              <option value="">Select Subject</option>
              <option v-for="subject in teacherSubjects" :key="subject.id" :value="subject.id">
                {{ subject.name }}
              </option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Due Date</label>
            <input 
              type="datetime-local" 
              v-model="newAssignment.due_date" 
              required
              class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">File (Optional)</label>
            <input 
              type="file" 
              @change="handleFileChange"
              class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Audience</label>
            <select 
              v-model="newAssignment.audience"
              class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            >
              <option value="student">Students</option>
              <option v-if="userRole === 'admin'" value="teacher">Teachers</option>
              <option v-if="userRole === 'admin'" value="both">Both</option>
            </select>
          </div>
          <div class="flex justify-end space-x-3">
            <button 
              type="button"
              @click="closeCreateModal" 
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 border border-gray-300 rounded-md hover:bg-gray-200"
            >
              Cancel
            </button>
            <button 
              type="submit"
              :disabled="isCreating"
              class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 disabled:opacity-50"
            >
              {{ isCreating ? 'Creating...' : 'Create Assignment' }}
            </button>
          </div>
        </form>
      </div>
    </div>
    
    <!-- Edit Assignment Modal -->
    <div v-if="showEditModal" class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-2xl mx-4 max-h-screen overflow-y-auto">
        <h3 class="text-lg font-medium text-gray-900 mb-4">Edit Assignment</h3>
        <form @submit.prevent="updateAssignment" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Title</label>
            <input 
              type="text" 
              v-model="editAssignmentData.title" 
              required
              class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
            <textarea 
              v-model="editAssignmentData.description" 
              rows="3"
              required
              class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            ></textarea>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Subject</label>
            <select 
              v-model="editAssignmentData.subject"
              required
              class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            >
              <option value="">Select Subject</option>
              <option v-for="subject in teacherSubjects" :key="subject.id" :value="subject.id">
                {{ subject.name }}
              </option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Due Date</label>
            <input 
              type="datetime-local" 
              v-model="editAssignmentData.due_date" 
              required
              class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Replace File (Optional)</label>
            <input 
              type="file" 
              @change="handleEditFileChange"
              class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
            />
            <p class="text-xs text-gray-500 mt-1">Leave empty to keep current file</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Audience</label>
            <select 
              v-model="editAssignmentData.audience"
              class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            >
              <option value="student">Students</option>
              <option v-if="userRole === 'admin'" value="teacher">Teachers</option>
              <option v-if="userRole === 'admin'" value="both">Both</option>
            </select>
          </div>
          <div class="flex items-center">
            <input 
              type="checkbox" 
              id="edit-published" 
              v-model="editAssignmentData.published"
              class="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            <label for="edit-published" class="ml-2 block text-sm text-gray-900">Published</label>
          </div>
          
          <div v-if="editErrorMessage" class="text-red-600 text-sm">
            {{ editErrorMessage }}
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
              {{ isUpdating ? 'Updating...' : 'Update Assignment' }}
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
  name: 'AssignmentList',
  props: {
    userRole: {
      type: String,
      required: true
    },
    teacherSubjects: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      assignments: [],
      isLoading: false,
      userId: null,
      showCreateModal: false,
      isCreating: false,
      newAssignment: {
        title: '',
        description: '',
        subject: '',
        due_date: '',
        audience: 'student',
        published: true
      },
      selectedFile: null,
      showEditModal: false,
      editingAssignment: null,
      editAssignmentData: {
        title: '',
        description: '',
        subject: '',
        due_date: '',
        audience: 'student',
        published: true
      },
      editSelectedFile: null,
      isUpdating: false,
      editErrorMessage: ''
    };
  },
  mounted() {
    this.getUserId();
    this.loadAssignments();
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
    
    async loadAssignments() {
      this.isLoading = true;
      
      try {
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:8000/api/assignments/', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        
        this.assignments = response.data;
        console.log('Loaded assignments for', this.userRole, ':', this.assignments);
      } catch (error) {
        console.error('Error loading assignments:', error);
      } finally {
        this.isLoading = false;
      }
    },
    
    canEditAssignment(assignment) {
      console.log('canEditAssignment check:', {
        userRole: this.userRole,
        userId: this.userId,
        assignmentCreatedBy: assignment.created_by,
        isAdmin: this.userRole === 'admin'
      });
      
      // Admin can edit any assignment
      if (this.userRole === 'admin') return true;
      // Teachers can only edit assignments they created
      if (this.userRole === 'teacher') {
        return String(assignment.created_by) === String(this.userId);
      }
      return false;
    },
    
    async deleteAssignment(assignmentId) {
      if (!confirm('Are you sure you want to delete this assignment?')) return;
      
      try {
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        await axios.delete(`http://127.0.0.1:8000/api/assignments/${assignmentId}/`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        
        this.assignments = this.assignments.filter(a => a.id !== assignmentId);
      } catch (error) {
        console.error('Error deleting assignment:', error);
        alert('Failed to delete assignment. Please try again.');
      }
    },
    
    handleFileChange(event) {
      this.selectedFile = event.target.files[0];
    },
    
    async createAssignment() {
      this.isCreating = true;
      
      try {
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        const formData = new FormData();
        
        // Add all assignment data to FormData
        Object.keys(this.newAssignment).forEach(key => {
          if (this.newAssignment[key] !== null && this.newAssignment[key] !== '') {
            formData.append(key, this.newAssignment[key]);
          }
        });
        
        // Add file if selected
        if (this.selectedFile) {
          formData.append('file', this.selectedFile);
        }
        
        console.log('Creating assignment with data:', {
          ...this.newAssignment,
          hasFile: !!this.selectedFile,
          userRole: this.userRole
        });
        
        const response = await axios.post('http://127.0.0.1:8000/api/assignments/', formData, {
          headers: { 
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'multipart/form-data'
          }
        });
        
        console.log('Assignment created successfully:', response.data);
        this.closeCreateModal();
        this.loadAssignments();
        alert('Assignment created successfully!');
      } catch (error) {
        console.error('Error creating assignment:', error);
        if (error.response?.data) {
          console.error('Error details:', error.response.data);
          alert(`Failed to create assignment: ${JSON.stringify(error.response.data)}`);
        } else {
          alert('Failed to create assignment. Please try again.');
        }
      } finally {
        this.isCreating = false;
      }
    },
    
    closeCreateModal() {
      this.showCreateModal = false;
      this.newAssignment = {
        title: '',
        description: '',
        subject: '',
        due_date: '',
        audience: 'student',
        published: true
      };
      this.selectedFile = null;
    },
    
    formatDate(dateString) {
      return new Date(dateString).toLocaleString();
    },
    
    getFileName(fileUrl) {
      if (!fileUrl) return 'Unknown file';
      // Extract filename from URL
      const parts = fileUrl.split('/');
      return parts[parts.length - 1];
    },
    
    getFileUrl(fileUrl) {
      if (!fileUrl) return '';
      
      if (fileUrl.startsWith('http://') || fileUrl.startsWith('https://')) {
        return fileUrl;
      } else {
        // Remove leading slash if present and construct proper URL
        const cleanPath = fileUrl.startsWith('/') ? fileUrl.substring(1) : fileUrl;
        return `http://127.0.0.1:8000/media/${cleanPath}`;
      }
    },
    
    viewFile(fileUrl) {
      const fullUrl = this.getFileUrl(fileUrl);
      console.log('Viewing file:', fullUrl);
      
      // Open file in new tab for viewing
      window.open(fullUrl, '_blank');
    },
    
    downloadFile(fileUrl) {
      const fullUrl = this.getFileUrl(fileUrl);
      console.log('Downloading file:', fullUrl);
      
      // Create a temporary anchor element to trigger download
      const link = document.createElement('a');
      link.href = fullUrl;
      link.download = this.getFileName(fileUrl);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    },
    
    submitAssignment(assignment) {
      this.$emit('submit-assignment', assignment);
    },
    
    editAssignment(assignment) {
      this.editingAssignment = assignment;
      
      // Format the due_date for datetime-local input
      const dueDate = new Date(assignment.due_date);
      const formattedDate = dueDate.toISOString().slice(0, 16);
      
      this.editAssignmentData = {
        title: assignment.title,
        description: assignment.description,
        subject: assignment.subject,
        due_date: formattedDate,
        audience: assignment.audience,
        published: assignment.published
      };
      this.editSelectedFile = null;
      this.editErrorMessage = '';
      this.showEditModal = true;
    },
    
    closeEditModal() {
      this.showEditModal = false;
      this.editingAssignment = null;
      this.editAssignmentData = {
        title: '',
        description: '',
        subject: '',
        due_date: '',
        audience: 'student',
        published: true
      };
      this.editSelectedFile = null;
      this.editErrorMessage = '';
    },
    
    handleEditFileChange(event) {
      this.editSelectedFile = event.target.files[0];
    },
    
    async updateAssignment() {
      this.isUpdating = true;
      this.editErrorMessage = '';
      
      try {
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        const formData = new FormData();
        
        // Add all assignment data to FormData
        Object.keys(this.editAssignmentData).forEach(key => {
          if (this.editAssignmentData[key] !== null && this.editAssignmentData[key] !== '') {
            formData.append(key, this.editAssignmentData[key]);
          }
        });
        
        // Add new file if selected
        if (this.editSelectedFile) {
          formData.append('file', this.editSelectedFile);
        }
        
        console.log('Updating assignment with data:', {
          ...this.editAssignmentData,
          hasNewFile: !!this.editSelectedFile,
          userRole: this.userRole,
          assignmentId: this.editingAssignment.id
        });
        
        const response = await axios.patch(`http://127.0.0.1:8000/api/assignments/${this.editingAssignment.id}/`, formData, {
          headers: { 
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'multipart/form-data'
          }
        });
        
        console.log('Assignment updated successfully:', response.data);
        this.closeEditModal();
        this.loadAssignments();
        alert('Assignment updated successfully!');
      } catch (error) {
        console.error('Error updating assignment:', error);
        if (error.response?.data) {
          console.error('Error details:', error.response.data);
          if (error.response.data.detail) {
            this.editErrorMessage = error.response.data.detail;
          } else if (error.response.data.error) {
            this.editErrorMessage = error.response.data.error;
          } else {
            this.editErrorMessage = `Failed to update assignment: ${JSON.stringify(error.response.data)}`;
          }
        } else {
          this.editErrorMessage = 'Failed to update assignment. Please try again.';
        }
      } finally {
        this.isUpdating = false;
      }
    },
  }
};
</script>
