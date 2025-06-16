<template>
  <div class="h-screen flex flex-col bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b border-gray-200 flex-shrink-0">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center">
            <!-- Replace ShieldIcon with a simple span or text -->
            <span class="h-8 w-8 text-blue-600 mr-3 font-bold">🛡️</span>
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
              <!-- Replace CheckCircleIcon -->
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
              <!-- Replace XCircleIcon -->
              <span class="h-5 w-5 text-red-400">✕</span>
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
                    <!-- Replace UsersIcon -->
                    <span class="h-6 w-6 text-gray-400">👥</span>
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
                    <!-- Replace UsersIcon -->
                    <span class="h-6 w-6 text-gray-400">👥</span>
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
                    <!-- Replace UsersIcon -->
                    <span class="h-6 w-6 text-gray-400">👥</span>
                  </div>
                  <div class="ml-5 w-0 flex-1">
                    <dl>
                      <dt class="text-sm font-medium text-gray-500 truncate">Total 
                      </dt>
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
                    <!-- Replace BookOpenIcon -->
                    <span class="h-6 w-6 text-gray-400">📚</span>
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
                  Add Student
                </button>
                <button
                  @click="addTeachers"
                  class="w-full flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  Add Teacher
                </button>
                <button
                  @click="manageStudents"
                  class="w-full flex items-center justify-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
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
                  Add Subject
                </button>
                <button
                  @click="viewReports"
                  class="w-full flex items-center justify-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  View Reports
                </button>
                <button
                  @click="systemSettings"
                  class="w-full flex items-center justify-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  System Settings
                </button>
              </div>
            </div>
          </div>

          <!-- Admin Management Tables -->
          <h2 class="text-xl font-bold mb-4">User & Subject Management</h2>
          
          <!-- User Management Table -->
          <div class="bg-white shadow rounded-lg mb-6">
            <div class="px-4 py-5 border-b border-gray-200 flex justify-between items-center">
              <h3 class="text-lg leading-6 font-medium text-gray-900">
                Users
              </h3>
              <div class="flex items-center space-x-2">
                <!-- Filter buttons -->
                <div class="flex rounded-md shadow-sm bg-gray-100 mr-3" role="group">
                  <button 
                    @click="filterUsers('all')" 
                    class="px-3 py-1 text-sm font-medium rounded-l-md" 
                    :class="userFilter === 'all' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700'"
                  >
                    All
                  </button>
                  <button 
                    @click="filterUsers('teacher')" 
                    class="px-3 py-1 text-sm font-medium" 
                    :class="userFilter === 'teacher' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700'"
                  >
                    Teachers
                  </button>
                  <button 
                    @click="filterUsers('student')" 
                    class="px-3 py-1 text-sm font-medium rounded-r-md" 
                    :class="userFilter === 'student' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700'"
                  >
                    Students
                  </button>
                </div>
                <!-- Refresh button -->
                <button @click="loadAllUsers" class="text-blue-600 hover:text-blue-800">
                  🔄 Refresh
                </button>
              </div>
            </div>
            <div class="p-4">
              <div v-if="isLoadingUsers" class="text-center py-4">
                <p>Loading users...</p>
              </div>
              <div v-else-if="filteredUsers.length === 0" class="text-center py-4">
                <p>No users found. Try changing the filter.</p>
              </div>
              <div v-else class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200">
                  <thead class="bg-gray-50">
                    <tr>
                      <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Name
                      </th>
                      <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Username
                      </th>
                      <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Email
                      </th>
                      <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Role
                      </th>
                      <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Actions
                      </th>
                    </tr>
                  </thead>
                  <tbody class="bg-white divide-y divide-gray-200">
                    <tr v-for="user in filteredUsers" :key="user.id">
                      <td class="px-6 py-4 whitespace-nowrap">
                        <div class="text-sm font-medium text-gray-900">{{ user.first_name }} {{ user.last_name }}</div>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <div class="text-sm text-gray-500">{{ user.username }}</div>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <div class="text-sm text-gray-500">{{ user.email }}</div>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full" 
                              :class="user.role === 'teacher' ? 'bg-blue-100 text-blue-800' : 'bg-green-100 text-green-800'">
                          {{ user.role.charAt(0).toUpperCase() + user.role.slice(1) }}
                        </span>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                        <button @click="showEditUser(user)" class="text-blue-600 hover:text-blue-900 mr-3">
                          Edit
                        </button>
                        <button @click="confirmDeleteUser(user)" class="text-red-600 hover:text-red-900">
                          Delete
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
          
          <!-- Subject Management Table -->
          <div class="bg-white shadow rounded-lg mb-6">
            <div class="px-4 py-5 border-b border-gray-200 flex justify-between items-center">
              <h3 class="text-lg leading-6 font-medium text-gray-900">
                Subjects
              </h3>
              <button @click="loadSubjects" class="text-blue-600 hover:text-blue-800">
                🔄 Refresh
              </button>
            </div>
            <div class="p-4">
              <div v-if="isLoadingSubjects" class="text-center py-4">
                <p>Loading subjects...</p>
              </div>
              <div v-else-if="subjects.length === 0" class="text-center py-4">
                <p>No subjects found.</p>
              </div>
              <div v-else class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200">
                  <thead class="bg-gray-50">
                    <tr>
                      <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Subject Name
                      </th>
                      <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Assigned Teacher
                      </th>
                      <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Actions
                      </th>
                    </tr>
                  </thead>
                  <tbody class="bg-white divide-y divide-gray-200">
                    <tr v-for="subject in subjects" :key="subject.id">
                      <td class="px-6 py-4 whitespace-nowrap">
                        <div class="text-sm font-medium text-gray-900">{{ subject.name }}</div>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <div class="text-sm text-gray-500">{{ subject.teacher_name || 'No teacher assigned' }}</div>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                        <button @click="showEditSubject(subject)" class="text-blue-600 hover:text-blue-900 mr-3">
                          Edit
                        </button>
                        <button @click="confirmDeleteSubject(subject)" class="text-red-600 hover:text-red-900">
                          Delete
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
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
                Manage Students & Subjects
              </button>
              <button
                @click="manageMarks"
                class="w-full flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
              >
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
                View My Results
              </button>
            </div>
          </div>
        </div>
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
      isLoadingSubjects: false,
      
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
      isDeleting: false
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
    
    filterUsers(filter) {
      this.userFilter = filter;
      
      if (filter === 'all') {
        this.filteredUsers = this.users;
      } else {
        this.filteredUsers = this.users.filter(user => user.role === filter);
      }
    },
    
    // Subject management methods
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
        
        this.successMessage = `Subject "${this.subjectToDelete.name}" deleted successfully!`;
        this.closeDeleteSubjectModal();
      } catch (error) {
        console.error("Error deleting subject:", error);
        this.errorMessage = error.response?.data?.error || 'Failed to delete subject.';
      } finally {
        this.isDeleting = false;
      }
    },
  },
};
</script>