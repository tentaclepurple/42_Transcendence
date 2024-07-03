import ballModel from './Ball.glb';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

let Ball;

export function loadBall(scene) {
  const loader = new GLTFLoader();
  loader.load(ballModel, (gltf) => {
    Ball = gltf.scene;
    gltf.scene.position.set(0, 1, 0);
    gltf.scene.scale.set(1,1,1);
    scene.add(gltf.scene);
  }, undefined, (error) => {
    console.error('An error occurred while loading the Ball', error);
  });
}

export function moveBall(x, y) {
  if (Ball) {
    Ball.position.x = x;
    Ball.position.z = y;
  }
}