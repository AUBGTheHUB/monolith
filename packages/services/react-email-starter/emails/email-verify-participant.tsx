import { Body, Container, Head, Html, Img, Section, Text } from '@react-email/components';
import * as React from 'react';

export const ParticipantVerifyEmail = () => (
    <Html>
        <Head>
            <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono&display=swap" rel="stylesheet" />
        </Head>
        <Body style={main}>
            <Container style={container}>
                <Section style={test1}>
                    <Section style={test2}>
                        <Section style={test3}>
                            <Section style={sectionStyle}>
                                <Text style={title}>
                                    Welcome to HackAUBG 6.0, <br /> <br /> {`{participantName}`}
                                </Text>
                                <br /> <br />
                                <Text style={paragraph as React.CSSProperties}>
                                    Before your adventure at the hackathon starts,{' '}
                                    <span style={highlight}>you have to:</span>
                                </Text>
                                <br /> <br /> <br />
                                <a href="{verifyLink}" style={registerButton}>
                                    <h1 style={buttonText}>Verify</h1>
                                    <svg
                                        width="20"
                                        height="25"
                                        viewBox="0 0 20 25"
                                        fill="none"
                                        xmlns="http://www.w3.org/2000/svg">
                                        <path
                                            fillRule="evenodd"
                                            clipRule="evenodd"
                                            d="M1.92298 25L1.92298 23.4042L4.23071 23.4042L4.23072 21.8087L6.53845 21.8087L6.53845 20.2128L8.84619 20.2128L8.84619 18.6173L11.1538 18.6173L11.1538 17.2873L13.4615 17.2873L13.4615 15.9575L15.7692 15.9575L15.7692 14.628L18.0769 14.628L18.0769 13.298L20 13.298L20 11.7022L18.0769 11.7022L18.0769 10.3722L15.7693 10.3722L15.7693 9.04297L13.4615 9.04297L13.4615 7.71297L11.1539 7.71297L11.1539 6.38321L8.84619 6.38321L8.84619 4.78741L6.53845 4.78741L6.53845 3.19185L4.23071 3.19185L4.23071 1.59605L1.92297 1.59604L1.92297 5.75475e-05L7.90761e-06 5.73794e-05L5.72205e-06 25L1.92298 25Z"
                                            fill="url(#paint0_linear_76_9313)"
                                        />
                                        <defs>
                                            <linearGradient
                                                id="paint0_linear_76_9313"
                                                x1="10"
                                                y1="25"
                                                x2="10"
                                                y2="0.000205119"
                                                gradientUnits="userSpaceOnUse">
                                                <stop stopColor="#d8c2fb" />
                                                <stop offset="0.9999" stopColor="#d8c2fb" />
                                                <stop offset="1" stopColor="white" stopOpacity="0" />
                                            </linearGradient>
                                        </defs>
                                    </svg>
                                </a>
                            </Section>
                        </Section>
                    </Section>
                </Section>
            </Container>
            <Img
                src={'https://s3-eu-central-1.amazonaws.com/hubarskibucket/moon-email.png'}
                width="100%"
                height="auto"
            />
        </Body>
    </Html>
);

export default ParticipantVerifyEmail;

const main = {
    fontFamily: "'IBM Plex Mono', monospace",
    backgroundImage: `url(https://s3-eu-central-1.amazonaws.com/hubarskibucket/email-background.png)`,
    backgroundColor: '#fff',
    margin: '0',
    display: 'flex',
    flexDirection: 'column' as 'column',
    justifyContent: 'space-between',
    minHeight: '100vh',
};

const title = {
    fontFamily: "'IBM Plex Mono', monospace",
    color: '#FFFFFF',
    textAlign: 'center' as 'center',
    fontSize: '25px',
};

const container = {
    display: 'flex',
    justifyContent: 'center',
    margin: '0 auto',
    padding: '20px 0 48px',
    color: '#FFFFFF',
    backgroundColor: 'rgba(0, 0, 0, 1.5)',
};

const sectionStyle = {
    display: 'flex',
    flexDirection: 'column' as 'column',
    justifyContent: 'center',
    alignItems: 'center',
    width: '100%',
    textAlign: 'center' as 'center',
};

const paragraph = {
    fontSize: '22px',
    color: '#FFFFFF',
    lineHeight: '24px',
    textAlign: 'center',
    textShadow: '0px 0px 8px rgba(0, 0, 0, 0.8)',
    marginTop: '60px',
};

const highlight = {
    color: '#C298F3',
};

const registerButton = {
    display: 'inline-flex',
    alignItems: 'center',
    alignSelf: 'center',
    justifyContent: 'center',
    padding: '25px 10px',
    border: '3px solid #D8C2FB',
    color: '#D8C2FB',
    textDecoration: 'none',
    width: '80%',
};

const buttonText = {
    paddingRight: '10px',
    fontSize: '35px',
    fontFamily: "'Press Start 2P'",
};

const test1 = {
    background: '#000',
    backgroundImage: 'linear-gradient(#000,#000)',
    color: '#fff',
};

const test2 = {
    background: '#000',
    mixBlendMode: 'screen',
};

const test3 = {
    background: '#000',
    mixBlendMode: 'difference',
};
