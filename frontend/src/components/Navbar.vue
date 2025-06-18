<template>
    <div class="w-full">
        <nav class="w-full bg-yellow-500 py-4 shadow-md">
            <ul class="list-none m-0 p-0 flex flex-col md:flex-row justify-end items-center gap-3 md:gap-12 pr-8">
                <template v-if="!isLoggedIn">
                    <li class="m-0 py-2 px-4 rounded hover:bg-sky-700 hover:bg-opacity-10 font-medium cursor-pointer ">
                        <router-link to="/login" class="text-white no-underline block w-full h-full">
                            {{ btn2 }}
                        </router-link>
                    </li>
                </template>
                
                <li v-if="isLoggedIn" class="relative">
                    <div @click="toggleDropdown" 
                         class="flex items-center gap-2 py-2 px-4 rounded hover:bg-sky-700 hover:bg-opacity-10 font-medium cursor-pointer text-white">
                        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd"/>
                        </svg>
                        <span>{{ userName || 'User' }}</span>
                        <svg class="w-4 h-4 transition-transform duration-200" :class="{'rotate-180': showDropdown}" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"/>
                        </svg>
                    </div>

                    <div v-if="showDropdown" 
                         class="absolute right-0 top-full mt-1 w-48 bg-white rounded-md shadow-lg border border-gray-200 z-50">
                        <div class="py-1">
                            <router-link to="/dashboard" 
                                       @click="closeDropdown"
                                       class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 no-underline">
                                       Dashboard
                            </router-link>
                            <hr class="border-gray-200">
                            <button @click="logout" 
                                  class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 focus:outline-none">
                                Logout
                            </button>
                        </div>
                    </div>
                </li>
            </ul>
        </nav>
    </div>
</template>

<script>
export default {
    name: 'Navbar',
    props: {
        btn2: {
            default: 'Login'
        }
    },
    data() {
        return {
            showDropdown: false,
            isLoggedIn: false,
            userName: ''
        }
    },
    mounted() {
        this.checkAuthStatus();
        // Listen for storage changes to update auth status
        window.addEventListener('storage', this.checkAuthStatus);
        // Also check on route changes
        this.$router.afterEach(() => {
            this.checkAuthStatus();
        });
    },
    beforeUnmount() {
        window.removeEventListener('storage', this.checkAuthStatus);
        document.removeEventListener('click', this.handleClickOutside);
    },
    methods: {
        checkAuthStatus() {
            const token = localStorage.getItem('token') || sessionStorage.getItem('token');
            const user = localStorage.getItem('user') || sessionStorage.getItem('user');
            
            this.isLoggedIn = !!token;
            
            if (user) {
                try {
                    const userData = JSON.parse(user);
                    this.userName = userData.username || userData.first_name || 'User';
                } catch (e) {
                    this.userName = 'User';
                }
            }
        },
        toggleDropdown() {
            this.showDropdown = !this.showDropdown;
            
            if (this.showDropdown) {
                // Add click outside listener when dropdown is open
                this.$nextTick(() => {
                    document.addEventListener('click', this.handleClickOutside);
                });
            } else {
                document.removeEventListener('click', this.handleClickOutside);
            }
        },
        closeDropdown() {
            this.showDropdown = false;
            document.removeEventListener('click', this.handleClickOutside);
        },
        handleClickOutside(event) {
            const dropdown = this.$el.querySelector('.relative');
            if (dropdown && !dropdown.contains(event.target)) {
                this.closeDropdown();
            }
        },
        async logout() {
            try {
                localStorage.removeItem('token');
                localStorage.removeItem('refresh_token');
                localStorage.removeItem('user');
                localStorage.removeItem('userRole');
                sessionStorage.removeItem('token');
                sessionStorage.removeItem('refresh_token');
                sessionStorage.removeItem('user');
                sessionStorage.removeItem('userRole');

                this.isLoggedIn = false;
                this.userName = '';
                this.closeDropdown();

                this.$router.push('/');
            } catch (error) {
                console.error('Logout error:', error);
            }
        }
    }
};
</script>