import { Schema, model } from "mongoose";

const orderSchema = new Schema({
    productoId:{type:String},
    nombre:{type:String},
    precio:{type:Number,required:true},
    cantidad:{type:Number,required:true},
    date:{type:Date, default:Date.now}
});

export default model("Ordenes",orderSchema)