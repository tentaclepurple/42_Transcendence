import fieldModel from './Field.glb';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

export function loadField(scene) {
  const loader = new GLTFLoader();
  loader.load(fieldModel, (gltf) => {
    gltf.scene.position.set(0, -1, 0);
    gltf.scene.scale.set(0.5, 0.5, 0.5);
    scene.add(gltf.scene);
  }, undefined, (error) => {
    //console.error('An error occurred while loading the Field', error);
  });
}