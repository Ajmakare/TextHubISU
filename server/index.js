// server/index.js

import student_db_functions from './Controllers/studentController.js';

import express from "express";

const PORT = process.env.PORT || 3001;

const app = express();

//Root endpoint
app.get("/", (request, response) => {
  response.json({info: "Node.js Express API - WORKING :)"})
})

//Example endpoint
app.get("/textbooks", student_db_functions.getTextbooks);

app.listen(PORT, () => {
  console.log(`Server listening on ${PORT}`);
});
