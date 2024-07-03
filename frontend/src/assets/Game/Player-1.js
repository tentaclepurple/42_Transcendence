import player1Model from './Car Police.glb';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import * as THREE from "three";

let Player1;
let cube2;

export function loadPlayer1(scene) {
    const loader = new GLTFLoader();
    loader.load(player1Model, (gltf) => {
        Player1 = gltf.scene;
        Player1.position.set(0 - 15, 6, 225 + 50);
        Player1.rotation.y = Math.PI;
        Player1.scale.set(100, 100, 100);
        scene.add(Player1);
    }, undefined, (error) => {
        //console.error('An error occurred while loading the Player1', error);
    });
}

export function unloadPlayer1() {
}

export function setPositionPlayer1(x, z) {
    if (Player1) {
        Player1.position.x = x - 15;
        Player1.position.z = z+50;
    }
}