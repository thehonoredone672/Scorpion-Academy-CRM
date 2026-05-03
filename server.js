require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const jwt = require('jsonwebtoken');
const path = require('path');
const cors = require('cors');

// Import Models
const Branch = require('./src/models/Branch');
const Lead = require('./src/models/Lead');
const Student = require('./src/models/Student');

const app = express();

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'src', 'public')));
app.use(cors());

// --- DATABASE CONNECTION ---
const MONGO_URI = process.env.MONGO_URI || "mongodb://127.0.0.1:27017/scorpion_academy";

mongoose.connect(MONGO_URI)
    .then(() => console.log('✅ Connected to Local MongoDB: Scorpion Academy'))
    .catch(err => console.error('❌ MongoDB Connection Error:', err));

// --- AUTH MIDDLEWARE ---
const authenticate = (req, res, next) => {
    const token = req.headers.authorization;
    if (!token) return res.status(401).json({ error: 'Access Denied. No token provided.' });

    try {
        const verified = jwt.verify(token, process.env.JWT_SECRET);
        req.branchId = verified.branchId;
        next();
    } catch (err) {
        res.status(400).json({ error: 'Invalid Token' });
    }
};

// --- AUTH ROUTES ---

// Branch Login
app.post('/api/login', async (req, res) => {
    const { slug, password } = req.body;
    try {
        const branch = await Branch.findOne({ slug, password });
        if (!branch) return res.status(400).json({ error: 'Invalid Branch ID or Password' });

        const token = jwt.sign({ branchId: branch._id }, process.env.JWT_SECRET);
        res.json({ token, branchName: branch.name });
    } catch (err) {
        res.status(500).json({ error: 'Server Error during login' });
    }
});

// --- LEAD MANAGEMENT ROUTES ---

// Add New Lead (Enquiry)
app.post('/api/leads', authenticate, async (req, res) => {
    try {
        const newLead = new Lead({
            ...req.body,
            branch: req.branchId
        });
        await newLead.save();
        res.status(201).json({ message: 'Enquiry saved successfully' });
    } catch (err) {
        res.status(500).json({ error: 'Failed to save enquiry' });
    }
});

// Get Leads for logged-in branch
app.get('/api/leads', authenticate, async (req, res) => {
    try {
        const leads = await Lead.find({ branch: req.branchId }).sort({ createdAt: -1 });
        res.json(leads);
    } catch (err) {
        res.status(500).json({ error: 'Failed to fetch leads' });
    }
});

// --- STUDENT MANAGEMENT ROUTES ---

// Add New Student
app.post('/api/students', authenticate, async (req, res) => {
    try {
        const newStudent = new Student({
            ...req.body,
            branch: req.branchId
        });
        await newStudent.save();
        res.status(201).json({ message: 'Student registered successfully' });
    } catch (err) {
        res.status(500).json({ error: 'Failed to register student' });
    }
});

// Get Students for logged-in branch
app.get('/api/students', authenticate, async (req, res) => {
    try {
        const students = await Student.find({ branch: req.branchId }).sort({ name: 1 });
        res.json(students);
    } catch (err) {
        res.status(500).json({ error: 'Failed to fetch students' });
    }
});

// --- DASHBOARD STATS ---
app.get('/api/stats', authenticate, async (req, res) => {
    try {
        const totalStudents = await Student.countDocuments({ branch: req.branchId });
        const activeLeads = await Lead.countDocuments({ branch: req.branchId, status: 'New' });
        const pendingFees = await Student.countDocuments({ branch: req.branchId, 'fees.status': 'Pending' });

        res.json({ totalStudents, activeLeads, pendingFees });
    } catch (err) {
        res.status(500).json({ error: 'Failed to fetch stats' });
    }
});

// --- PAGE NAVIGATION ---
// These help serve HTML files if you aren't using a purely static server approach
app.get('/dashboard', (req, res) => res.sendFile(path.join(__dirname, 'src', 'public', 'dashboard.html')));
app.get('/leads', (req, res) => res.sendFile(path.join(__dirname, 'src', 'public', 'leads.html')));
app.get('/students', (req, res) => res.sendFile(path.join(__dirname, 'src', 'public', 'students.html')));

// Start Server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`
    ●━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━●
      🚀 SCORPION ACADEMY CRM IS LIVE
      🔗 Local: http://localhost:${PORT}
      📂 Database: Local MongoDB (scorpion_academy)
    ●━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━●
    `);
});