import chalk from "chalk"
chalk.level = 3

const withColor = message => {
    const type = message.type()

    let log = chalk.grey

    switch (type) {
        case "log":
            log = chalk.blue
            break
        case "warn":
            log = chalk.yellow
            break
        case "error":
            log = chalk.red
            break
    }

    return log(`console.${type} > ${message.text()}`)
}

const withPrefix = async (tabId, page) => {
    let title = ""
    try {
        title = await page.title()
    } catch {}

    let url = ""
    try {
        url = await page.url()
    } catch {}

    return chalk.bold(`[Tab ${tabId} - ${title} | (${url})]> `)
}

const initPageListeners = async (page, tabId) => {
    page.on("console", async message => {
        console.log(
            await withPrefix(tabId, page) + withColor(message)
        )
    })

    page.on("framenavigated", async frame => {
        if (frame === page.mainFrame()) {
            console.log(
                await withPrefix(tabId, page) + chalk.blue("Navigating") + ` > ${frame.url()}`
            )
        }
    })
}

const initWorkerListeners = async (worker, swId) => {
    worker.client.on("Runtime.consoleAPICalled", args => {
        const message = {
            type: args.type,
            text: () => args.args[0].value
        }

        console.log(
            chalk.bold(`[SW ${swId}]> `) + withColor(message)
        )
    })
}

let tabCounter = 0
let serviceWorkerCounter = 0

const onNewTargetCreated = async target => {
    try {
        if (target.type() === "page") {
            tabCounter++

            console.log(
                chalk.bold(`[Tab ${tabCounter} (${target.url()})]> `) + chalk.grey("Nouvel onglet detecté!")
            )

            await initPageListeners(await target.page(), tabCounter)
        } else if (target.type() === "service_worker") {
            serviceWorkerCounter++

            console.log(
                chalk.bold(`[SW ${serviceWorkerCounter} (${target.url()})]> `) + chalk.grey("New Service Worker detected!")
            )

            await initWorkerListeners(await target.worker(), serviceWorkerCounter)
        }
    } catch {
        console.log(chalk.red.underline.bold("\nErreur imprévue, contactez un admin si cette erreur vous bloque dans votre payload."))
    }
}


export default onNewTargetCreated