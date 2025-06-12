<template>
    <section>
        <div>
            <h2 >Sign Up</h2>
            <form>
                <div>
                    <label for="username">Username</label>
                    <input type="text" id="username" name="username" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500">
                </div>
                <div>
                    <label for="email">Email</label>
                    <input type="email" id="email" name="email" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500">
                </div>
                <div>
                    <label for="password">Password</label>
                    <input type="password" id="password" name="password" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500">
                </div>
                <button type="submit">
                    Sign Up
                </button>
            </form>
        </div>
    </section>
</template>

<script>
export default {
    name: 'SignUp',
}
</script>

<style scoped>
section {
    padding: 2rem;
    background-color: #f9fafb;
}
form {
    max-width: 400px;
    margin: auto;
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
form div {
    margin-bottom: 1rem;
}
input {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #d1d5db;
    border-radius: 0.375rem;
}
button {
    background-color: #4f46e5;
    color: white;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 0.375rem;
    cursor: pointer;
    font-weight: 600;
}
button:hover {
    background-color: #4338ca;
}
button:focus {
    outline: none;
    box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.5);
}

</style>