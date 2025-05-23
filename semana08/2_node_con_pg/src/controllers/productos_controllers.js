import { crearProductoSerializer } from "./serializers/productos_serializers.js";
import conexion from "../conexion.js";

export const crearProducto = async (req, res) => {
    const serializador = crearProductoSerializer.safeParse(req.body);

    if (serializador.error) {
        return res.json ({
        message: "Error al crear el producto",
        content : serializador.error,
    });
}
const dataValidada = serializador.data;
const nuevoProducto = await conexion.query (
    "INSERT INTO productos (nombre, precio) VALUES ($1, $2) RETURNING*",
    [dataValidada.nombre, dataValidada.precio]
);
console.log(dataValidada)

console.log(nuevoProducto.rows);
return res.json ({
    message: "Producto creado exitosamente",
});
};

export const listarProductos = async (req,res) => {
    const productos = await conexion.query("SELECT * FROM productos");

    console.log(productos.rows);
    return res.json({
        content:productos.rows,
    });
};

export const devolverProducto = async (req,res) => {
    const id = req.params.id;
    const productoEncontrado = await conexion.query(
        "SELECT * FROM productos WHERE id = $1 LIMIT 1",
        [id]
    );

    if (productoEncontrado.rows[0] === undefined) {
        return res.status(404).json ({
            message: "Producto no encontrado",
        })
    }

    return res.json({
        content:productoEncontrado.rows[0],
    });
};

// export const actualizarProducto = async (req,res) => {
//     const id = req.params.id;
//     const nombre = req.body.nombre;
//     const precio = req.body.precio;
//     const productoActualizado = await conexion.query(
//         "UPDATE productos SET nombre = $1 , precio = $2 WHERE id = $3 RETURNING*",
//         [nombre,precio,id]
//     );

//     if (productoActualizado.rowCount===0) {
//         return res.status(404).json ({
//             message: "Producto no actualizado"
//         })
//     }

//     return res.json({
//         content:productoActualizado.rows[0],
//     });
// };

export const actualizarProducto = async (req,res) => {
    const serializador = crearProductoSerializer.safeParse(req.body);
    const id = req.params.id;

    if (serializador.error) {
        return res.status(400).json ({
            message: "Error al actualizar el producto",
            content: serializador.error,
        });
    }

    const { nombre, precio } = serializador.data;

    try {
        await conexion.query("BEGIN");
        const productoActualizado = await conexion.query(
            "UPDATE productos SET nombre=$1, precio=$2 WHERE id=$3 RETURNING*",
            [nombre, precio, id]
        );

        if (1===1) {
            //throw Error("Error inesperado");
        }
        await conexion.query("COMMIT");
        if (!productoActualizado.rows[0]) {
            return res.status(400).json ({
               message:"El producto a actualizar no existe" ,
            });
        }
        return res.json ({
            message:"Prodcuto actualizado exitosamentee" ,
            content : productoActualizado.rows[0],
        });
    } catch (error) {
        await conexion.query("ROLLBACK");
        return res.status(500).json ({
            messaage: "Ocurrio un error al hacer la operacion"
        })
    }
}

export const eliminarProducto = async (req, res) => {
    const { id } = req.params;

    const productoEliminado = await conexion.query(
        "DELETE productos WHERE id = $1 RETURNING id",
        [id]
    );

    if (productoEliminado.rows[0]) {
        return res.status(400).json ({
            message: "El producto a eliminar no existe"
        })
    }

    return res.json({
        message: "Producto eliminado exitosamnete",
    });

};
