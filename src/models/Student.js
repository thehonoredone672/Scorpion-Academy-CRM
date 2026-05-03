const mongoose = require('mongoose');
const studentSchema = new mongoose.Schema({
    branch: { type: mongoose.Schema.Types.ObjectId, ref: 'Branch' },
    name: String,
    beltRank: { type: String, default: 'White' },
    programs: [String], // Karate, Silambam, etc.
    joinDate: { type: Date, default: Date.now },
    fees: {
        plan: Number,
        dueDate: Date,
        status: { type: String, default: 'Paid' }
    },
    attendance: [{ date: String, status: String }]
});
module.exports = mongoose.model('Student', studentSchema);