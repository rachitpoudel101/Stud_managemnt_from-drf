<template>
    <div>
        <nav>
            <ul>
                <li>
                    <router-link to="/sign-up" class="nav-link">Sign Up</router-link>
                </li>
                <li>
                    <router-link to="/login" class="nav-link">Login</router-link>
                </li>
            </ul>
        </nav>
    </div>
</template>

<script>
export default {
    name: 'Navbar',
};
</script>

<style scoped>
div {
  width: 100%;
  margin: 0;
  padding: 0;
}

nav {
  width: 100%;
  background-color: #0080ff;
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

ul {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 3rem;
  padding-right: 2rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  display: block;
  width: 100%;
  height: 100%;
}

li {
  margin: 0;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s ease;
  font-weight: 500;
  cursor: pointer;
}

li:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

@media (max-width: 768px) {
  ul {
    flex-direction: column;
    gap: 1rem;
  }
  
  nav {
    padding: 0.5rem 0;
  }
}
</style>