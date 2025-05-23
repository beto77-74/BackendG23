const parImpar = (numero) => {
    // if (numero % 2 === 0) {
    //     return true;
    // } else{
    //     return false;
    // }
    return numero % 2 === 0 ? true : false;
};

const esPositivo = (numero) => (numero >= 0) ? true : false;

module.exports = {
    parImpar,
    esPositivo,
};