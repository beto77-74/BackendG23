import { Router } from "express";
import * as NotasController from "../controllers/notas_controller.js"; 
import { validarToken } from "../utils/validar_token.js";

export const notasRouter = Router();

notasRouter
    .route("/notas")
    .all(validarToken)
    .post(NotasController.crearNota)
    .get(NotasController.buscarNota);
