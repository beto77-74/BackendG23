import { Schema,model } from "mongoose"

const productSchema = new Schema({
    nombre: {type:String, required:true},
    precio: {type: Number, required:true},
    descripcion: {type:String},
});

export default model("Producto", productSchema)