const user = "ivan"
const url = "https://omori.tolkunov.dev/img?user=" + user
const refreshInterval = 1

const widget = await createWidget()
if (!config.runsInWidget) { WebView.loadURL(url) }
Script.setWidget(widget)
Script.complete()

const reactions = new Map();
reactions.set("heart", "🥰")
reactions.set("poop", "💩")
reactions.set("stone", "🗿")
reactions.set("lol", "😂")

async function createWidget() {
    let img = await new Request("https://omori.tolkunov.dev/img/get-img?user=" + user).loadImage()
    let notifications = await new Request("https://omori.tolkunov.dev/img/get-reactions?user=" + user).loadJSON()
    let widget = new ListWidget()
    widget.backgroundImage = img
    await createNotification(notifications)

    let interval = 1000 * 60 * refreshInterval
    widget.refreshAfterDate = new Date(Date.now() + interval)

    return widget
}

async function createNotification(notifications) {
    if (notifications.length > 0) {
        for (let notification of notifications) {
            let n = new Notification()
            n.title = "Wow!"
            n.body = reactions.get(notification)
            n.schedule()
        }
    }
}