import * as THREE from "three";

export function loadLight(scene) {
  const light = new THREE.AmbientLight(0xffffff, 1); // white light, full intensity
  scene.add(light);
}