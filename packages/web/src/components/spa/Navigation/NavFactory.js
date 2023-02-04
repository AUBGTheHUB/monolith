class Props {
    constructor(
        anchorList,
        hasHackButton,
        bgColor,
        isSticky,
        mobileHeader = false,
        mobileBgColor = '#050328'
    ) {
        this.anchorList = anchorList;
        this.hasHackButton = hasHackButton;
        this.bgColor = bgColor;
        this.isSticky = isSticky;
        this.mobileHeader = mobileHeader;
        this.mobileBgColor = mobileBgColor;
    }
}

class Anchor {
    constructor(name, endpoint) {
        this.name = name;
        this.endpoint = endpoint;
    }
}

export { Props, Anchor };
