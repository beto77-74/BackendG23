import express from "express";
import { productoRouter } from "./routes/productos_router.js";
import { clientesRouter } from "./routes/clientes_router.js";
import { usuarioRouter } from "./routes/usuarios_router.js";
import { archivosRouter } from "./routes/archivos_router.js";

const servidor = express();

// Nullish coalescing operator
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Nullish_coalescing
const PORT = process.env.PORT ?? 3000;
servidor.use(express.json());

// Aca dejamos las rutas declaradas en nuestros routes
servidor.use(productoRouter);
servidor.use(clientesRouter);
servidor.use(usuarioRouter);
servidor.use(archivosRouter);

servidor.listen(PORT, (error) => {
  if (error) {
    throw error;
  }
  console.log(`Servidor corriendo en http://127.0.0.1:${PORT}`);
});