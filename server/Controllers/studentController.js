import { response } from "express";
import Pool from "pg";
import * as dotenv from "dotenv";
dotenv.config()

const pgPool = Pool.Pool;

const pool = new pgPool({
    user: process.env.USERNAME,
    host: process.env.HOST,
    database: "texthubdatabase",
    password: process.env.PASSWORD,
    port:"5432"
});

const getTextbooks = async(request, respones) => {
    pool.query("SELECT * FROM textbook", (error, results) => {
        if(error) {throw error;}
        response.status(200).json(results);
    });
};

export default {
    getTextbooks
};







