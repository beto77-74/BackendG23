import { Schema, model } from "mongoose";
import { genSaltSync, hashSync } from "bcrypt";

const usuarioSchema = new Schema({
    nombre : Schema.Types.String,
    correo : {
        type: Schema.Types.String,
    },
    password: {
        type:Schema.Types.String,
        set : (valor) => {
            const salt = genSaltSync();
            const hashPassword = hashSync(valor, salt);

            return hashPassword;
        },
    },
});

export const UsuarioModel = model("usuarios",usuarioSchema);