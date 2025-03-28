const puppeteer = require("puppeteer");

let html = "";

process.stdin.on("data", (chunk) => {
    html += chunk;
});

process.stdin.on("end", async () => {
    const outputPath = process.argv[2];

    if (!html.trim()) {
        console.error("❌ Error: No HTML content received!");
        process.exit(1);
    }

    const browser = await puppeteer.launch({
        headless: "new",
    });

    const page = await browser.newPage();
    
    // Set content and wait for network requests to finish
    await page.setContent(html, { waitUntil: "networkidle0" });

    // Wait for images and fonts to load
    await page.evaluate(() => new Promise(resolve => setTimeout(resolve, 2000)));

    // Generate the PDF
    await page.pdf({
        path: outputPath,
        format: "A4",
        printBackground: true,
    });

    await browser.close();
});
