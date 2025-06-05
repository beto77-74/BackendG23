import { Schema,model } from "mongoose";

const NotasSchema = Schema ({
    nombre: {
        type: Schema.Types.String,
        require:true,
        trim:true,
    },
    descripcion:{
        type: Schema.Types.String,
        trim:true,
    },
    orden:{
        type:Schema.Types.Int32,
        min:0,
    },
    etiquetas:{
        type:Schema.Types.Array,
        default:[],
    },
    usuarioId:{
        type: Schema.Types.ObjectId,
        require:true,
        alias:"Usuario_id",
    },
});

export const NotasModel = model("Notas",NotasSchema);