require('dotenv').config();
const mongoose = require('mongoose');
const Branch = require('./src/models/Branch');

// LOCAL CONNECTION STRING
const directUri = "mongodb://127.0.0.1:27017/scorpion_academy";

async function seed() {
    try {
        console.log("Connecting to LOCAL MongoDB...");
        await mongoose.connect(directUri);
        console.log("✅ Connected!");

        // Clear existing branches to avoid duplicates during testing (Optional)
        await Branch.deleteMany({ slug: "coimbatore-main" });

        await Branch.create({
            name: "Scorpion Academy",
            slug: "coimbatore-main",
            password: "dojo123", 
            instructor: "Sensei Kumar"
        });

        console.log("✅ Branch Created! Login: coimbatore-main / dojo123");
    } catch (err) {
        console.error("❌ Error:", err);
    } finally {
        await mongoose.connection.close();
        process.exit();
    }
}

seed();