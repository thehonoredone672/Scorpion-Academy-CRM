const mongoose = require('mongoose');

const leadSchema = new mongoose.Schema({
    branch: { type: mongoose.Schema.Types.ObjectId, ref: 'Branch' },
    name: { type: String, required: true },
    parentName: String, // Critical for kids' batches
    phone: { type: String, required: true },
    whatsapp: String,
    age: Number,
    program: { type: String, enum: ['Karate', 'Silambam', 'Yoga', 'Self Defense'] },
    source: String, // Poster, Meta Ads, Referral, Walk-in
    status: { 
        type: String, 
        enum: ['New', 'Contacted', 'Trial Booked', 'Joined', 'Not Interested'], 
        default: 'New' 
    },
    followUpDate: Date,
    createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Lead', leadSchema);