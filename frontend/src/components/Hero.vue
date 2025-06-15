<template>
  <section class="w-full min-h-[calc(100vh-67px)] bg-blue-500 flex items-center justify-center">
    <div class="text-center text-white max-w-4xl px-4">
      <h1 class="text-4xl md:text-6xl font-bold mb-4 leading-tight">
        {{ title }}
      </h1>
      <p class="text-lg md:text-xl mb-8 opacity-90 leading-relaxed">
        {{ subtitle }}
      </p>
      <div class="flex flex-col md:flex-row gap-4 justify-center items-center">
        <button class="w-48 md:w-auto px-8 py-4 bg-white text-indigo-500 border-none rounded-lg text-base font-semibold cursor-pointer transition-all duration-300 hover:bg-gray-50 hover:-translate-y-0.5">
          {{ buttonText1 }}
        </button>
        <button class="w-48 md:w-auto px-8 py-4 bg-transparent text-white border-2 border-white rounded-lg text-base font-semibold cursor-pointer transition-all duration-300 hover:bg-white hover:text-indigo-500 hover:-translate-y-0.5">
          {{ buttonText2 }}
        </button>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'Hero',
  data() {
    return {
      title: 'Student Management System',
      subtitle: 'Manage student records, grades, and academic information efficiently',
      buttonText1: 'Get Started',
      buttonText2: 'Learn More',
    };
  },
  mounted() {
    
  },
}
</script>
