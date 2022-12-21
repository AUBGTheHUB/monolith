class Props {
    constructor(anchorList, hasHackButton) {
        this.anchorList = anchorList;
        this.hasHackButton = hasHackButton;
    }
}

class Anchor {
    constructor(name, endpoint) {
        this.name = name;
        this.endpoint = endpoint;
    }
}

export { Props, Anchor };
