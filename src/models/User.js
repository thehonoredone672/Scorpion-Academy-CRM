const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
    name: { type: String, required: true },
    username: { type: String, unique: true },
    phonenumber: String,
    email: { type: String, unique: true },
    discipline: { type: String, enum: ['Karate', 'Silambam', 'Both'] },
    beltLevel: String,
    address: String,
    active: { type: Boolean, default: true },
    plan: String,
    createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('User', userSchema);