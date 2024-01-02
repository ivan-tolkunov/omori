const user = "ivan"
const url = "https://omori.tolkunov.dev/img?user=" + user
const refreshInterval = 1
const basepaintUrl = "https://basepaint-ponder-production.up.railway.app/"

const widget = await createWidget()
if (!config.runsInWidget) { WebView.loadURL(url) }
Script.setWidget(widget)
Script.complete()

async function createWidget() {
    let img = await new Request("https://omori.tolkunov.dev/img/get-img?user=" + user).loadImage()
    let widget = new ListWidget()
    widget.backgroundImage = img

    let interval = 1000 * 60 * refreshInterval
    widget.refreshAfterDate = new Date(Date.now() + interval)

    return widget
}
