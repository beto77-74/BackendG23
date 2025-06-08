import express from "express";
import { config } from 'dotenv';
import connectDB from "./config/db.js";
import morgan from "morgan";
import ProductRoutes from "./routes/product_routes.js";
import OrderRoutes from "./routes/orders_routes.js"


config()
connectDB();

const servidor = express();
const PORT = process.env.PORT;

servidor.use(express.json())
servidor.use(morgan("dev"))

servidor.use("/api/producto",ProductRoutes);
servidor.use("/api/ordenes",OrderRoutes);

servidor.listen(PORT, async () => {
    try {
        console.log(`Servidor corriendo en http://127.0.0.1:${PORT}`);
    } catch (error){
        console.log('Error al levantar el servidor');
        console.log(error.message);
    }
});