import player2Model from './Car Taxi.glb';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import * as THREE from "three";

let Player2;
let cube2;

export function loadPlayer2(scene) {
    const loader = new GLTFLoader();
    loader.load(player2Model, (gltf) => {
        Player2 = gltf.scene;
        Player2.position.set(700 + 15, 6, 225 + 50);
        Player2.rotation.y = Math.PI;
        Player2.scale.set(100,100,100);
        scene.add(Player2);
    }, undefined, (error) => {
        //console.error('An error occurred while loading the Player2', error);
    });
}

export function unloadPlayer2() {
}

export function setPositionPlayer2(x, z) {
    if (Player2) {
        Player2.position.x = x + 15;
        Player2.position.z = z + 50;
    }
}