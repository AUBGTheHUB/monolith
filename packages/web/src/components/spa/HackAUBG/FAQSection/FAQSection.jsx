import React from 'react';
import { FAQModule } from './FAQModule';
import './faq_section.css';

export const FAQSection = () => {
    return (
        <div className="faq-section" id="faq">
            <svg
                className="left-svg"
                width="385"
                height="619"
                viewBox="0 0 385 619"
                fill="none"
                xmlns="http://www.w3.org/2000/svg">
                <path
                    d="M-62.1147 100.499C-29.8748 -15.632 78.07 35.2938 133.544 109.453C167.159 150.64 224.175 119.404 265.795 170.463C307.416 221.522 207.452 243.831 270.139 323.62C332.826 403.408 209.855 518.529 137.837 477.529C65.8198 436.53 71.3366 471.601 -31.7675 482.455C-134.872 493.309 -210.063 347.282 -133.282 286.708C-56.501 226.134 -97.0149 226.212 -62.1147 100.499Z"
                    stroke="#1C1B1B"
                    strokeWidth="2.23917"
                />
                <path
                    d="M44.3282 269.733C46.8451 258.34 70.885 251.939 78.9174 265.637C86.2729 278.181 99.8352 280.826 105.598 287.907C120.769 306.548 111.411 305.992 115.075 319.526C119.533 335.996 108.631 365.588 84.3937 351.058C64.4596 339.107 64.6198 352.365 47.1212 347.706C29.6226 343.047 17.0724 325.596 28.598 306.371C32.9263 299.152 40.1362 288.708 44.3282 269.733Z"
                    stroke="#1C1B1B"
                    strokeWidth="2.23917"
                />
                <path
                    d="M-52.1498 115.399C-22.612 8.79001 77.7051 54.5042 128.866 123.167C160.094 161.75 213.16 133.594 251.52 180.655C290.736 228.767 199.009 248.998 256.331 322.763C313.724 396.795 200.941 504.141 133.267 465.547C65.9844 427.189 71.0143 460.277 -24.3075 469.72C-119.629 479.164 -189.126 344.826 -118.277 288.011C-48.083 232.287 -84.2583 231.409 -52.1498 115.399Z"
                    stroke="#1C1B1B"
                    strokeWidth="2.23917"
                />
                <path
                    d="M-42.1848 130.299C-15.3491 33.2113 77.3403 73.7139 124.189 136.88C153.029 172.859 202.145 147.784 237.245 190.847C274.056 236.012 190.567 254.163 242.522 321.906C294.622 390.182 192.027 489.752 128.697 453.565C66.1491 417.847 70.692 448.952 -16.8474 456.985C-104.387 465.018 -168.189 342.369 -103.273 289.313C-39.6649 238.44 -71.5017 236.605 -42.1848 130.299Z"
                    stroke="#1C1B1B"
                    strokeWidth="2.23917"
                />
                <path
                    d="M-32.2204 145.199C-8.08675 57.633 76.9749 92.9241 119.51 150.594C145.963 183.969 191.129 161.974 222.97 201.039C257.376 243.256 182.123 259.329 228.713 321.049C275.52 383.568 183.113 475.363 124.126 441.582C66.3133 408.505 70.3692 437.627 -9.38794 444.25C-89.1451 450.873 -147.253 339.913 -88.2685 290.616C-31.2473 244.593 -58.7456 241.802 -32.2204 145.199Z"
                    stroke="#1C1B1B"
                    strokeWidth="2.23917"
                />
                <path
                    d="M-22.2557 160.1C-0.824132 82.0553 76.6098 112.135 114.832 164.308C138.898 195.079 180.113 176.164 208.694 211.231C240.697 250.502 173.68 264.496 214.905 320.192C256.418 376.956 174.199 460.975 119.556 429.601C66.4777 399.164 70.0467 426.303 -1.92815 431.516C-73.903 436.729 -126.316 337.457 -73.2641 291.919C-22.8295 250.747 -45.9892 246.999 -22.2557 160.1Z"
                    stroke="#1C1B1B"
                    strokeWidth="2.23917"
                />
                <path
                    d="M-12.4907 175.334C6.23872 106.811 76.0449 131.679 109.955 178.356C131.633 206.523 168.898 190.688 194.219 221.757C223.817 258.081 165.038 269.996 200.896 319.669C237.116 370.677 165.085 446.921 114.786 417.953C66.4424 390.157 69.5244 415.313 5.33186 419.116C-58.8606 422.918 -105.579 335.335 -58.4594 293.556C-14.6114 257.234 -33.4327 252.53 -12.4907 175.334Z"
                    stroke="#1C1B1B"
                    strokeWidth="2.23917"
                />
                <path
                    d="M-2.96116 190.961C13.0662 131.96 75.2447 151.616 104.842 192.796C124.133 218.36 157.447 205.605 179.509 232.676C206.702 266.052 156.16 275.889 186.652 319.539C217.578 364.79 155.736 433.259 109.78 406.697C66.1717 381.543 68.7667 404.715 12.3565 407.108C-44.0537 409.5 -85.0773 333.606 -43.8901 295.586C-6.62871 264.114 -21.1114 258.453 -2.96116 190.961Z"
                    stroke="#1C1B1B"
                    strokeWidth="2.23917"
                />
                <path
                    d="M6.55553 206.611C19.8808 157.132 74.4316 171.576 99.7156 207.26C116.62 230.22 145.984 220.544 164.785 243.617C189.574 274.047 147.269 281.805 172.396 319.432C198.028 358.927 146.373 419.621 104.762 395.465C65.8881 372.951 67.9961 394.141 19.3682 395.123C-29.2596 396.105 -64.5885 331.9 -29.3336 297.638C1.34108 271.017 -8.80311 264.4 6.55553 206.611Z"
                    stroke="#1C1B1B"
                    strokeWidth="2.23917"
                />
                <path
                    d="M16.0541 222.291C26.6773 182.333 73.6004 191.567 94.5715 221.754C109.088 242.109 134.502 235.514 150.044 254.589C172.428 282.072 138.36 287.752 158.121 319.355C178.46 353.094 136.993 406.012 99.725 384.263C65.5864 364.39 67.2075 383.596 26.3619 383.168C-14.4836 382.74 -44.1179 330.223 -14.7953 299.721C9.29282 277.95 3.48715 270.376 16.0541 222.291Z"
                    stroke="#1C1B1B"
                    strokeWidth="2.23917"
                />
                <path
                    d="M25.5257 238.02C33.4468 207.584 72.7421 211.606 89.4003 236.297C101.53 254.048 122.993 250.533 135.275 265.61C155.255 290.146 129.424 293.746 143.819 319.327C158.864 347.309 127.586 392.452 94.6614 373.109C65.2577 355.877 66.3918 373.101 33.3286 371.262C0.265323 369.424 -23.6743 328.596 -0.283976 301.853C17.2175 284.932 15.7503 276.402 25.5257 238.02Z"
                    stroke="#1C1B1B"
                    strokeWidth="2.23917"
                />
                <path
                    d="M34.9573 253.82C40.1763 232.905 71.8439 231.715 84.1892 250.91C93.9318 266.058 111.445 265.622 120.467 276.701C138.042 298.29 120.448 299.812 129.477 319.37C139.229 341.596 118.139 378.964 89.5579 362.027C64.889 347.435 65.5361 362.676 40.2552 359.427C14.9743 356.179 -3.27062 327.039 14.1873 304.055C25.1022 291.985 27.9736 282.498 34.9573 253.82Z"
                    stroke="#1C1B1B"
                    strokeWidth="2.23917"
                />
            </svg>

            <svg
                className="right-svg"
                width="365"
                height="619"
                viewBox="0 0 365 619"
                fill="none"
                xmlns="http://www.w3.org/2000/svg">
                <path
                    d="M175.885 100.499C208.125 -15.632 316.07 35.2938 371.544 109.453C405.159 150.64 462.175 119.404 503.795 170.463C545.415 221.522 445.452 243.831 508.139 323.62C570.826 403.408 447.855 518.529 375.837 477.529C303.82 436.53 309.337 471.601 206.232 482.455C103.128 493.309 27.9367 347.282 104.718 286.708C181.499 226.134 140.985 226.212 175.885 100.499Z"
                    stroke="#1C1B1B"
                    strokeWidth="2.23917"
                />
                <path
                    d="M282.328 269.733C284.845 258.34 308.885 251.939 316.917 265.637C324.273 278.181 337.835 280.826 343.598 287.907C358.769 306.548 349.411 305.992 353.075 319.526C357.533 335.996 346.631 365.588 322.394 351.058C302.46 339.107 302.62 352.365 285.121 347.706C267.623 343.047 255.072 325.596 266.598 306.371C270.926 299.152 278.136 288.708 282.328 269.733Z"
                    stroke="#1C1B1B"
                    strokeWidth="2.23917"
                />
                <path
                    d="M185.85 115.399C215.388 8.79001 315.705 54.5042 366.866 123.167C398.093 161.75 451.16 133.594 489.52 180.655C528.736 228.767 437.009 248.998 494.33 322.763C551.724 396.795 438.941 504.141 371.267 465.547C303.984 427.189 309.014 460.277 213.692 469.72C118.371 479.164 48.8736 344.826 119.722 288.011C189.917 232.287 153.741 231.409 185.85 115.399Z"
                    stroke="#1C1B1B"
                    strokeWidth="2.23917"
                />
                <path
                    d="M195.815 130.299C222.651 33.2113 315.34 73.7139 362.189 136.88C391.029 172.859 440.145 147.784 475.245 190.847C512.056 236.012 428.566 254.163 480.522 321.906C532.622 390.182 430.027 489.752 366.697 453.565C304.149 417.847 308.692 448.952 221.152 456.985C133.613 465.018 69.8107 342.369 134.727 289.313C198.335 238.44 166.498 236.605 195.815 130.299Z"
                    stroke="#1C1B1B"
                    strokeWidth="2.23917"
                />
                <path
                    d="M205.779 145.199C229.913 57.633 314.975 92.9241 357.51 150.594C383.963 183.969 429.129 161.974 460.969 201.039C495.376 243.256 420.123 259.329 466.713 321.049C513.52 383.568 421.113 475.363 362.126 441.582C304.313 408.505 308.369 437.627 228.612 444.25C148.855 450.873 90.7471 339.913 149.731 290.616C206.752 244.593 179.254 241.802 205.779 145.199Z"
                    stroke="#1C1B1B"
                    strokeWidth="2.23917"
                />
                <path
                    d="M215.744 160.1C237.176 82.0553 314.61 112.135 352.832 164.308C376.898 195.079 418.113 176.164 446.694 211.231C478.696 250.502 411.68 264.496 452.904 320.192C494.418 376.956 412.199 460.975 357.556 429.601C304.478 399.164 308.047 426.303 236.072 431.516C164.097 436.729 111.684 337.457 164.736 291.919C215.17 250.747 192.011 246.999 215.744 160.1Z"
                    stroke="#1C1B1B"
                    strokeWidth="2.23917"
                />
                <path
                    d="M225.509 175.334C244.239 106.811 314.045 131.679 347.955 178.356C369.633 206.523 406.898 190.688 432.219 221.757C461.817 258.081 403.038 269.996 438.896 319.669C475.116 370.677 403.085 446.921 352.786 417.953C304.442 390.157 307.524 415.313 243.332 419.116C179.139 422.918 132.421 335.335 179.541 293.556C223.389 257.234 204.567 252.53 225.509 175.334Z"
                    stroke="#1C1B1B"
                    strokeWidth="2.23917"
                />
                <path
                    d="M235.039 190.961C251.066 131.96 313.245 151.616 342.841 192.796C362.133 218.36 395.447 205.605 417.509 232.676C444.702 266.052 394.16 275.889 424.652 319.539C455.578 364.79 393.736 433.259 347.78 406.697C304.172 381.543 306.767 404.715 250.356 407.108C193.946 409.5 152.923 333.606 194.11 295.586C231.371 264.114 216.888 258.453 235.039 190.961Z"
                    stroke="#1C1B1B"
                    strokeWidth="2.23917"
                />
                <path
                    d="M244.556 206.611C257.881 157.132 312.432 171.576 337.716 207.26C354.62 230.22 383.984 220.544 402.785 243.617C427.574 274.047 385.269 281.805 410.396 319.432C436.028 358.927 384.373 419.621 342.762 395.465C303.888 372.951 305.996 394.141 257.368 395.123C208.74 396.105 173.411 331.9 208.666 297.638C239.341 271.017 229.197 264.4 244.556 206.611Z"
                    stroke="#1C1B1B"
                    strokeWidth="2.23917"
                />
                <path
                    d="M254.054 222.291C264.677 182.333 311.6 191.567 332.571 221.754C347.088 242.109 372.502 235.514 388.044 254.589C410.428 282.072 376.36 287.752 396.121 319.355C416.46 353.094 374.993 406.012 337.725 384.263C303.586 364.39 305.207 383.596 264.362 383.168C223.516 382.74 193.882 330.223 223.205 299.721C247.293 277.95 241.487 270.376 254.054 222.291Z"
                    stroke="#1C1B1B"
                    strokeWidth="2.23917"
                />
                <path
                    d="M263.525 238.02C271.447 207.584 310.742 211.606 327.4 236.297C339.53 254.048 360.993 250.533 373.275 265.61C393.255 290.146 367.424 293.746 381.819 319.327C396.864 347.309 365.586 392.452 332.661 373.109C303.257 355.877 304.392 373.101 271.328 371.262C238.265 369.424 214.326 328.596 237.716 301.853C255.217 284.932 253.75 276.402 263.525 238.02Z"
                    stroke="#1C1B1B"
                    strokeWidth="2.23917"
                />
                <path
                    d="M272.957 253.82C278.176 232.905 309.844 231.715 322.189 250.91C331.932 266.058 349.444 265.622 358.467 276.701C376.042 298.29 358.448 299.812 367.477 319.37C377.229 341.596 356.139 378.964 327.558 362.027C302.889 347.435 303.536 362.676 278.255 359.427C252.974 356.179 234.729 327.039 252.187 304.055C263.102 291.985 265.973 282.498 272.957 253.82Z"
                    stroke="#1C1B1B"
                    strokeWidth="2.23917"
                />
            </svg>

            <h1 className="faq-h1">FREQUENTLY ASKED QUESTIONS</h1>
            <div className="faq">
                <FAQModule
                    title={`Gather a team and register`}
                    text={`Gather your dream team and register in the form
                            below! Don’t forget to create a diverse team, as the
                            best teams usually incorporate programmers, business
                            planners, and designers. The teams should be between
                            4 and 6 people. However, if you have less, don’t
                            worry! Organizers from the Hub will add you to the
                            best suited team for you. Don’t procrastinate
                            registering, because if the registered teams become
                            more than 12, your team will be waitlisted until the
                            very last week before the competition.`}></FAQModule>
                <FAQModule
                    title={`Gather a team and register`}
                    text={`Gather your dream team and register in the form
                            below! Don’t forget to create a diverse team, as the
                            best teams usually incorporate programmers, business
                            planners, and designers. The teams should be between
                            4 and 6 people. However, if you have less, don’t
                            worry! Organizers from the Hub will add you to the
                            best suited team for you. Don’t procrastinate
                            registering, because if the registered teams become
                            more than 12, your team will be waitlisted until the
                            very last week before the competition.`}
                    border={'faq-hide-border'}></FAQModule>
                <FAQModule
                    title={`Gather a team and register`}
                    text={`Gather your dream team and register in the form
                            below! Don’t forget to create a diverse team, as the
                            best teams usually incorporate programmers, business
                            planners, and designers. The teams should be between
                            4 and 6 people. However, if you have less, don’t
                            worry! Organizers from the Hub will add you to the
                            best suited team for you. Don’t procrastinate
                            registering, because if the registered teams become
                            more than 12, your team will be waitlisted until the
                            very last week before the competition.`}></FAQModule>
                <FAQModule
                    title={`Gather a team and register`}
                    text={`Gather your dream team and register in the form
                            below! Don’t forget to create a diverse team, as the
                            best teams usually incorporate programmers, business
                            planners, and designers. The teams should be between
                            4 and 6 people. However, if you have less, don’t
                            worry! Organizers from the Hub will add you to the
                            best suited team for you. Don’t procrastinate
                            registering, because if the registered teams become
                            more than 12, your team will be waitlisted until the
                            very last week before the competition.`}></FAQModule>
                <FAQModule
                    title={`Gather a team and register`}
                    text={`Gather your dream team and register in the form
                            below! Don’t forget to create a diverse team, as the
                            best teams usually incorporate programmers, business
                            planners, and designers. The teams should be between
                            4 and 6 people. However, if you have less, don’t
                            worry! Organizers from the Hub will add you to the
                            best suited team for you. Don’t procrastinate
                            registering, because if the registered teams become
                            more than 12, your team will be waitlisted until the
                            very last week before the competition.`}></FAQModule>
                <FAQModule
                    title={`Gather a team and register`}
                    text={`Gather your dream team and register in the form
                            below! Don’t forget to create a diverse team, as the
                            best teams usually incorporate programmers, business
                            planners, and designers. The teams should be between
                            4 and 6 people. However, if you have less, don’t
                            worry! Organizers from the Hub will add you to the
                            best suited team for you. Don’t procrastinate
                            registering, because if the registered teams become
                            more than 12, your team will be waitlisted until the
                            very last week before the competition.`}></FAQModule>
            </div>
        </div>
    );
};
