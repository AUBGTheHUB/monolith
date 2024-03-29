import { Body, Container, Head, Html, Img, Link, Section, Text } from '@react-email/components';
import * as React from 'react';

export const ParticipantVerifyEmail = () => (
    <Html>
        <Head>
            <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono&display=swap" rel="stylesheet" />
        </Head>
        <Body style={main}>
            <Container style={container}>
                <Section style={styleForBackground}>
                    <Section style={styleForBackground2}>
                        <Section style={styleForBackground3}>
                            <Section style={sectionStyle}>
                                <Text style={title_team}>
                                    Welcome to HackAUBG 6.0, <br /> <br /> {`{participantName}`}, from team{' '}
                                    {`{teamName}`}!
                                </Text>
                                <Text style={title_no_team}>
                                    Welcome to HackAUBG 6.0, <br /> <br /> {`{participantName}`}!
                                </Text>
                                <br /> <br />
                                <Text style={paragraph}>
                                    Thank you for registering for our sixth{' '}
                                    <span style={highlight}> annual hackathon</span>!<br /> <br />
                                    We are extremely excited to have you on board and can't wait to see what{' '}
                                    <span style={highlight}> you'll create! </span>
                                    <br /> <br />
                                    Before your adventure at the hackathon starts,{' '}
                                    <span style={highlight}>you have to:</span>
                                </Text>
                                <br /> <br /> <br />
                                <div style={{ textAlign: 'center', paddingBottom: '50px' }}>
                                    <Link href="{verifyLink}" style={registerButton}>
                                        <h1 style={buttonText}>Verify</h1>
                                        <svg
                                            style={{ display: 'inline-block', verticalAlign: 'middle' }}
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
                                                    <stop stopColor="#fff" />
                                                    <stop offset="0.9999" stopColor="#fff" />
                                                    <stop offset="1" stopColor="white" stopOpacity="0" />
                                                </linearGradient>
                                            </defs>
                                        </svg>
                                    </Link>
                                </div>
                            </Section>
                        </Section>
                    </Section>
                </Section>
            </Container>
            <Img src={'https://s3-eu-central-1.amazonaws.com/hubarskibucket/moon-email.png'} width="100%" />
        </Body>
    </Html>
);

export default ParticipantVerifyEmail;

const main = {
    fontFamily: "'IBM Plex Mono', monospace",
    backgroundColor: '#000',
    backgroundImage: `url(https://s3-eu-central-1.amazonaws.com/hubarskibucket/email-background.png)`,
    margin: '0',
};

const title_no_team = {
    display: '{title_no_team}',
    fontFamily: "'IBM Plex Mono', monospace",
    color: '#FFFFFF',
    background: '#000',
    textAlign: 'center' as 'center',
    fontSize: '25px',
    paddingTop: '30px',
};

const title_team = {
    display: '{title_team}',
    fontFamily: "'IBM Plex Mono', monospace",
    color: '#FFFFFF',
    background: '#000',
    textAlign: 'center' as 'center',
    fontSize: '25px',
    paddingTop: '30px',
};

const container = {
    margin: '20px auto',
    color: '#FFFFFF',
    backgroundColor: 'rgba(0, 0, 0, 1.5)',
};

const sectionStyle = {
    width: '100%',
    textAlign: 'center' as 'center',
};

const paragraph = {
    fontSize: '22px',
    color: '#FFFFFF',
    lineHeight: '30px',
    textAlign: 'center' as 'center',
    textShadow: '0px 0px 8px rgba(0, 0, 0, 0.8)',
    marginTop: '20px',
    marginLeft: '10px',
    marginRight: '10px',
};

const highlight = {
    color: '#C298F3',
};

const registerButton = {
    display: 'inline-block',
    padding: '10px 0',
    border: '3px solid #fff',
    color: '#D8C2FB',
    textDecoration: 'none',
    width: '60%',
};

const buttonText = {
    paddingRight: '10px',
    fontSize: '35px',
    fontFamily: "'Press Start 2P'",
    display: 'inline-block',
    verticalAlign: 'middle',
    color: '#fff',
};

const styleForBackground = {
    background: '#000',
    backgroundImage: 'linear-gradient(#000,#000)',
    color: '#fff',
};

const styleForBackground2 = {
    background: '#000',
    mixBlendMode: 'screen' as 'screen',
};

const styleForBackground3 = {
    background: '#000',
    mixBlendMode: 'difference' as 'difference',
};
