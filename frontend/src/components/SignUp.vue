<template>
    <section class="p-8">
        <div class="max-w-md mx-auto bg-white p-10 rounded-lg ">
            <h2 class="text-2xl font-bold text-center mb-6 ">Sign Up</h2>
            <form class="space-y-4">
                <div>
                    <label for="username" class="block text-sm font-medium text-gray-700 mb-1">Username</label>
                    <input 
                        type="text" 
                        id="username" 
                        name="username" 
                        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-700 focus:border-indigo-700"
                    >
                </div>
                <div>
                    <label for="email" class="block text-sm font-medium text-gray-700 mb-1">Email</label>
                    <input 
                        type="email" 
                        id="email" 
                        name="email" 
                        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                    >
                </div>
                <div>
                    <label for="password" class="block text-sm font-medium text-gray-700 mb-1">Password</label>
                    <input 
                        type="password" 
                        id="password" 
                        name="password" 
                        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                    >
                </div>
                <button 
                    type="submit"
                    class="w-full bg-indigo-600 text-white py-3 px-6 rounded-md font-semibold hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-colors duration-200">
                    {{ btn1 }}
                </button>
            </form>
        </div>
    </section>
</template>

<script>

export default {
    name: 'SignUp',
    data(){
        return{
            btn1: 'Sign Up',
        }
    }
}
</script>   