import { Router } from "express";
import { crearProducto, devolverProducto, listarProductos, actualizarProducto, eliminarProducto } from "../controllers/productos_controllers.js";

export const productoRouter = Router();
//productoRouter.post("/productos", crearProducto);
//productoRouter.get("/productos", listarProductos);

productoRouter.route("/productos").get(listarProductos).post(crearProducto);

productoRouter.route("/producto/:id").get(devolverProducto).put(actualizarProducto).delete(eliminarProducto);

//productoRouter.route("/producto/:id").put(actualizarProducto);