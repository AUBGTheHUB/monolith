class Props {
    constructor(
        anchorList,
        hasHackButton,
        bgColor,
        isSticky,
        mobileHeader = false,
        mobileBgColor = '#050328',
        anchorColor = 'white',
        specifyHack = '',
        // mobileAnchorHoverColor = 'rgb(21, 76, 121)',
    ) {
        this.anchorList = anchorList;
        this.hasHackButton = hasHackButton;
        this.bgColor = bgColor;
        this.isSticky = isSticky;
        this.mobileHeader = mobileHeader;
        this.mobileBgColor = mobileBgColor;
        this.anchorColor = anchorColor;
        this.specifyHack = specifyHack;
        // this.mobileAnchorHoverColor = mobileAnchorHoverColor;
    }
}

class Anchor {
    constructor(name, endpoint, icon = false, isLink = false, featureSwitch = true) {
        this.name = name;
        this.endpoint = endpoint;
        this.isLink = isLink;
        this.featureSwitch = featureSwitch;
        this.icon = icon;
    }
}

export { Props, Anchor };
