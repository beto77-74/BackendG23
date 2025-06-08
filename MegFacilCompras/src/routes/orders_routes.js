import express from "express";
import { getOrders, addOrders } from "../controllers/order_controller.js";

const router = express.Router()

router.get("/", getOrders);
router.post("/",addOrders);

export default router;