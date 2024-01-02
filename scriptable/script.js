const refreshInterval = 1
const basepaintUrl = "https://basepaint-ponder-production.up.railway.app/"

const widget = await createWidget()
if (!config.runsInWidget) { await widget.presentMedium() }
Script.setWidget(widget)
Script.complete()

async function createWidget() {

    let widget = new ListWidget()
    let selection = await getLatestCanvas()
    widget.backgroundImage = selection.image
    widget.addSpacer()

    let interval = 1000 * 60 * refreshInterval
    widget.refreshAfterDate = new Date(Date.now() + interval)
    
    widget.url = selection.url

    return widget

}

async function getLatestCanvas() {
    try {
        let img = await new Request("https://omori.tolkunov.dev/img/get-img?user=ivan").loadImage()
        return {
            image: img, 
            title: "",
            url: "https://omori.tolkunov.dev/img?user=ivan"
        }
    } catch (e) {
        console.error(e)
        return null
    }

}