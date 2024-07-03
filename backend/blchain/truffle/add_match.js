const MatchStorage = artifacts.require("MatchStorage");

module.exports = async function () {
  try {
    const newString = process.argv[process.argv.length - 1];

    if (typeof newString !== 'string' || newString.trim() === '') {
      console.error("String inválido:", newString);
      process.exit(1);
    }

    const instance = await MatchStorage.deployed();

    // Añadir el nuevo string al array
    const setResult = await instance.addString(newString);
    console.log(newString);

    // Asegúrate de llamar a process.exit() al final del script
    process.exit(0);
  } catch (error) {
    console.error("Error en el script JS:", error);
    process.exit(1);
  }
};