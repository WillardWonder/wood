const fs = require('fs');
const https = require('https');

// --- CONFIGURATION ---
const FRED_KEY = "ebbb8a10eb02bb0cec3c5c9fdaccb6ca";
const DATA_PATH = './public/intelligence.json';

// Helper: Simple Node.js fetch wrapper (avoiding extra dependencies)
const fetchJSON = (url) => {
    return new Promise((resolve, reject) => {
        https.get(url, (res) => {
            let data = '';
            res.on('data', (chunk) => data += chunk);
            res.on('end', () => {
                try {
                    resolve(JSON.parse(data));
                } catch (e) {
                    reject(e);
                }
            });
        }).on('error', reject);
    });
};

async function gatherIntelligence() {
    console.log("🌲 KRETZ INTELLIGENCE: Starting Data Harvest...");
    
    const packet = {
        updated: new Date().toISOString(),
        fred: [],
        comtrade: []
    };

    // 1. FETCH FRED (Hardwood Index)
    try {
        console.log(">> Contacting Federal Reserve...");
        const fredUrl = `https://api.stlouisfed.org/fred/series/observations?series_id=WPU081&api_key=${FRED_KEY}&file_type=json&limit=12&sort_order=desc`;
        const fredData = await fetchJSON(fredUrl);
        
        if (fredData.observations) {
            packet.fred = fredData.observations.reverse().map(o => ({
                date: o.date,
                value: parseFloat(o.value)
            }));
            console.log(`   ✅ FRED: Retrieved ${packet.fred.length} records.`);
        }
    } catch (err) {
        console.error("   ❌ FRED FAILURE:", err.message);
        // Fallback: Keep existing data if read fails? (Optional logic)
    }

    // 2. FETCH COMTRADE (China Exports)
    try {
        console.log(">> Contacting UN Comtrade...");
        // Using a slightly more robust public endpoint or fallback logic
        const comtradeUrl = 'https://comtradeapi.un.org/public/v1/preview/C/A/HS?max=5&reporterCode=842&period=2023,2024&partnerCode=156&cmdCode=440791&flowCode=X';
        const comtradeData = await fetchJSON(comtradeUrl);
        
        if (comtradeData.data) {
            packet.comtrade = comtradeData.data;
            console.log(`   ✅ COMTRADE: Retrieved ${packet.comtrade.length} records.`);
        }
    } catch (err) {
        console.error("   ❌ COMTRADE FAILURE:", err.message);
    }

    // 3. WRITE TO PUBLIC
    fs.writeFileSync(DATA_PATH, JSON.stringify(packet, null, 2));
    console.log("💾 Intelligence Packet Saved to " + DATA_PATH);
}

gatherIntelligence();
