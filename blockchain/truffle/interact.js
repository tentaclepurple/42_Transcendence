const SimpleStorage = artifacts.require("SimpleStorage");

module.exports = async function () {
  try {
    const instance = await SimpleStorage.deployed();

    // Imprimir el valor almacenado
    const initialData = await instance.getData();
    console.log("Valor almacenado inicialmente:", initialData.toNumber());

    // Cambiar el valor
    const newValue = 777; // Puedes cambiar este valor según sea necesario
    const setResult = await instance.setData(newValue);
   // console.log("Transaction Hash para cambiar el valor:", setResult.tx);

    // Imprimir el nuevo valor
    const newData = await instance.getData();
    console.log("Nuevo valor almacenado:", newData.toNumber());
    
    // Asegúrate de llamar a process.exit() al final del script
    process.exit(0);
  } catch (error) {
    console.error("Error en el script:", error);
    process.exit(1);
  }
};
