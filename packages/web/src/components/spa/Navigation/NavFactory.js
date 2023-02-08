class Props {
    constructor(
        anchorList,
        hasHackButton,
        bgColor,
        isSticky,
        mobileHeader = false,
        mobileBgColor = '#050328',
        anchorColor = 'white',
        anchorHoverColor = 'rgb(21, 76, 121)',
        mobileAnchorHoverColor = 'rgb(21, 76, 121)'
    ) {
        this.anchorList = anchorList;
        this.hasHackButton = hasHackButton;
        this.bgColor = bgColor;
        this.isSticky = isSticky;
        this.mobileHeader = mobileHeader;
        this.mobileBgColor = mobileBgColor;
        this.anchorColor = anchorColor;
        this.anchorHoverColor = anchorHoverColor;
        this.mobileAnchorHoverColor = mobileAnchorHoverColor;
    }
}

class Anchor {
    constructor(name, endpoint) {
        this.name = name;
        this.endpoint = endpoint;
    }
}

export { Props, Anchor };
