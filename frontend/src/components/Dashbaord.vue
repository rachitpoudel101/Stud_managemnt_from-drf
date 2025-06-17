<template>
  <div class="h-screen flex flex-col bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b border-gray-200 flex-shrink-0">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center">
            <span class="h-8 w-8 text-blue-600 mr-3 font-bold">🛡</span>
            <h1 class="text-xl font-semibold text-gray-900">{{ userRole.charAt(0).toUpperCase() + userRole.slice(1) }} Dashboard</h1>
          </div>
          <div class="flex items-center space-x-4">
            <div class="text-sm text-gray-500">Welcome, {{ getUserName() }}</div>
            <button
              @click="logout"
              class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500">
              Logout
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex-1 overflow-y-auto">
      <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <!-- Success/Error Messages -->
        <div v-if="successMessage" class="mb-6">
          <div class="rounded-md bg-green-50 p-4">
            <div class="flex">
              <span class="h-5 w-5 text-green-400">✓</span>
              <div class="ml-3">
                <p class="text-sm font-medium text-green-800">{{ successMessage }}</p>
              </div>
            </div>
          </div>
        </div>

        <div v-if="errorMessage" class="mb-6">
          <div class="rounded-md bg-red-50 p-4">
            <div class="flex">
              <span class="h-5 w-5 text-red-400">✕</span>
              <div class="ml-3">
                <p class="text-sm font-medium text-red-800">{{ errorMessage }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Admin Dashboard -->
        <AdminDashboard
          v-if="userRole === 'admin'"
          :user-count="userCount"
          :teacher-count="teacherCount"
          :student-count="studentCount"
          :subject-count="subjectCount"
          :filtered-users="filteredUsers"
          :user-filter="userFilter"
          :is-loading-users="isLoadingUsers"
          :subjects="subjects"
          :is-loading-subjects="isLoadingSubjects"
          @add-students="addStudents"
          @add-teachers="addTeachers"
          @manage-students="manageStudents"
          @add-subject="addSubject"
          @filter-users="filterUsers"
          @load-users="loadAllUsers"
          @edit-user="showEditUser"
          @delete-user="confirmDeleteUser"
          @restore-user="restoreUser"
          @load-subjects="loadSubjects"
          @edit-subject="showEditSubject"
          @delete-subject="confirmDeleteSubject"
          @view-all-results="viewAllStudentResults"
        >
          <template v-slot:create-notice>
            <CreateNotice 
              :userRole="userRole" 
              @notice-created="loadNotices"
            />
          </template>
          <template v-slot:notice-list>
            <NoticeList 
              :userRole="userRole" 
              ref="noticeList"
              @edit-notice="prepareEditNotice"
            />
          </template>
        </AdminDashboard>
        
        <!-- Teacher Dashboard -->
        <TeacherDashboard
          v-if="userRole === 'teacher'"
          :teacher-subjects="teacherSubjects"
          :is-loading-subjects="isLoadingSubjects"
          @manage-students="manageStudents"
          @manage-marks="manageMarks"
        >
          <template v-slot:create-notice>
            <CreateNotice 
              :userRole="userRole" 
              @notice-created="loadNotices"
            />
          </template>
          <template v-slot:notice-list>
            <NoticeList 
              :userRole="userRole" 
              ref="noticeList"
              @edit-notice="prepareEditNotice"
            />
          </template>
        </TeacherDashboard>
        
        <!-- Student Dashboard -->
        <StudentDashboard
          v-if="userRole === 'student'"
          :student-profile="studentProfile"
          :student-subjects="studentSubjects"
          :is-loading-student-profile="isLoadingStudentProfile"
          @view-results="viewResults"
        >
          <template v-slot:notice-list>
            <NoticeList 
              :userRole="userRole" 
              ref="noticeList"
            />
          </template>
        </StudentDashboard>
      </div>
    </main>
    
    <!-- Edit User Modal -->
    <div v-if="showEditUserModal" class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md mx-4">
        <h3 class="text-lg font-medium text-gray-900 mb-4">Edit Username</h3>
        <div class="mb-4">
          <label for="username" class="block text-sm font-medium text-gray-700 mb-1">Username</label>
          <input 
            type="text" 
            id="username" 
            v-model="editUserUsername" 
            class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          />
        </div>
        <div class="flex justify-end space-x-3">
          <button 
            @click="closeEditUserModal" 
            class="inline-flex justify-center px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 border border-gray-300 rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Cancel
          </button>
          <button 
            @click="updateUser" 
            :disabled="isUpdating"
            class="inline-flex justify-center px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
          >
            {{ isUpdating ? 'Updating...' : 'Update' }}
          </button>
        </div>
      </div>
    </div>
    
    <!-- Delete User Modal -->
    <div v-if="showDeleteUserModal" class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md mx-4">
        <h3 class="text-lg font-medium text-gray-900 mb-4">Delete User</h3>
        <p class="text-gray-700 mb-4">
          Are you sure you want to delete {{ userToDelete?.first_name }} {{ userToDelete?.last_name }} ({{ userToDelete?.username }})?
          This action cannot be undone.
        </p>
        <div class="flex justify-end space-x-3">
          <button 
            @click="closeDeleteUserModal" 
            class="inline-flex justify-center px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 border border-gray-300 rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Cancel
          </button>
          <button 
            @click="deleteUser" 
            :disabled="isDeleting"
            class="inline-flex justify-center px-4 py-2 text-sm font-medium text-white bg-red-600 border border-transparent rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50"
          >
            {{ isDeleting ? 'Deleting...' : 'Delete' }}
          </button>
        </div>
      </div>
    </div>
    
    <!-- Edit Subject Modal -->
    <div v-if="showEditSubjectModal" class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md mx-4">
        <h3 class="text-lg font-medium text-gray-900 mb-4">Edit Subject</h3>
        <div class="mb-4">
          <label for="subject-name" class="block text-sm font-medium text-gray-700 mb-1">Subject Name</label>
          <input 
            type="text" 
            id="subject-name" 
            v-model="editSubjectName" 
            class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          />
        </div>
        <div class="flex justify-end space-x-3">
          <button 
            @click="closeEditSubjectModal" 
            class="inline-flex justify-center px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 border border-gray-300 rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Cancel
          </button>
          <button 
            @click="updateSubject" 
            :disabled="isUpdating"
            class="inline-flex justify-center px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
          >
            {{ isUpdating ? 'Updating...' : 'Update' }}
          </button>
        </div>
      </div>
    </div>
    
    <!-- Delete Subject Modal -->
    <div v-if="showDeleteSubjectModal" class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md mx-4">
        <h3 class="text-lg font-medium text-gray-900 mb-4">Delete Subject</h3>
        <p class="text-gray-700 mb-4">
          Are you sure you want to delete the subject "{{ subjectToDelete?.name }}"?
          This action cannot be undone.
        </p>
        <div class="flex justify-end space-x-3">
          <button 
            @click="closeDeleteSubjectModal" 
            class="inline-flex justify-center px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 border border-gray-300 rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Cancel
          </button>
          <button 
            @click="deleteSubject" 
            :disabled="isDeleting"
            class="inline-flex justify-center px-4 py-2 text-sm font-medium text-white bg-red-600 border border-transparent rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50"
          >
            {{ isDeleting ? 'Deleting...' : 'Delete' }}
          </button>
        </div>
      </div>
    </div>
    
    <!-- Edit Notice Modal -->
    <div v-if="showEditNoticeModal" class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md mx-4">
        <h3 class="text-lg font-medium text-gray-900 mb-4">Edit Notice</h3>
        <div class="space-y-4">
          <div>
            <label for="notice-title" class="block text-sm font-medium text-gray-700 mb-1">Title</label>
            <input 
              type="text" 
              id="notice-title" 
              v-model="editNoticeForm.title" 
              class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            />
          </div>
          <div>
            <label for="notice-content" class="block text-sm font-medium text-gray-700 mb-1">Content</label>
            <textarea 
              id="notice-content" 
              v-model="editNoticeForm.content" 
              rows="4"
              class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            ></textarea>
          </div>
          <div v-if="userRole === 'admin'">
            <label for="notice-audience" class="block text-sm font-medium text-gray-700 mb-1">Audience</label>
            <select 
              id="notice-audience" 
              v-model="editNoticeForm.audience"
              class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            >
              <option value="student">Students Only</option>
              <option value="teacher">Teachers Only</option>
              <option value="both">Both Students & Teachers</option>
            </select>
          </div>
          <div class="flex items-center">
            <input 
              type="checkbox" 
              id="notice-published" 
              v-model="editNoticeForm.published"
              class="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            <label for="notice-published" class="ml-2 block text-sm text-gray-900">Published</label>
          </div>
        </div>
        <div class="mt-6 flex justify-end space-x-3">
          <button 
            @click="closeEditNoticeModal" 
            class="inline-flex justify-center px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 border border-gray-300 rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Cancel
          </button>
          <button 
            @click="updateNotice" 
            :disabled="isUpdating"
            class="inline-flex justify-center px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
          >
            {{ isUpdating ? 'Updating...' : 'Update' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import CreateNotice from "./CreateNotice.vue";
import NoticeList from "./NoticeList.vue";
import AdminDashboard from "./AdminDashboard.vue";
import TeacherDashboard from "./TeacherDashboard.vue";
import StudentDashboard from "./StudentDashboard.vue";

export default {
  name: "Dashboard",
  components: {
    CreateNotice,
    NoticeList,
    AdminDashboard,
    TeacherDashboard,
    StudentDashboard
  },
  data() {
    return {
      successMessage: "",
      errorMessage: "",
      userRole: "",
      userCount: null,
      teacherCount: null,
      studentCount: null,
      subjectCount: null,
      teacherSubjects: [],
      isLoadingSubjects: false,
      studentProfile: null,
      studentSubjects: [],
      isLoadingStudentProfile: false,
      
      // Replace separate teachers and students arrays with a unified users array
      users: [],
      filteredUsers: [],
      userFilter: 'all', // 'all', 'teacher', 'student'
      isLoadingUsers: false,
      
      // Keep other properties
      subjects: [],
      
      // Edit user modal
      showEditUserModal: false,
      editingUser: null,
      editUserUsername: '',
      // Delete user modal
      showDeleteUserModal: false,
      userToDelete: null,
      // Edit subject modal
      showEditSubjectModal: false,
      editingSubject: null,
      editSubjectName: '',
      // Delete subject modal
      showDeleteSubjectModal: false,
      subjectToDelete: null,
      isUpdating: false,
      isDeleting: false,
      deletedUsers: [],
      
      // For notice management
      editingNotice: null,
      showEditNoticeModal: false,
      editNoticeForm: {
        title: '',
        content: '',
        audience: 'student',
        published: true
      }
    };
  },
  created() {
    // Get user role from storage first
    this.userRole =
      localStorage.getItem("userRole") || sessionStorage.getItem("userRole") || "user";
    
    // Then fetch all stats when component is created for admin
    if (this.userRole === "admin") {
      this.fetchUserCount();
      this.fetchTeacherCount();
      this.fetchStudentCount();
      this.fetchSubjectCount();
    }

    // Fetch teacher's subjects if the user is a teacher
    if (this.userRole === "teacher") {
      this.fetchTeacherSubjects();
    }

    // Fetch student profile if the user is a student
    if (this.userRole === "student") {
      this.fetchStudentProfile();
    }
    
    // If admin, load all users and subjects for management
    if (this.userRole === 'admin') {
      this.loadAllUsers(); // New unified method instead of separate teacher/student loads
      this.loadSubjects();
    }
  },
  methods: {
    // Add this new method to display user's name
    getUserName() {
      const userStr = localStorage.getItem("user") || sessionStorage.getItem("user");
      if (userStr) {
        try {
          const user = JSON.parse(userStr);
          return user.first_name || user.username;
        } catch (e) {
          console.error("Error parsing user data:", e);
        }
      }
      return this.userRole.charAt(0).toUpperCase() + this.userRole.slice(1);
    },
    async fetchTeacherSubjects() {
      this.isLoadingSubjects = true;

      try {
        const token = localStorage.getItem("token") || sessionStorage.getItem("token");
        const response = await axios.get("http://127.0.0.1:8000/api/subjects/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        // The API should already filter subjects for the current teacher
        this.teacherSubjects = response.data;
        console.log("Teacher subjects:", this.teacherSubjects);
      } catch (error) {
        console.error("Error fetching teacher subjects:", error);
        this.errorMessage = "Failed to load your subjects.";
      } finally {
        this.isLoadingSubjects = false;
      }
    },
    async logout() {
      try {
        // Clear all stored authentication data
        localStorage.removeItem("token");
        localStorage.removeItem("refresh_token");
        localStorage.removeItem("user");
        localStorage.removeItem("userRole");
        sessionStorage.removeItem("token");
        sessionStorage.removeItem("refresh_token");
        sessionStorage.removeItem("user");
        sessionStorage.removeItem("userRole");

        this.successMessage = "Successfully logged out!";
        this.errorMessage = "";

        // Navigate to login page with a slight delay to show success message
        setTimeout(() => {
          this.$router.push("/login");
        }, 10);
      } catch (error) {
        console.error("Logout error:", error);
        this.errorMessage = "An error occurred during logout. Please try again.";
        this.successMessage = "";
      }
    },
    async addTeachers() {
      try {
        console.log("Navigating to add teacher");
        this.$router.push("/admin/add-teacher");
      } catch (error) {
        console.error("Error navigating to add teachers:", error);
        this.errorMessage = "An error occurred while navigating to add teachers.";
      }
    },
    async addStudents() {
      try {
        console.log("Navigating to add student");
        this.$router.push("/admin/add-student");
      } catch (error) {
        console.error("Error navigating to add students:", error);
        this.errorMessage = "An error occurred while navigating to add students.";
      }
    },
    async addSubject() {
      try {
        console.log("Navigating to add subject");
        this.$router.push("/admin/add-subject");
      } catch (error) {
        console.error("Error navigating to add subject:", error);
        this.errorMessage = "An error occurred while navigating to add subject.";
      }
    },
    async fetchUserCount() {
      // Only fetch if user is admin
      if (this.userRole === "admin") {
        try {
          const token = localStorage.getItem("token") || sessionStorage.getItem("token");
          const response = await axios.get("http://127.0.0.1:8000/api/users/", {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          this.userCount = response.data.user_count || response.data.length || 0;
        } catch (error) {
          console.error("Error fetching user count:", error);
          this.errorMessage = "Failed to fetch user count.";
          this.userCount = "Error";
        }
      }
    },
    async fetchTeacherCount() {
      try {
        const token = localStorage.getItem("token") || sessionStorage.getItem("token");
        // Make sure we're properly filtering by role=teacher
        const response = await axios.get("http://127.0.0.1:8000/api/users/", {
          params: { role: 'teacher' },
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        
        // Ensure we're counting only teachers
        const teachers = Array.isArray(response.data) 
          ? response.data.filter(user => user.role === 'teacher')
          : [];
        
        this.teacherCount = teachers.length;
        console.log("Teacher count:", this.teacherCount);
      } catch (error) {
        console.error("Error fetching teacher count:", error);
        this.teacherCount = "Error";
      }
    },
    async fetchStudentCount() {
      try {
        const token = localStorage.getItem("token") || sessionStorage.getItem("token");
        // Make sure we're properly filtering by role=student
        const response = await axios.get("http://127.0.0.1:8000/api/users/", {
          params: { role: 'student' },
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        
        // Ensure we're counting only students
        const students = Array.isArray(response.data) 
          ? response.data.filter(user => user.role === 'student')
          : [];
        
        this.studentCount = students.length;
        console.log("Student count:", this.studentCount);
      } catch (error) {
        console.error("Error fetching student count:", error);
        this.studentCount = "Error";
      }
    },
    async fetchSubjectCount() {
      try {
        const token = localStorage.getItem("token") || sessionStorage.getItem("token");
        const response = await axios.get("http://127.0.0.1:8000/api/subjects/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.subjectCount = response.data.length || 0;
      } catch (error) {
        console.error("Error fetching subject count:", error);
        this.subjectCount = "Error";
      }
    },
    manageStudents() {
      this.$router.push("/manage-students");
    },
    manageMarks() {
      this.$router.push("/teacher/manage-marks");
    },
    viewResults() {
      this.$router.push("/student/view-results");
    },
    async fetchStudentProfile() {
      this.isLoadingStudentProfile = true;

      try {
        const token = localStorage.getItem("token") || sessionStorage.getItem("token");
        const userId = this.getUserId();

        if (!userId) {
          console.error("No user ID found");
          return;
        }

        // Get the student profile
        const profileResponse = await axios.get(
          `http://127.0.0.1:8000/api/users/${userId}/profile/`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );

        this.studentProfile = profileResponse.data;
        console.log("Student profile:", this.studentProfile);

        // Extract subjects from the profile
        if (this.studentProfile && this.studentProfile.subject_details) {
          this.studentSubjects = this.studentProfile.subject_details;
        } else if (this.studentProfile && this.studentProfile.subjects) {
          // Fetch full subject details if only IDs are provided
          await this.fetchStudentSubjects(this.studentProfile.subjects);
        }
      } catch (error) {
        console.error("Error fetching student profile:", error);
        this.errorMessage = "Failed to load your profile information.";
      } finally {
        this.isLoadingStudentProfile = false;
      }
    },
    async fetchStudentSubjects(subjectIds) {
      if (!subjectIds || !subjectIds.length) return;

      try {
        const token = localStorage.getItem("token") || sessionStorage.getItem("token");
        const response = await axios.get("http://127.0.0.1:8000/api/subjects/", {
          headers: { Authorization: `Bearer ${token}` },
        });

        // Filter only the subjects assigned to the student
        this.studentSubjects = response.data.filter((subject) =>
          subjectIds.includes(subject.id)
        );
      } catch (error) {
        console.error("Error fetching student subjects:", error);
      }
    },
    getUserId() {
      // Try to get user ID from stored user object
      const userStr = localStorage.getItem("user") || sessionStorage.getItem("user");
      if (userStr) {
        try {
          const user = JSON.parse(userStr);
          return user.id || null;
        } catch (e) {
          console.error("Error parsing user data:", e);
        }
      }
      return null;
    },
    
    // New methods for admin management of users and subjects
    viewReports() {
      console.log("View reports clicked - functionality to be implemented");
    },
    
    systemSettings() {
      console.log("System settings clicked - functionality to be implemented");
    },
    
    // Teacher management methods
    async loadAllUsers() {
      this.isLoadingUsers = true;
      this.errorMessage = '';
      
      try {
        const token = localStorage.getItem("token") || sessionStorage.getItem("token");
        const response = await axios.get("http://127.0.0.1:8000/api/users/", {
          headers: { Authorization: `Bearer ${token}` }
        });
        
        this.users = response.data;
        this.filterUsers(this.userFilter); // Apply current filter
      } catch (error) {
        console.error("Error loading users:", error);
        this.errorMessage = "Failed to load users.";
      } finally {
        this.isLoadingUsers = false;
      }
    },
    
    // Updated method to handle deleted users filter
    async filterUsers(filter) {
      this.userFilter = filter;
      
      if (filter === 'deleted') {
        await this.loadDeletedUsers();
        this.filteredUsers = this.deletedUsers;
      } else if (filter === 'all') {
        this.filteredUsers = this.users;
      } else {
        this.filteredUsers = this.users.filter(user => user.role === filter);
      }
    },
    
    // New method to load deleted users
    async loadDeletedUsers() {
      this.isLoadingUsers = true;
      this.errorMessage = '';
      
      try {
        const token = localStorage.getItem("token") || sessionStorage.getItem("token");
        const response = await axios.get("http://127.0.0.1:8000/api/users/deleted/", {
          headers: { Authorization: `Bearer ${token}` }
        });
        
        this.deletedUsers = response.data;
      } catch (error) {
        console.error("Error loading deleted users:", error);
        this.errorMessage = "Failed to load deleted users.";
        this.deletedUsers = [];
      } finally {
        this.isLoadingUsers = false;
      }
    },
    
    // New method to restore a user
    async restoreUser(user) {
      try {
        this.errorMessage = '';
        const token = localStorage.getItem("token") || sessionStorage.getItem("token");
        
        await axios.post(
          `http://127.0.0.1:8000/api/users/${user.id}/restore/`,
          {},
          { headers: { Authorization: `Bearer ${token}` } }
        );
        
        // Remove from deleted users list
        this.deletedUsers = this.deletedUsers.filter(u => u.id !== user.id);
        this.filteredUsers = this.deletedUsers;
        
        // Refresh active users
        await this.loadAllUsers();
        
        this.successMessage = `User ${user.username} has been restored.`;
      } catch (error) {
        console.error("Error restoring user:", error);
        this.errorMessage = error.response?.data?.error || "Failed to restore user.";
      }
    },
    
    // Edit user methods
    showEditUser(user) {
      this.editingUser = { ...user };
      this.editUserUsername = user.username;
      this.showEditUserModal = true;
    },
    
    closeEditUserModal() {
      this.showEditUserModal = false;
      this.editingUser = null;
      this.editUserUsername = '';
    },
    
    async updateUser() {
      if (!this.editingUser || !this.editUserUsername.trim()) {
        return;
      }
      
      this.isUpdating = true;
      this.errorMessage = '';
      
      try {
        const token = localStorage.getItem("token") || sessionStorage.getItem("token");
        await axios.patch(
          `http://127.0.0.1:8000/api/users/${this.editingUser.id}/change-username/`,
          { username: this.editUserUsername.trim() },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        
        // Update local data
        const userIndex = this.users.findIndex(u => u.id === this.editingUser.id);
        if (userIndex !== -1) {
          this.users[userIndex].username = this.editUserUsername.trim();
          this.filterUsers(this.userFilter); // Re-apply the current filter
        }
        
        this.successMessage = 'Username updated successfully!';
        this.closeEditUserModal();
      } catch (error) {
        console.error("Error updating username:", error);
        this.errorMessage = error.response?.data?.error || 'Failed to update username.';
      } finally {
        this.isUpdating = false;
      }
    },
    
    // Delete user methods
    confirmDeleteUser(user) {
      this.userToDelete = user;
      this.showDeleteUserModal = true;
    },
    
    closeDeleteUserModal() {
      this.showDeleteUserModal = false;
      this.userToDelete = null;
    },
    
    async deleteUser() {
      if (!this.userToDelete) {
        return;
      }
      
      this.isDeleting = true;
      this.errorMessage = '';
      
      try {
        const token = localStorage.getItem("token") || sessionStorage.getItem("token");
        await axios.delete(
          `http://127.0.0.1:8000/api/users/${this.userToDelete.id}/`,
          { headers: { Authorization: `Bearer ${token}` } }
        );
        
        // Update local data
        this.users = this.users.filter(u => u.id !== this.userToDelete.id);
        this.filterUsers(this.userFilter); // Re-apply the current filter
        
        // Update counts
        if (this.userToDelete.role === 'teacher') {
          this.teacherCount = Math.max(0, this.teacherCount - 1);
        } else if (this.userToDelete.role === 'student') {
          this.studentCount = Math.max(0, this.studentCount - 1);
        }
        this.userCount = Math.max(0, this.userCount - 1);
        
        this.successMessage = `User ${this.userToDelete.username} deleted successfully!`;
        this.closeDeleteUserModal();
      } catch (error) {
        console.error("Error deleting user:", error);
        this.errorMessage = error.response?.data?.error || 'Failed to delete user.';
      } finally {
        this.isDeleting = false;
      }
    },
    // Edit subject methods
    showEditSubject(subject) {
      this.editingSubject = { ...subject };
      this.editSubjectName = subject.name;
      this.showEditSubjectModal = true;
    },
    
    closeEditSubjectModal() {
      this.showEditSubjectModal = false;
      this.editingSubject = null;
      this.editSubjectName = '';
    },
    
    async updateSubject() {
      if (!this.editingSubject || !this.editSubjectName.trim()) {
        return;
      }
      
      this.isUpdating = true;
      this.errorMessage = '';
      
      try {
        const token = localStorage.getItem("token") || sessionStorage.getItem("token");
        await axios.patch(
          `http://127.0.0.1:8000/api/subjects/${this.editingSubject.id}/`,
          { name: this.editSubjectName.trim() },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        
        // Update local data
        const subjectIndex = this.subjects.findIndex(s => s.id === this.editingSubject.id);
        if (subjectIndex !== -1) {
          this.subjects[subjectIndex].name = this.editSubjectName.trim();
        }
        
        this.closeEditSubjectModal();
      } catch (error) {
        console.error("Error updating subject:", error);
        this.errorMessage = error.response?.data?.error || 'Failed to update subject.';
      } finally {
        this.isUpdating = false;
      }
    },
    
    // Delete subject methods
    confirmDeleteSubject(subject) {
      this.subjectToDelete = subject;
      this.showDeleteSubjectModal = true;
    },
    
    closeDeleteSubjectModal() {
      this.showDeleteSubjectModal = false;
      this.subjectToDelete = null;
    },
    
    async deleteSubject() {
      if (!this.subjectToDelete) {
        return;
      }
      
      this.isDeleting = true;
      this.errorMessage = '';
      
      try {
        const token = localStorage.getItem("token") || sessionStorage.getItem("token");
        await axios.delete(
          `http://127.0.0.1:8000/api/subjects/${this.subjectToDelete.id}/`,
          { headers: { Authorization: `Bearer ${token}` } }
        );
        
        // Update local data
        this.subjects = this.subjects.filter(s => s.id !== this.subjectToDelete.id);
        this.subjectCount = Math.max(0, this.subjectCount - 1);
        
        this.successMessage = `Subject "${this.subjectToDelete.name}" deleted successfully!`;
        this.closeDeleteSubjectModal();
      } catch (error) {
        console.error("Error deleting subject:", error);
        this.errorMessage = error.response?.data?.error || 'Failed to delete subject.';
      } finally {
        this.isDeleting = false;
      }
    },
    
    // Methods for viewing student results
    viewSubjectResults(subject) {
      // Navigate to view results page with subject filter
      this.$router.push({
        path: "/student/view-results",
        query: { 
          subjectId: subject.id,
          subjectName: subject.name,
          viewAsAdmin: this.userRole === 'admin' ? 'true' : 'false' // Add flag to identify admin view
        }
      });
    },
    
    viewAllStudentResults() {
      // Navigate to the view results page without filters
      this.$router.push({
        path: "/student/view-results",
        query: { viewAsAdmin: this.userRole === 'admin' ? 'true' : 'false' }
      });
    },
    
    // Method to load subjects - added missing method
    async loadSubjects() {
      this.isLoadingSubjects = true;
      this.errorMessage = '';
      try {
        const token = localStorage.getItem("token") || sessionStorage.getItem("token");
        const response = await axios.get("http://127.0.0.1:8000/api/subjects/", {
          headers: { Authorization: `Bearer ${token}` }
        });
        
        this.subjects = response.data;
      } catch (error) {
        console.error("Error loading subjects:", error);
        this.errorMessage = "Failed to load subjects.";
      } finally {
        this.isLoadingSubjects = false;
      }
    },
    
    // Notice related methods
    loadNotices() {
      if (this.$refs.noticeList) {
        this.$refs.noticeList.loadNotices();
      }
    },
    
    prepareEditNotice(notice) {
      this.editingNotice = notice;
      
      // Initialize the form with the notice data
      this.editNoticeForm = {
        title: notice.title,
        content: notice.content,
        audience: notice.audience,
        published: notice.published
      };
      
      // Show the modal
      this.showEditNoticeModal = true;
    },
    
    closeEditNoticeModal() {
      this.showEditNoticeModal = false;
      this.editingNotice = null;
      this.editNoticeForm = {
        title: '',
        content: '',
        audience: 'student',
        published: true
      };
    },
    
    async updateNotice() {
      if (!this.editingNotice) return;
      
      this.isUpdating = true;
      this.errorMessage = '';
      
      try {
        const token = localStorage.getItem('token') || sessionStorage.getItem('token');
        
        // Teachers can only update title and content, not audience
        const updateData = this.userRole === 'admin' 
          ? this.editNoticeForm 
          : {
              title: this.editNoticeForm.title,
              content: this.editNoticeForm.content,
              published: this.editNoticeForm.published
            };
        
        await axios.patch(
          `http://127.0.0.1:8000/api/notices/${this.editingNotice.id}/`,
          updateData,
          { headers: { Authorization: `Bearer ${token}` } }
        );
        
        this.successMessage = 'Notice updated successfully!';
        
        // Refresh notices list
        this.loadNotices();
        
        // Close the modal
        this.closeEditNoticeModal();
      } catch (error) {
        console.error('Error updating notice:', error);
        
        if (error.response?.status === 403) {
          this.errorMessage = 'You do not have permission to update this notice';
        } else {
          this.errorMessage = error.response?.data?.detail || 'Failed to update notice';
        }
      } finally {
        this.isUpdating = false;
      }
    }
  }
};
</script>