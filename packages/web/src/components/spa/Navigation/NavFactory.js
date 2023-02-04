class Props {
    constructor(anchorList, hasHackButton, bgColor, isSticky) {
        this.anchorList = anchorList;
        this.hasHackButton = hasHackButton;
        this.bgColor = bgColor;
        this.isSticky = isSticky;
    }
}

class Anchor {
    constructor(name, endpoint) {
        this.name = name;
        this.endpoint = endpoint;
    }
}

export { Props, Anchor };
