import buildingModel1 from './Buildings/Building 1.glb';
import buildingModel2 from './Buildings/Building 2.glb';
import buildingModel3 from './Buildings/Building 3.glb';
import buildingModel4 from './Buildings/Building 4.glb';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

export function loadBuilding(scene) {
  const loader = new GLTFLoader();
  loader.load(buildingModel1, (gltf) => {
    gltf.scene.position.set(50, 0, 500);
    gltf.scene.rotation.y = Math.PI;
    gltf.scene.scale.set(50,50,50);
    scene.add(gltf.scene);
  }, undefined, (error) => {
    //console.error('An error occurred while loading the Building', error);
  });
  loader.load(buildingModel4, (gltf) => {
    gltf.scene.position.set(150, 0, 500);
    gltf.scene.rotation.y = Math.PI;
    gltf.scene.scale.set(50,50,50);
    scene.add(gltf.scene);
  }, undefined, (error) => {
    //console.error('An error occurred while loading the Building', error);
  });
  loader.load(buildingModel2, (gltf) => {
    gltf.scene.position.set(250, 0, 500);
    gltf.scene.rotation.y = Math.PI;
    gltf.scene.scale.set(50,50,50);
    scene.add(gltf.scene);
  }, undefined, (error) => {
    //console.error('An error occurred while loading the Building', error);
  });
  loader.load(buildingModel1, (gltf) => {
    gltf.scene.position.set(350, 0, 500);
    gltf.scene.rotation.y = Math.PI;
    gltf.scene.scale.set(50,50,50);
    scene.add(gltf.scene);
  }, undefined, (error) => {
    //console.error('An error occurred while loading the Building', error);
  });
  loader.load(buildingModel1, (gltf) => {
    gltf.scene.position.set(450, 0, 500);
    gltf.scene.rotation.y = Math.PI;
    gltf.scene.scale.set(50,50,50);
    scene.add(gltf.scene);
  }, undefined, (error) => {
    //console.error('An error occurred while loading the Building', error);
  });

  loader.load(buildingModel3, (gltf) => {
    gltf.scene.position.set(550, 0, 500);
    gltf.scene.rotation.y = Math.PI;
    gltf.scene.scale.set(50,50,50);
    scene.add(gltf.scene);
  }, undefined, (error) => {
    //console.error('An error occurred while loading the Building', error);
  });

  loader.load(buildingModel2, (gltf) => {
    gltf.scene.position.set(650, 0, 500);
    gltf.scene.rotation.y = Math.PI;
    gltf.scene.scale.set(50,50,50);
    scene.add(gltf.scene);
  }, undefined, (error) => {
    //console.error('An error occurred while loading the Building', error);
  });

  loader.load(buildingModel4, (gltf) => {
      gltf.scene.position.set(50, 0, -50);
      gltf.scene.scale.set(50,50,50);
      scene.add(gltf.scene);
  }, undefined, (error) => {
      //console.error('An error occurred while loading the Building', error);
  });

  loader.load(buildingModel1, (gltf) => {
      gltf.scene.position.set(150, 0, -50);
      gltf.scene.scale.set(50,50,50);
      scene.add(gltf.scene);
  }, undefined, (error) => {
      //console.error('An error occurred while loading the Building', error);
  });

  loader.load(buildingModel3, (gltf) => {
      gltf.scene.position.set(250, 0, -50);
      gltf.scene.scale.set(50,50,50);
      scene.add(gltf.scene);
  }, undefined, (error) => {
      //console.error('An error occurred while loading the Building', error);
  });

  loader.load(buildingModel2, (gltf) => {
      gltf.scene.position.set(350, 0, -50);
      gltf.scene.scale.set(50,50,50);
      scene.add(gltf.scene);
  }, undefined, (error) => {
      //console.error('An error occurred while loading the Building', error);
  });

  loader.load(buildingModel4, (gltf) => {
      gltf.scene.position.set(450, 0, -50);
      gltf.scene.scale.set(50,50,50);
      scene.add(gltf.scene);
  }, undefined, (error) => {
      //console.error('An error occurred while loading the Building', error);
  });

  loader.load(buildingModel3, (gltf) => {
      gltf.scene.position.set(550, 0, -50);
      gltf.scene.scale.set(50,50,50);
      scene.add(gltf.scene);
  }, undefined, (error) => {
      //console.error('An error occurred while loading the Building', error);
  });

  loader.load(buildingModel1, (gltf) => {
      gltf.scene.position.set(650, 0, -50);
      gltf.scene.scale.set(50,50,50);
      scene.add(gltf.scene);
  }, undefined, (error) => {
      //console.error('An error occurred while loading the Building', error);
  });

}