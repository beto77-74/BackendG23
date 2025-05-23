import { Client } from 'pg';
import { config } from "dotenv";
config();

const cliente = new Client({
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    host: process.env.DB_HOST,
    port: process.env.DB_PORT,
    database: process.env.DB_NAME,
})

cliente.connect ((error) => {
    if (error) {
        throw error;
    }
});

export default cliente;