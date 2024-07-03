<script setup>
import {onMounted, onUnmounted, reactive, watch} from 'vue';

import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';

import { loadBall } from '../assets/Game/Ball.js';
import { loadField } from '../assets/Game/Field.js';
import { loadLight } from "../assets/Game/Lightning.js";
import { loadRoad } from '../assets/Game/Road-Straight.js';
import { loadBuilding } from '../assets/Game/Buildings.js';
import { loadPlayer1, unloadPlayer1 } from '../assets/Game/Player-1.js';
import { loadPlayer2, unloadPlayer2 } from '../assets/Game/Player-2.js';
import { loadWS, unloadWS, loadInput, unloadInput } from "../assets/Game/WS.js";
import {useRouter} from "vue-router";
import {useCookies} from "vue3-cookies";
import process from "vue3-cookies/.eslintrc.js";

const props = defineProps({
  game_id: Number
});

const router = useRouter();

const navigateHome = () => {
  router.push({ name: 'home' });
};

const navigateStats = () => {
  router.push({ name: 'stats' });
};

let renderer, scene, camera, controls;
let animationFrameId;

let scores = reactive({ state: '', player1: 0, player2: 0, error: ''});

let modals = reactive({ errorModal: false, finishModal: false });

onMounted(() => {

  watch(() => scores.error, (newState) => {
    if (newState !== '' && newState !== 'Game is paused')
      modals.errorModal = true
  });

  watch(() => scores.state, (newState) => {
    if (newState === 'FINISHED')
      modals.finishModal = true
  });

  const { cookies } = useCookies();

  loadWS(import.meta.env.VITE_WSS_APP_BACKEND_URL +'/pong/' + props.game_id + '/?token='+ cookies.get('token_auth'), scores)

  scene = new THREE.Scene();

  camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 10000);
  camera.position.set(350, 50, 225);
  camera.lookAt(new THREE.Vector3(350, 0, 225));

  const gameDiv = document.getElementById('game');

  renderer = new THREE.WebGLRenderer({antialias: true, alpha: true});
  renderer.setSize(gameDiv.clientWidth, gameDiv.clientHeight);

  gameDiv.appendChild(renderer.domElement);

  controls = new OrbitControls(camera, renderer.domElement);
  controls.target.set(350, 0, 225);  // Set the target of the controls
  camera.position.x = 350;
  camera.position.y = 400;
  camera.position.z = 10;

  controls.update();

  const geometry = new THREE.BoxGeometry( 700, 1, 450 );
  const material = new THREE.MeshBasicMaterial( {color: 0x282a36} );
  const cube = new THREE.Mesh( geometry, material );
  cube.position.set(350,0,225)
  scene.add( cube );

  //loadField(scene);
  loadBall(scene);
  loadRoad(scene);
  loadBuilding(scene);
  loadLight(scene);
  loadPlayer1(scene);
  loadPlayer2(scene);
  loadInput(window);

  const animate = function () {
    animationFrameId = requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
  };

  animate();
});

onUnmounted(() => {
  cancelAnimationFrame(animationFrameId);
  unloadPlayer1();
  unloadPlayer2();
  renderer.dispose();
  scene = null;
  camera = null;
  renderer = null;
  controls = null;
  unloadInput(window);
  unloadWS();
});
</script>

<template>
  <div id="game" class="position-relative d-flex vh-100 justify-content-center align-items-center">
    <header class="position-absolute top-0 start-50 translate-middle-x p-3" style="background-color: rgba(0, 0, 0, 0);">
      <div class="container d-flex flex-column justify-content-center align-items-center">
        <p class="h1 text-white">Score: {{ scores.player1 }} - {{ scores.player2 }}</p>
        <p class="h1 text-white" v-if="scores.error === 'Game is paused'">Game is paused</p>
      </div>
    </header>
    <b-modal v-model="modals.errorModal" title="There was an Error!">
      <p>{{ scores.error }}</p>
      <template #footer>
        <b-button variant="primary" @click="navigateHome">Quit Game</b-button>
      </template>
    </b-modal>
    <b-modal v-model="modals.finishModal" title="Game Ended">
      <p>Score: {{ scores.player1 }} - {{ scores.player2 }}</p>
      <p>Winner: {{ scores.player1 > scores.player2 ? 'Player 1' : 'Player 2' }}</p>
      <template #footer>
        <b-button variant="secondary" @click="navigateStats">Show stats</b-button>
        <b-button variant="primary" @click="navigateHome">Quit Game</b-button>
      </template>
    </b-modal>
  </div>
</template>