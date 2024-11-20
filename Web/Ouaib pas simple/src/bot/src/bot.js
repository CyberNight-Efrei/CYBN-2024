import chalk from "chalk"
import puppeteer from "puppeteer";

import onNewTargetCreated from "./utils.js";
chalk.level = 3

const TIMEOUT = 5000

console.log("==========\nconsole.log, warn & error seront affichés ici.\n==========")


async function goto(url) {
    console.log(chalk.underline("\nLancement du navigateur..."))

    const browser = await puppeteer.launch({
        headless: "new",
        ignoreHTTPSErrors: true,
        args: [
            "--no-sandbox",
            "--incognito",
            "--disable-gpu",
            "--disable-jit",
            "--disable-wasm",
            "--disable-dev-shm-usage"
        ],
        executablePath: "/usr/bin/chromium"
    })

    const page = await browser.newPage()
    await page.setDefaultNavigationTimeout(TIMEOUT)

    browser.on("targetcreated", onNewTargetCreated)

    try {
        const parsedUrl = new URL(url);

        await page.goto(`${parsedUrl.origin}/wp-login.php`);

        await page.type('#user_login', 'ouaib');
        await page.type('#user_pass', '346a5fba02ac21433c143ecb988353e7');

        await page.click('#wp-submit');

        await page.waitForNavigation();

        const currentUrl = page.url();

        if (currentUrl.includes('wp-admin')) {
            console.log('Ready to visit');
        } else {
            console.log('Contact admin');
        }

        const xss_page = await browser.newPage()
        await xss_page.goto(url)

        await xss_page.evaluate(() => {
            const el = document.querySelector("[autofocus]")
            console.log(el)
            if (el) el.focus()
        })
    } catch {}

    await new Promise(resolve => setTimeout(resolve, TIMEOUT))

    console.log(chalk.underline("\nVisite terminée !"))

    return browser.close()
}

process.stdin.on("data", data => {
    const url = data.toString().trim()

    if (!url || !(url.toLowerCase().startsWith("http://") || url.toLowerCase().startsWith("https://"))) {
        console.log("[ERROR] URL invalide !")
        process.exit(1)
    }

    goto(url).then(() => process.exit(0))
})