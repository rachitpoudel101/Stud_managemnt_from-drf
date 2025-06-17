<template>
  <div class="space-y-6">
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
          @click="$emit('view-results')"
          class="w-full flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          View My Results
        </button>
      </div>
    </div>
    
    <!-- Assignment Section -->
    <div class="mt-8">
      <h2 class="text-xl font-bold mb-4">Assignments</h2>
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <AssignmentList 
          :userRole="'student'" 
          @submit-assignment="handleSubmitAssignment"
        />
        <SubmissionList 
          :userRole="'student'" 
          ref="submissionList"
        />
      </div>
    </div>
    
    <!-- Notices Section for Student - View Only -->
    <div class="mt-8">
      <h2 class="text-xl font-bold mb-4">Notice Board</h2>
      <slot name="notice-list"></slot>
    </div>
    
    <!-- Submit Assignment Modal -->
    <SubmitAssignment 
      v-if="showSubmitModal && selectedAssignment"
      :assignment="selectedAssignment"
      @close="closeSubmitModal"
      @submitted="handleAssignmentSubmitted"
    />
  </div>
</template>

<script>
import AssignmentList from './AssignmentList.vue';
import SubmissionList from './SubmissionList.vue';
import SubmitAssignment from './SubmitAssignment.vue';

export default {
  name: 'StudentDashboard',
  components: {
    AssignmentList,
    SubmissionList,
    SubmitAssignment
  },
  props: {
    studentProfile: Object,
    studentSubjects: {
      type: Array,
      default: () => []
    },
    isLoadingStudentProfile: Boolean
  },
  data() {
    return {
      showSubmitModal: false,
      selectedAssignment: null
    };
  },
  methods: {
    handleSubmitAssignment(assignment) {
      this.selectedAssignment = assignment;
      this.showSubmitModal = true;
    },
    
    closeSubmitModal() {
      this.showSubmitModal = false;
      this.selectedAssignment = null;
    },
    
    handleAssignmentSubmitted() {
      // Refresh the submission list
      this.$refs.submissionList?.loadSubmissions();
    }
  }
}
</script>
