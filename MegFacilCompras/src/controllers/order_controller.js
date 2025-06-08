import Order from "../models/orders_model.js"

//obteniendo todas las ordenes
export const getOrders = async(req,res) => {
    try{
        const ordenes = await Order.find()
        if(!ordenes || ordenes.length===0){
            return res.status(404).json({
                message:"No existe ninguna orden"
            })
        }
        return res.json(ordenes)
    } catch(error){
        console.error("Eroor al obtener las ordenes", error)
        return res.status(500).json({
            message:"Error interno del servidor"
        })
    }
}

//adicionar ordenes
export  const addOrders = async(req,res) => {    
    try{
        const nuevaOrden = new Order(req.body)
        if(!nuevaOrden || nuevaOrden.length===0){
          return res.status(404).json({
             message: "No se puede crear la orden falta un dato"
          })
        } await nuevaOrden.save()
        return res.status(201).json(nuevaOrden);
    }
    catch (error){
        console.error("Error al crear la orden", error)
        return res.status(500).json({
            message:"Error interno del servidor"
        });
    }
}