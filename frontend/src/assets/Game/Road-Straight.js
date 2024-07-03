import roadModel from './Road-Straight.glb';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

export function loadRoad(scene) {
  const loader = new GLTFLoader();

  loader.load(roadModel, (gltf) => {
    gltf.scene.position.set(0, 0, -50);
    gltf.scene.scale.set(50,50,50);
    scene.add(gltf.scene);
  }, undefined, (error) => {
    //console.error('An error occurred while loading the Road', error);
  });

  loader.load(roadModel, (gltf) => {
    gltf.scene.position.set(0, 0, 50);
    gltf.scene.scale.set(50,50,50);
    scene.add(gltf.scene);
  }, undefined, (error) => {
    //console.error('An error occurred while loading the Road', error);
  });

  loader.load(roadModel, (gltf) => {
      gltf.scene.position.set(0, 0, 150);
      gltf.scene.scale.set(50,50,50);
      scene.add(gltf.scene);
  }, undefined, (error) => {
      //console.error('An error occurred while loading the Road', error);
  });

  loader.load(roadModel, (gltf) => {
      gltf.scene.position.set(0, 0, 250);
      gltf.scene.scale.set(50,50,50);
      scene.add(gltf.scene);
  }, undefined, (error) => {
      //console.error('An error occurred while loading the Road', error);
  });

  loader.load(roadModel, (gltf) => {
      gltf.scene.position.set(0, 0, 350);
      gltf.scene.scale.set(50,50,50);
      scene.add(gltf.scene);
  }, undefined, (error) => {
      //console.error('An error occurred while loading the Road', error);
  });

  loader.load(roadModel, (gltf) => {
      gltf.scene.position.set(0, 0, 450);
      gltf.scene.scale.set(50,50,50);
      scene.add(gltf.scene);
  }, undefined, (error) => {
      //console.error('An error occurred while loading the Road', error);
  });

  loader.load(roadModel, (gltf) => {
      gltf.scene.position.set(0, 0, 500);
      gltf.scene.scale.set(50,50,50);
      scene.add(gltf.scene);
  }, undefined, (error) => {
      //console.error('An error occurred while loading the Road', error);
  });

   loader.load(roadModel, (gltf) => {
      gltf.scene.position.set(700, 0, -50);
      gltf.scene.scale.set(50,50,50);
      scene.add(gltf.scene);
  }, undefined, (error) => {
      //console.error('An error occurred while loading the Road', error);
  });

  loader.load(roadModel, (gltf) => {
      gltf.scene.position.set(700, 0, 50);
      gltf.scene.scale.set(50,50,50);
      scene.add(gltf.scene);
  }, undefined, (error) => {
      //console.error('An error occurred while loading the Road', error);
  });

  loader.load(roadModel, (gltf) => {
      gltf.scene.position.set(700, 0, 150);
      gltf.scene.scale.set(50,50,50);
      scene.add(gltf.scene);
  }, undefined, (error) => {
      //console.error('An error occurred while loading the Road', error);
  });

  loader.load(roadModel, (gltf) => {
      gltf.scene.position.set(700, 0, 250);
      gltf.scene.scale.set(50,50,50);
      scene.add(gltf.scene);
  }, undefined, (error) => {
      //console.error('An error occurred while loading the Road', error);
  });

  loader.load(roadModel, (gltf) => {
      gltf.scene.position.set(700, 0, 350);
      gltf.scene.scale.set(50,50,50);
      scene.add(gltf.scene);
  }, undefined, (error) => {
      //console.error('An error occurred while loading the Road', error);
  });

  loader.load(roadModel, (gltf) => {
      gltf.scene.position.set(700, 0, 450);
      gltf.scene.scale.set(50,50,50);
      scene.add(gltf.scene);
  }, undefined, (error) => {
      //console.error('An error occurred while loading the Road', error);
  });

  loader.load(roadModel, (gltf) => {
      gltf.scene.position.set(700, 0, 500);
      gltf.scene.scale.set(50,50,50);
      scene.add(gltf.scene);
  }, undefined, (error) => {
      //console.error('An error occurred while loading the Road', error);
  });

}