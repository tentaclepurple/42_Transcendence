<template>
  <div class="not-found">
    <div class="not-found-content">
      <h1>404</h1>
      <p>Oops! Parece que esta página no existe.</p>
      <button class="home-button" @click="redirectToHome">Volver a la página de inicio</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFound',
  methods: {
    redirectToHome() {
      this.$router.replace({ name: 'home' });
    }
  }
}
</script>

<style scoped>
.not-found {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f4f4f4;
  text-align: center;
}

.not-found-content {
  max-width: 600px;
}

.not-found h1 {
  font-size: 8rem;
  color: #ff6b6b;
  margin-bottom: 0.5rem;
}

.not-found p {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 2rem;
}

.home-button {
  background-color: #42b983;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 1rem;
  cursor: pointer;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.home-button:hover {
  background-color: #358a6d;
}
</style>
