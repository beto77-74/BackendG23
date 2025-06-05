import express from "express";
import http from "http";
import { Server } from "socket.io";
import { config } from "dotenv";
import { info } from "console";
config();

const app = express();
const servidor = http.createServer(app);
const socket = new Server(servidor, {cors: { origin: "*"}});
const PORT = process.env.PORT;

app.use(express.json());

app.get("/", (req,res) => {
    return res.json ({
        message: "Bienvenido a mi API",
    });
});

socket.on('connection',(info) => {
    console.log(info);
});

servidor.listen(PORT, () => {
    console.log(`Servidor corriendo exitosamente en el puerto http://127.0.0.1:${PORT}`);
});