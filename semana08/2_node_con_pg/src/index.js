import express from "express"
import { config } from "dotenv";
import { productoRouter } from "./routers/productos_routers.js";

config();

const servidor = express();
const PORT = process.env.PORT ?? 3000;

servidor.use(express.json());

servidor.get ('/status',(req,res) => {
    const horaServidor = new Date();

    res.json({
        status: "Activo",
        hora: horaServidor,
    });
});

servidor.use(productoRouter);

servidor.listen(PORT,(error) =>{
    if (error) {
        console.error(error);
    } else {
        console.log (`Servidor corriendo exitosamente en el puerto ${PORT}`);
    }

})