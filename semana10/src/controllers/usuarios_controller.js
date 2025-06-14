import { json } from "express";
import { UsuarioModel } from "../models/usuarios.js";
import { cambiarPasswordSerializer, 
         loginUsuarioSerializer, 
         registrarUsuarioSerializer } from "./usuarios_serializer.js";
import { compareSync, genSaltSync, hashSync } from "bcrypt";
import JWT from 'jsonwebtoken';

export const crearUsuario = async (req,res) => {
const serializador = registrarUsuarioSerializer.safeParse(req.body);

if (serializador.error) {
    return res.status(400).json ({
        message: "Error al crear el usuario",
        content: serializador.error,
    });
}
 const nuevoUsuario = await UsuarioModel.create(serializador.data)

 const usuario = nuevoUsuario.toJSON();

 delete usuario.password;

 return res.status(201).json ({
     message: "usuario creado exitosamnete",
     content: usuario,


 });
};

export const login = async (req,res) => {
    const serializador = loginUsuarioSerializer.safeParse(req.body);

    if (serializador.error) {
        return res.status(400).json ({
            message:"Error al hacer el login",
            content: serializador.error,
        });
    }

    const usuarioEncontrado = await UsuarioModel.findOne({
        correo: serializador.data.correo,
    });

    if (!usuarioEncontrado) {
        return res.status(400).json ({
            message: "Credenciales incorrectas",
        });
    }

    const password = usuarioEncontrado.password;
    const esLaPassword =compareSync(serializador.data.password, password);
    
    if (esLaPassword){
        const token = JWT.sign(
            {usuarioId: usuarioEncontrado._id},
            process.env.JWT_SECRET_KEY,
            { expiresIn:3600}
        );
        return res.json({
        message: "Bienvenido",
        content:token,
        });
    } else {
        return res.status(400).json ({
            message: "Credenciales incorrectas",
        });
    }
};

export const cambiarPassword = async (req,res)=> {
    const serializador = cambiarPasswordSerializer.safeParse(req.body);
    if (serializador.error){
        return res.status(400).json ({
            message: "Error al cambiar el password",
            content: serializador.error,
        });
    }
    const passwordHashed = req.user.password

    const esLaPassword = compareSync (
        serializador.data.antiguaPassword,
        passwordHashed
    );

    if (esLaPassword) {
        //const salt = genSaltSync();
        //const nuevaPassword = hashSync(serializador.data.nuevaPassword, salt);
        await UsuarioModel.updateOne(
            {_id: req.user._id},
            { $set : {password: serializador.data.nuevaPassword}}
        );

        return res.json ({
            message: "Password actualizada exitosamente",
        });
    } else {
        return res.status(403).json({
            message:"La antigua password es incorrecta"
        })

    }
}