const socket = io("http://127.0.0.1:3000");
const form = document.getElementById("formulario");
const input = document.getElementById("input");
const mensajes = document.getElementById("mensajes");


form.addEventListener("submit",(e) => {
    e.preventDefault();
});

socket.on ("connect", (data) => {
    console.log("El id de mi cliente es:",socket.id);
});

socket.on ("connection", (usuario)=> {
    usuario.on()
    console.log(data);
})