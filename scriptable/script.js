const user = "ivan"
const url = "https://omori.onrender.com/img?user=" + user
const refreshInterval = 1

const widget = await createWidget()
if (!config.runsInWidget) { WebView.loadURL(url) }
Script.setWidget(widget)
Script.complete()

async function createWidget() {
    let img = await new Request("https://omori.onrender.com/img/get-img?user=" + user).loadImage()
    // let notifications = await new Request("https://omori.onrender.com/img/get-reactions?user=" + user).loadJSON()
    let widget = new ListWidget()
    widget.backgroundImage = img
    // await createNotification(notifications)

    let interval = 1000 * 60 * refreshInterval
    widget.refreshAfterDate = new Date(Date.now() + interval)

    return widget
}

async function createNotification(notifications) {
    const reactions = {
        "heart": "🥰",
        "poop": "💩",
        "stone": "🗿",
        "lol": "😂",
    }
    for (let notification of notifications) {
        let n = new Notification()
        n.title = "Wow!"
        n.body = reactions[notification]
        await n.schedule()
    }
}
