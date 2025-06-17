<template>
  <div class="space-y-6">
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
          @click="$emit('manage-students')"
          class="w-full flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          Manage Students & Subjects
        </button>
        <button
          @click="$emit('manage-marks')"
          class="w-full flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
        >
          Manage Student Marks
        </button>
      </div>
    </div>
    
    <!-- Assignment Management Section -->
    <div class="mt-8">
      <h2 class="text-xl font-bold mb-4">Assignment Management</h2>
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <AssignmentList 
          :userRole="'teacher'" 
          :teacherSubjects="teacherSubjects"
          @submit-assignment="handleSubmitAssignment"
          @edit-assignment="handleEditAssignment"
        />
        <SubmissionList :userRole="'teacher'" />
      </div>
    </div>
    
    <!-- Notices Section for Teacher -->
    <div class="mt-8">
      <h2 class="text-xl font-bold mb-4">Notice Board Management</h2>
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <slot name="create-notice"></slot>
        <slot name="notice-list"></slot>
      </div>
    </div>
  </div>
</template>

<script>
import AssignmentList from './AssignmentList.vue';
import SubmissionList from './SubmissionList.vue';

export default {
  name: 'TeacherDashboard',
  components: {
    AssignmentList,
    SubmissionList
  },
  props: {
    teacherSubjects: {
      type: Array,
      default: () => []
    },
    isLoadingSubjects: Boolean
  },
  methods: {
    handleSubmitAssignment(assignment) {
      // This shouldn't happen for teachers, but handle gracefully
      console.log('Teacher cannot submit assignments');
    },
    
    handleEditAssignment(assignment) {
      // Implement edit functionality
      console.log('Edit assignment:', assignment);
    }
  }
}
</script>
