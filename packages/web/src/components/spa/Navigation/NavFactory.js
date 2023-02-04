class Props {
    constructor(anchorList, hasHackButton, bgColor) {
        this.anchorList = anchorList;
        this.hasHackButton = hasHackButton;
        this.bgColor = bgColor;
    }
}

class Anchor {
    constructor(name, endpoint) {
        this.name = name;
        this.endpoint = endpoint;
    }
}

export { Props, Anchor };
