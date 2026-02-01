import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

type JourneyTab = 'start' | 'gather' | 'hack' | 'finish';

const TAB_ORDER: Array<{ value: JourneyTab; label: string }> = [
    { value: 'start', label: 'START' },
    { value: 'gather', label: 'GATHER' },
    { value: 'hack', label: 'HACK' },
    { value: 'finish', label: 'FINISH' },
];

const CARD_TITLE = 'PRESENT AND WIN';
const CARD_BODY =
    'This is the home stretch! You have put in the work and now need to blow the judges\n' +
    'away!\n\n' +
    'Your task consists of creating a presentation for your product, as well as a Software\n' +
    'Demo.\n\n' +
    'After your presentation, there will be a Q&A session with the panel of judges.\n\n' +
    'The grading criteria for the project and presentation can be found below.\n\n' +
    'Make sure to check it, as it is extremely important!\n\n' +
    'If you have any more questions, check out the FAQ section at the end of the page!';

export const JourneySection = () => {
    return (
        <section
            className="relative overflow-hidden rounded-[32px]"
            style={{
                width: 1440,
                height: 780,
                backgroundColor: '#FFFDF5',
            }}
        >
            {/* Left hero image */}
            <img
                src="/Katniss.png"
                alt="Katniss Silhouette"
                className="pointer-events-none select-none absolute left-0 top-0 h-full"
                style={{ width: 715 }}
                draggable={false}
            />

            {/* Top-right logo */}
            <img
                src="/journey/mockingjay-red.svg"
                alt="Journey"
                className="pointer-events-none select-none absolute"
                style={{
                    top: 93,
                    right: 122,
                    height: 50,
                    width: 'auto',
                }}
                draggable={false}
            />

            <Tabs
                defaultValue="finish"
                className="absolute"
                style={{
                    left: 719,
                    top: 215,
                    width: 606,
                }}
            >
                {/* Buttons */}
                <TabsList className="flex w-full bg-transparent p-0" style={{ gap: 26, height: 48 }}>
                    {TAB_ORDER.map((t) => {
                        const isStart = t.value === 'start';
                        const bg =
                            t.value === 'gather'
                                ? '#E74018'
                                : t.value === 'hack'
                                  ? '#E43717'
                                  : t.value === 'finish'
                                    ? '#F88320'
                                    : 'transparent';

                        const color = isStart ? '#D01414' : '#FFFDF5';
                        const border = isStart ? '2px solid #D01414' : 'none';

                        return (
                            <TabsTrigger
                                key={t.value}
                                value={t.value}
                                className={[
                                    'm-0',
                                    'h-[48px] w-[132px]',
                                    'rounded-[12px]',
                                    'px-0',
                                    'shadow-none',
                                    'focus-visible:ring-0 focus-visible:ring-offset-0',
                                    'data-[state=active]:bg-transparent data-[state=active]:shadow-none',
                                ].join(' ')}
                                style={{
                                    backgroundColor: bg,
                                    border,
                                    color,
                                    fontFamily: 'Orbitron, ui-sans-serif, system-ui',
                                    fontSize: 18,
                                    letterSpacing: '0.12em',
                                    lineHeight: '18px',
                                    textTransform: 'uppercase',
                                }}
                            >
                                {t.label}
                            </TabsTrigger>
                        );
                    })}
                </TabsList>

                {/* Card panel (same content for all tabs for now) */}
                {TAB_ORDER.map((t) => (
                    <TabsContent key={t.value} value={t.value} className="m-0 p-0">
                        <Card
                            className="relative overflow-hidden"
                            style={{
                                marginTop: 24,
                                width: 606,
                                height: 334,
                                borderRadius: 18,
                                border: 'none',
                                boxShadow: '0px 10px 18px rgba(0,0,0,0.20)',
                                background: 'linear-gradient(90deg, #DE2515 0%, #F05F1B 55%, #FAA82A 100%)',
                            }}
                        >
                            {/* subtle vertical darkening */}
                            <div
                                className="absolute inset-0"
                                style={{
                                    background: 'linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.28) 100%)',
                                }}
                            />

                            <CardHeader
                                className="relative z-10"
                                style={{ paddingLeft: 24, paddingRight: 24, paddingTop: 22 }}
                            >
                                <CardTitle
                                    style={{
                                        fontFamily: 'Orbitron, ui-sans-serif, system-ui',
                                        fontSize: 24,
                                        lineHeight: '28px',
                                        color: '#FFFDF5',
                                        textTransform: 'uppercase',
                                    }}
                                >
                                    {CARD_TITLE}
                                </CardTitle>

                                {/* divider line */}
                                <div
                                    style={{
                                        marginTop: 12,
                                        height: 1,
                                        width: '100%',
                                        backgroundColor: 'rgba(255, 253, 245, 0.70)',
                                    }}
                                />
                            </CardHeader>

                            <CardContent
                                className="relative z-10"
                                style={{ paddingLeft: 24, paddingRight: 24, paddingTop: 0 }}
                            >
                                <CardDescription
                                    style={{
                                        whiteSpace: 'pre-line',
                                        fontFamily: 'oxanium',
                                        fontSize: 14,
                                        lineHeight: '19px',
                                        color: '#FFFDF5',
                                    }}
                                >
                                    {CARD_BODY}
                                </CardDescription>
                            </CardContent>
                        </Card>
                    </TabsContent>
                ))}
            </Tabs>
        </section>
    );
};
