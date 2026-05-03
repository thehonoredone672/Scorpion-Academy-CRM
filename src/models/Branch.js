const mongoose = require('mongoose');
const branchSchema = new mongoose.Schema({
    name: String, // e.g., "Chennai Main"
    slug: { type: String, unique: true }, // e.g., "chennai-main"
    password: { type: String, required: true },
    instructor: String
});
module.exports = mongoose.model('Branch', branchSchema);