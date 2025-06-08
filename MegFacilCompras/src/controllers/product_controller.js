import Producto from "../models/product_model.js";

//visualizar los productos
export const getProducts = async (req,res) => {
    try{
        const productos = await Producto.find()
        if(!productos || productos.length===0){
            return res.status(404).json({
                message:"No hay productos cargados"
            });
        }
        return res.json(productos)
    }catch {
        console.log("Error al obtener los productos", error)
        return res.status(500).json({
            message:"Error interno del servidor"
        });
    }
}

//agregar productos
export const addProduct = async (req,res) => {
    try{
        const newProduct = new Producto(req.body);
        if(!newProduct){
            return res.status(404).json({
                message: "Campos incompletos"
            });
        } await newProduct.save();
        return res.status(201).json(newProduct);
    } catch(error) {
        console.error("Error al guardar el producto", error);
        return res.status(500).json({
            message: "Error interno del servidor"
        });
    }
};

//eliminar productos
export const deleteProduct = async(req,res) => {
    try {
        const deleteProduct = await Producto.findByIdAndDelete(req.params.productId)
        if (!deleteProduct || deleteProduct.length===0) {
            return res.status(404).json({
                message:"El producto no existe"
            });
        }
        return res.status(201).json({
            message:"Producto eliminado satisfactoriamente"
        })
    } catch (error) {
        console.error("Error al eliminar el producto", error);
        return res.status(500).json ({
            message: "Error interno del servidor"
        }
        )
    }
}

//actualizar productos
export const updateProduct = async(req,res) => {
    try {
        const updateProduct = await Producto.findByIdAndUpdate(req.params.productId,req.body)
        if (!updateProduct || updateProduct.length===0) {
            return res.status(404).json({
                message:"El producto no se puede actualizar"
            });
        }
        return res.status(201).json({
            message:"Producto actualizado satisfactoriamente"
        })
    } catch (error) {
        console.error("Error al actualizar el producto", error);
        return res.status(500).json ({
            message: "Error interno del servidor"
        }
        )
    }
}