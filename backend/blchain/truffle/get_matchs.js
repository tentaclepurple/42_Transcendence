const MatchStorage = artifacts.require("MatchStorage");

module.exports = async function () {
  try {
    const instance = await MatchStorage.deployed();

    const storedData = await instance.getAllStrings();

    const blchainData =storedData.join('\n');

    console.log(blchainData);

    process.exit(0);
  } catch (error) {
    console.error("Error en el script:", error);
    process.exit(1);
  }
};