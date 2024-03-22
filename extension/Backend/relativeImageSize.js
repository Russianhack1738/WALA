const puppeteer = require('puppeteer');

async function getEffectiveImageSizes(webpageUrl, screenWidth, screenHeight) {
    try {
        const browser = await puppeteer.launch();
        const page = await browser.newPage();

        await page.setViewport({ width: screenWidth, height: screenHeight });
        await page.goto(webpageUrl, { waitUntil: 'networkidle2' });

        const imageData = await page.evaluate(() => {
            const images = Array.from(document.querySelectorAll('img'));
            return images
                .filter(img => img.width >= 100 && img.height >= 100)
                .map(img => ({ url: img.src, width: img.width, height: img.height }));
        });

        await browser.close();

        return imageData;
    } catch (error) {
        console.error(`Error getting image sizes for ${webpageUrl}: ${error}`);
        return [];
    }
}

// Extract command line arguments
const [webpageUrl, screenWidth, screenHeight] = process.argv.slice(2).map(arg => arg.trim());

// Run the function and print the result as JSON
getEffectiveImageSizes(webpageUrl, parseInt(screenWidth), parseInt(screenHeight))
    .then(imageData => console.log(JSON.stringify(imageData)))
    .catch(error => console.error(error));
