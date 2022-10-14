// server/index.js

import student_db_functions from './Controllers/studentController.js';

import express from "express";

const PORT = process.env.PORT || 3001;

const app = express();

//Example endpoint
app.get("/textbooks", student_db_functions.getTextbooks);

app.listen(PORT, () => {
  console.log(`Server listening on ${PORT}`);
});
