<template>
  <div class="bg-white shadow rounded-lg">
    <div class="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
      <h3 class="text-lg leading-6 font-medium text-gray-900">Notices</h3>
      <button 
        @click="loadNotices" 
        class="text-sm text-blue-600 hover:text-blue-800"
      >
        Refresh
      </button>
    </div>
    <div class="px-6 py-4">
      <div v-if="isLoading" class="text-center py-4">
        <p class="text-gray-500">Loading notices...</p>
      </div>
      
      <div v-else-if="notices.length === 0" class="text-center py-4">
        <p class="text-gray-500">No notices available.</p>
      </div>
      
      <div v-else class="space-y-4">
        <div v-for="notice in notices" :key="notice.id" class="border border-gray-200 rounded-md p-4">
          <div class="flex justify-between items-start">
            <h4 class="text-lg font-medium text-gray-900">{{ notice.title }}</h4>
            <div v-if="canEditNotice(notice)" class="flex space-x-2">
              <button 
                @click="editNotice(notice)" 
                class="text-blue-600 hover:text-blue-800"
              >
                Edit
              </button>
              <button 
                @click="deleteNotice(notice.id)" 
                class="text-red-600 hover:text-red-800"
              >
                Delete
              </button>
            </div>
          </div>
          
          <div class="mt-2 text-sm text-gray-700 whitespace-pre-wrap">{{ notice.content }}</div>
          
          <div class="mt-3 text-xs text-gray-500 flex justify-between">
            <span>
              For: 
              <span v-if="notice.audience === 'student'" class="bg-green-100 text-green-800 px-2 py-0.5 rounded">Students</span>
              <span v-else-if="notice.audience === 'teacher'" class="bg-blue-100 text-blue-800 px-2 py-0.5 rounded">Teachers</span>
              <span v-else class="bg-purple-100 text-purple-800 px-2 py-0.5 rounded">All</span>
            </span>
            <span>Posted by: {{ notice.created_by_name || 'Unknown' }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'NoticeList',
  props: {
    userRole: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      notices: [],
      isLoading: false,
      userId: null
    };
  },
  mounted() {
    this.getUserId();
    this.loadNotices();
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
    
    async loadNotices() {
      this.isLoading = true;
      
      try {
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:8000/api/notices/', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        
        this.notices = response.data;
        console.log('Loaded notices:', this.notices); // Debug log
      } catch (error) {
        console.error('Error loading notices:', error);
      } finally {
        this.isLoading = false;
      }
    },
    
    canEditNotice(notice) {
      // Admin can edit any notice
      if (this.userRole === 'admin') {
        return true;
      }
      
      // Teachers can edit notices they created - fix the comparison
      if (this.userRole === 'teacher') {
        // Convert both to numbers/strings for safe comparison
        return String(notice.created_by) === String(this.userId);
      }
      
      // Students can't edit any notices
      return false;
    },
    
    async deleteNotice(noticeId) {
      if (!confirm('Are you sure you want to delete this notice?')) return;
      
      try {
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        await axios.delete(`http://127.0.0.1:8000/api/notices/${noticeId}/`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        
        this.notices = this.notices.filter(notice => notice.id !== noticeId);
      } catch (error) {
        console.error('Error deleting notice:', error);
        alert('Failed to delete notice. Please try again.');
      }
    },
    
    editNotice(notice) {
      // Emit event to parent component to handle editing
      this.$emit('edit-notice', notice);
    }
  }
};
</script>
