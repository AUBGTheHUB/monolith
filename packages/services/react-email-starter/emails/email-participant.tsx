import { Body, Container, Head, Html, Img, Section, Text, Link } from '@react-email/components';
import * as React from 'react';

export const ParticipantWelcomeEmail = () => (
    <Html>
        <Head>
            <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono&display=swap" rel="stylesheet" />
            <meta name="color-scheme" content="light"></meta>
            <meta name="supported-color-schemes" content="light"></meta>
        </Head>
        <Body style={main}>
            <Container style={container}>
                <Section style={removeDots}>
                    <Section style={styleForBackground}>
                        <Section style={styleForBackground2}>
                            <Text style={title_team}>
                                Welcome to HackAUBG 6.0, <br /> <br /> {`{participantName}`}, from team {`{teamName}`}!
                            </Text>
                            <Text style={title_no_team}>
                                Welcome to HackAUBG 6.0, <br /> <br /> {`{participantName}`}!
                            </Text>
                            <br /> <br />
                            <Text style={paragraph as React.CSSProperties}>
                                Before the hackathon starts, there are a few{' '}
                                <span style={highlight}>important things:</span>
                            </Text>
                            <Text style={paragraph_invite as React.CSSProperties}>
                                Here is the invite link, so you can invite your teammates to join: <br />
                            </Text>
                            <Text style={aaa}>
                                <Link href="{inviteLink}" style={inv_link as React.CSSProperties}>
                                    {`{inviteLink}`}
                                </Link>
                            </Text>
                            <Text style={paragraph as React.CSSProperties}>
                                To ensure you stay in the loop, we will invite you to join the Official HackAUBG 6.0
                                Facebook group. That is where we'll share all the latest updates and instructions about
                                the event.
                            </Text>
                            <Text style={paragraph as React.CSSProperties}>
                                What's more, each team will have their very own{' '}
                                <span style={highlight}>facilitator</span> from The Hub to guide you through the
                                hackathon. They'll be your point of contact for any questions or concerns you may have
                                and will even help you find new teammates if needed.
                            </Text>
                            <Text style={paragraph as React.CSSProperties}>
                                Make sure to follow our social media accounts for updates about the event and exciting
                                upcoming surpises -{' '}
                                <Link href="https://www.facebook.com/TheHubAUBG" style={highlight}>
                                    Facebook
                                </Link>
                                ,{' '}
                                <Link href="https://www.instagram.com/thehubaubg/" style={highlight}>
                                    Instagram
                                </Link>{' '}
                                and{' '}
                                <Link href="https://www.linkedin.com/company/the-hub-aubg/mycompany/" style={highlight}>
                                    Linkedin
                                </Link>
                            </Text>
                            <Text style={paragraph as React.CSSProperties}>
                                We're thrilled to have you on board and can't wait to meet you!
                            </Text>
                            <Text style={paragraph_last as React.CSSProperties}>
                                <span style={highlight}>See you soon! - The Hub AUBG</span>
                            </Text>
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

export default ParticipantWelcomeEmail;

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
    margin: '0 auto',
    padding: '20px 0 48px',
};

const paragraph = {
    fontSize: '16px',
    color: '#FFFFFF',
    lineHeight: '24px',
    textAlign: 'center',
    textShadow: '0px 0px 8px rgba(0, 0, 0, 0.8)',
    marginLeft: '3px',
    marginRight: '3px',
};

const paragraph_invite = {
    display: '{inviteLinkVisibility}',
    fontSize: '16px',
    color: '#FFFFFF',
    lineHeight: '24px',
    textAlign: 'center',
    textShadow: '0px 0px 8px rgba(0, 0, 0, 0.8)',
    marginLeft: '3px',
    marginRight: '3px',
};

const paragraph_last = {
    fontSize: '16px',
    color: '#FFFFFF',
    lineHeight: '24px',
    textAlign: 'center',
    textShadow: '0px 0px 8px rgba(0, 0, 0, 0.8)',
    marginBottom: '25px',
    marginLeft: '3px',
    marginRight: '3px',
};

const removeDots = {
    background: '#000',
    backgroundImage: 'linear-gradient(#000,#000)',
    color: '#fff',
};

const styleForBackground = {
    background: '#000',
    mixBlendMode: 'normal' as 'normal',
};

const styleForBackground2 = {
    background: '#000',
    mixBlendMode: 'difference' as 'difference',
};

const highlight = {
    color: '#C298F3',
};

const inv_link = {
    color: '#fff',
    textDecoration: 'underline',
    wordBreak: 'break-all',
    textAlign: 'center',
};

const aaa = {
    textAlign: 'center',
    marginLeft: '3px',
    marginRight: '3px',
    fontSize: '12px',
};
