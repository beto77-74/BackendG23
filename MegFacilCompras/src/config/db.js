import mongoose from "mongoose";

const connectDB =async () => {
    try {
        await mongoose.connect(process.env.MONGO_URL);
        console.log("Base de datos conectada");
    }catch (error) {
        console.log("Error al conectar la base de datos");
    }
};

export default connectDB;