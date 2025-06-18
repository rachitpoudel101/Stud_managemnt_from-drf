<template>
  <div>
    <!-- Stats Grid -->
    <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8">
      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
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
              <span class="h-6 w-6 text-gray-400">👥</span>
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
            @click="$emit('add-students')"
            class="w-full flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
          >
            Add Student
          </button>
          <button
            @click="$emit('add-teachers')"
            class="w-full flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Add Teacher
          </button>
          <button
            @click="$emit('manage-students')"
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
            @click="$emit('add-subject')"
            class="w-full flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
          >
            Add Subject
          </button>
        </div>
      </div>
    </div>

    <!-- Assignment Overview  -->
    <div class="mt-8">
      <h2 class="text-xl font-bold mb-4">Assignment Overview</h2>
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <AssignmentList 
          :userRole="'admin'" 
          :teacherSubjects="subjects"
        />
        <SubmissionList :userRole="'admin'" />
      </div>
    </div>

    <!-- Notices Section for Admin -->
    <div class="mt-8">
      <h2 class="text-xl font-bold mb-4">Notice Board Management</h2>
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <slot name="create-notice"></slot>
        <slot name="notice-list"></slot>
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
              @click="$emit('filter-users', 'all')" 
              class="px-3 py-1 text-sm font-medium rounded-l-md" 
              :class="userFilter === 'all' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700'"
            >
              All
            </button>
            <button 
              @click="$emit('filter-users', 'teacher')" 
              class="px-3 py-1 text-sm font-medium" 
              :class="userFilter === 'teacher' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700'"
            >
              Teachers
            </button>
            <button 
              @click="$emit('filter-users', 'student')" 
              class="px-3 py-1 text-sm font-medium" 
              :class="userFilter === 'student' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700'"
            >
              Students
            </button>
            <button 
              @click="$emit('filter-users', 'deleted')" 
              class="px-3 py-1 text-sm font-medium rounded-r-md" 
              :class="userFilter === 'deleted' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700'"
            >
              Deleted
            </button>
          </div>
          <!-- Refresh button -->
          <button @click="$emit('load-users')" class="text-blue-600 hover:text-blue-800">
            Refresh
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
                  <button v-if="userFilter === 'deleted'" @click="$emit('restore-user', user)" class="text-green-600 hover:text-green-900 mr-3">
                    Restore
                  </button>
                  <template v-else>
                    <button @click="$emit('edit-user', user)" class="text-blue-600 hover:text-blue-900 mr-3">
                      Edit
                    </button>
                    <button @click="$emit('delete-user', user)" class="text-red-600 hover:text-red-900">
                      Delete
                    </button>
                  </template>
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
        <button @click="$emit('load-subjects')" class="text-blue-600 hover:text-blue-800">
           Refresh
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
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium flex justify-end space-x-2">
                  <button @click="$emit('edit-subject', subject)" class="text-blue-600 hover:text-blue-900 mr-2">
                    Edit
                  </button>
                  <button @click="$emit('delete-subject', subject)" class="text-red-600 hover:text-red-900">
                    Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
    <!-- All Student Results Section -->
    <div class="bg-white shadow rounded-lg mb-6">
      <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          Student Results
        </h3>
      </div>
      <div class="p-6">
        <p class="mb-4 text-gray-600">View academic performance of all students across subjects.</p>
        <button 
          @click="$emit('view-all-results')" 
          class="w-full bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
        >
          View All Student Results
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import AssignmentList from './AssignmentList.vue';
import SubmissionList from './SubmissionList.vue';

export default {
  name: 'AdminDashboard',
  components: {
    AssignmentList,
    SubmissionList
  },
  props: {
    userCount: Number,
    teacherCount: Number,
    studentCount: Number,
    subjectCount: Number,
    filteredUsers: Array,
    userFilter: String,
    isLoadingUsers: Boolean,
    subjects: Array,
    isLoadingSubjects: Boolean
  }
}
</script>
