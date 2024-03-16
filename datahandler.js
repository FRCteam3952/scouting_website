// We know that all the data should exist in ./data/<team number>/<qual or playoff>/<match number>.txt
// Given a request for a team number, we should iterate through all files in ./data/<team number>/*, then make sure all required data points exist in each json,
// then we can output that data into a CSV format for viewing in Google Sheets or whatever

const fs = require('fs');
