import {z} from 'zod'

export const registrarUsuarioSerializer = z.object({
    nombre: z.string(),
    correo: z.string().email({ message:"Fornato invalido"}),
    password: z
        .string("^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#$%^&*()_+])[A-Za-z0-9!@#$%^&*()_+]{8,}$")
        .regex(
            new RegExp(),
        {
            message:
            "El password debe tener al menos una may, minu, un numero y un caracter especial",
        }    
        ),
    });

export const loginUsuarioSerializer = z.object({
        correo:z.string(),
        password:z.string(),
    });

export const cambiarPasswordSerializer = z.object({
    antiguaPassword: z.string(),
    nuevaPassword: z.string(),
});