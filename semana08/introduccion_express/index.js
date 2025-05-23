import express from "express";

const servidor = express();
const PORT = 3000;

servidor.use(express.json())


servidor.get('/',(req,res) => {
    console.log(req.body);
    return res.json({message: "Bienvenido a mi API"});
}
)

servidor.post("/obtener-datos",(req,res) => {
    console.log(req.body);

    return res.status(201).json({message: "Registro exitoso"});
})

servidor.listen(PORT,(error) => {
    if (error) {
        console.log("Hubo un error");
    }else {
        console.log (`Servidor corriendo http://127.0.0.1:${PORT}`);
    }
});