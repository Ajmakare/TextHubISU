import { response } from "express";
import Pool from "pg";

const pgPool = Pool.Pool;

const pool = new pgPool({
    user: "dev-texthub",
    host: "34.134.83.78",
    database: "texthubdatabase",
    password: "texthub123",
    port:"5432"
});

const getTextbooks = async(request, respones) => {
    pool.query("SELECT * FROM textbooks", (error, results) => {
        if(error) {throw error;}
        response.status(200).json(results);
    });
};

export default {
    getTextbooks
};







