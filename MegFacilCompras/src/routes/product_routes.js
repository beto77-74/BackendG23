import express from "express"
import { addProduct, deleteProduct, getProducts, updateProduct } from "../controllers/product_controller.js";

const router = express.Router()

router.get("/", getProducts);
router.post("/", addProduct);
router.delete("/:productId", deleteProduct);
router.put("/:productId", updateProduct);

export default router