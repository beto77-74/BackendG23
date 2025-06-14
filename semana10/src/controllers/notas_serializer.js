import {string, z} from "zod";

export const crearNotaSerializer = z.object({
    nombre: z.string(),
    descripcion: z.string().optional(),
    orden: z.number(),
    etiquetas: z.array(z.string()).optional(),
});
