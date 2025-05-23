const nombre ='Carlos'
let edad= 51
edad=33
edad=35
edad='cuarenta'

function sumar(numero1,numero2){
    const resultado = numero1 + numero2
    return resultado;
}

const sumatoria = sumar(10,5)
console.log('Resultado es:' , sumatoria)

const sumatoria2 = sumar('a',80)
console.log('Resultado es:' , sumatoria2)

const restar = (numero1, numero2) => {
    const resultado = numero1 - numero2
    return resultado
}
const resta = restar (20,10)
console.log('Resultado de la resta es:', resta)