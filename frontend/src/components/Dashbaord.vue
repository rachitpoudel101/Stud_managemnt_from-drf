<template>
  <div class="h-screen flex flex-col bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b border-gray-200 flex-shrink-0">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center">
            <ShieldIcon class="h-8 w-8 text-blue-600 mr-3" />
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
              <CheckCircleIcon class="h-5 w-5 text-green-400" />
              <div class="ml-3">
                <p class="text-sm font-medium text-green-800">{{ successMessage }}</p>
              </div>
            </div>
          </div>
        </div>

        <div v-if="errorMessage" class="mb-6">
          <div class="rounded-md bg-red-50 p-4">
            <div class="flex">
              <XCircleIcon class="h-5 w-5 text-red-400" />
              <div class="ml-3">
                <p class="text-sm font-medium text-red-800">{{ errorMessage }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Admin Dashboard -->
        <div v-if="userRole === 'admin'">
          <!-- Stats Grid -->
          <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8">
            <div class="bg-white overflow-hidden shadow rounded-lg">
              <div class="p-5">
                <div class="flex items-center">
                  <div class="flex-shrink-0">
                    <UsersIcon class="h-6 w-6 text-gray-400" />
                  </div>
                  <div class="ml-5 w-0 flex-1">
                    <dl>
                      <dt class="text-sm font-medium text-gray-500 truncate">Total Users</dt>
                      <dd class="text-lg font-medium text-gray-900">
                        {{ userCount !== null ? userCount : 'Loading...' }}
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>

            <div class="bg-white overflow-hidden shadow rounded-lg">
              <div class="p-5">
                <div class="flex items-center">
                  <div class="flex-shrink-0">
                    <GraduationCapIcon class="h-6 w-6 text-gray-400" />
                  </div>
                  <div class="ml-5 w-0 flex-1">
                    <dl>
                      <dt class="text-sm font-medium text-gray-500 truncate">Total Students</dt>
                      <dd class="text-lg font-medium text-gray-900">
                        {{ studentCount !== null ? studentCount : 'Loading...' }}
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>

            <div class="bg-white overflow-hidden shadow rounded-lg">
              <div class="p-5">
                <div class="flex items-center">
                  <div class="flex-shrink-0">
                    <UserIcon class="h-6 w-6 text-gray-400" />
                  </div>
                  <div class="ml-5 w-0 flex-1">
                    <dl>
                      <dt class="text-sm font-medium text-gray-500 truncate">Total Teachers</dt>
                      <dd class="text-lg font-medium text-gray-900">
                        {{ teacherCount !== null ? teacherCount : 'Loading...' }}
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>

            <div class="bg-white overflow-hidden shadow rounded-lg">
              <div class="p-5">
                <div class="flex items-center">
                  <div class="flex-shrink-0">
                    <BookOpenIcon class="h-6 w-6 text-gray-400" />
                  </div>
                  <div class="ml-5 w-0 flex-1">
                    <dl>
                      <dt class="text-sm font-medium text-gray-500 truncate">Total Subjects</dt>
                      <dd class="text-lg font-medium text-gray-900">
                        {{ subjectCount !== null ? subjectCount : 'Loading...' }}
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Quick Actions Grid -->
          <div class="grid grid-cols-1 gap-6 lg:grid-cols-2 mb-8">
            <!-- User Management -->
            <div class="bg-white shadow rounded-lg">
              <div class="px-6 py-4 border-b border-gray-200">
                <h3 class="text-lg leading-6 font-medium text-gray-900">User Management</h3>
                <p class="mt-1 text-sm text-gray-500">Manage students and teachers</p>
              </div>
              <div class="px-6 py-4 space-y-3">
                <button
                  @click="addStudents"
                  class="w-full flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                >
                  <UserPlusIcon class="h-4 w-4 mr-2" />
                  Add Student
                </button>
                <button
                  @click="addTeachers"
                  class="w-full flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  <UserPlusIcon class="h-4 w-4 mr-2" />
                  Add Teacher
                </button>
                <button
                  @click="manageStudents"
                  class="w-full flex items-center justify-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  <SettingsIcon class="h-4 w-4 mr-2" />
                  Manage Users & Subjects
                </button>
              </div>
            </div>

            <!-- Academic Management -->
            <div class="bg-white shadow rounded-lg">
              <div class="px-6 py-4 border-b border-gray-200">
                <h3 class="text-lg leading-6 font-medium text-gray-900">Academic Management</h3>
                <p class="mt-1 text-sm text-gray-500">Manage subjects and curriculum</p>
              </div>
              <div class="px-6 py-4 space-y-3">
                <button
                  @click="addSubject"
                  class="w-full flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
                >
                  <PlusIcon class="h-4 w-4 mr-2" />
                  Add Subject
                </button>
                <button
                  @click="viewReports"
                  class="w-full flex items-center justify-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  <BarChartIcon class="h-4 w-4 mr-2" />
                  View Reports
                </button>
                <button
                  @click="systemSettings"
                  class="w-full flex items-center justify-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  <CogIcon class="h-4 w-4 mr-2" />
                  System Settings
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Teacher Dashboard -->
        <div v-if="userRole === 'teacher'" class="space-y-6">
          <!-- Teacher's Assigned Subjects -->
          <div class="bg-white shadow rounded-lg">
            <div class="px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg leading-6 font-medium text-gray-900">Your Assigned Subjects</h3>
            </div>
            <div class="px-6 py-4">
              <div v-if="isLoadingSubjects" class="text-center text-gray-600">
                <p>Loading subjects...</p>
              </div>
              
              <div v-else-if="teacherSubjects.length === 0" class="bg-yellow-50 border border-yellow-200 rounded-lg p-4 text-center">
                <p class="text-yellow-700">You don't have any subjects assigned to you yet.</p>
              </div>
              
              <div v-else>
                <ul class="divide-y divide-gray-200">
                  <li v-for="subject in teacherSubjects" :key="subject.id" class="py-4 flex justify-between">
                    <span class="font-medium text-gray-800">{{ subject.name }}</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>

          <!-- Teacher Actions -->
          <div class="bg-white shadow rounded-lg">
            <div class="px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg leading-6 font-medium text-gray-900">Teacher Actions</h3>
            </div>
            <div class="px-6 py-4 space-y-3">
              <button
                @click="manageStudents"
                class="w-full flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                <SettingsIcon class="h-4 w-4 mr-2" />
                Manage Students & Subjects
              </button>
              <button
                @click="manageMarks"
                class="w-full flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
              >
                <PencilIcon class="h-4 w-4 mr-2" />
                Manage Student Marks
              </button>
            </div>
          </div>
        </div>
        
        <!-- Student Dashboard -->
        <div v-if="userRole === 'student'" class="space-y-6">
          <!-- Student Profile Info -->
          <div class="bg-white shadow rounded-lg">
            <div class="px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg leading-6 font-medium text-gray-900">Your Information</h3>
            </div>
            <div class="px-6 py-4">
              <div v-if="isLoadingStudentProfile" class="text-center text-gray-600">
                <p>Loading profile...</p>
              </div>
              
              <div v-else-if="!studentProfile" class="bg-yellow-50 border border-yellow-200 rounded-lg p-4 text-center">
                <p class="text-yellow-700">Could not load your profile information.</p>
              </div>
              
              <div v-else>
                <!-- Grade Information -->
                <div class="mb-4 pb-3 border-b border-gray-200">
                  <p class="font-medium">Your Grade: 
                    <span class="text-blue-600 font-bold">
                      {{ studentProfile.grade_display || `Grade ${studentProfile.grade}` }}
                    </span>
                  </p>
                </div>
                
                <!-- Assigned Subjects -->
                <div>
                  <p class="font-medium mb-3">Your Subjects:</p>
                  <ul v-if="studentSubjects.length > 0" class="divide-y divide-gray-200">
                    <li v-for="subject in studentSubjects" :key="subject.id" class="py-3 flex justify-between">
                      <span class="font-medium">{{ subject.name }}</span>
                      <span class="text-sm text-gray-600">
                        {{ subject.teacher_name ? `Teacher: ${subject.teacher_name}` : 'No teacher assigned' }}
                      </span>
                    </li>
                  </ul>
                  <p v-else class="text-center text-gray-600">No subjects assigned yet.</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Student Actions -->
          <div class="bg-white shadow rounded-lg">
            <div class="px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg leading-6 font-medium text-gray-900">Student Actions</h3>
            </div>
            <div class="px-6 py-4">
              <button
                @click="viewResults"
                class="w-full flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                <DocumentReportIcon class="h-4 w-4 mr-2" />
                View My Results
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>

import axios from "axios";

export default {
  name: "Dashboard",
  data() {
    return {
      successMessage: "",
      errorMessage: "",
      userRole: "",
      userCount: null,
      teacherCount: null,  // Add teacher count
      studentCount: null,  // Add student count
      subjectCount: null,  // Add subject count
      teacherSubjects: [],
      isLoadingSubjects: false,
      studentProfile: null,
      studentSubjects: [],
      isLoadingStudentProfile: false,
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
          return user.id;
        } catch (e) {
          console.error("Error parsing user data:", e);
        }
      }
      return null;
    },
  },
};
</script>