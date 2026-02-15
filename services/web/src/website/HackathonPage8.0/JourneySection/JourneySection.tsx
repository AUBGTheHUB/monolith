import { useMemo, useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

import journeyTabsRaw from './StaticContent/journeyTabs.json';

type JourneyTab = 'start' | 'gather' | 'hack' | 'finish';

type JourneyTabEntry = {
    value: JourneyTab;
    label: string;
    title: string;
    body: string;
};

const triggerBase = [
    'flex items-center justify-center',
    'h-[48px] rounded-[12px] px-0',
    'shadow-none transition-all duration-200',
    'focus-visible:ring-0 focus-visible:ring-offset-0',
    // active feel
    'data-[state=active]:shadow-[0_10px_18px_rgba(0,0,0,0.20)]',
    'data-[state=active]:-translate-y-[1px]',
].join(' ');

const triggerTextStyle: React.CSSProperties = {
    fontFamily: 'oxanium, ui-sans-serif, system-ui',
    fontSize: 24,
    letterSpacing: '0.12em',
    lineHeight: '24px',
    textTransform: 'uppercase',
};

export const JourneySection = () => {
    const tabs = useMemo(() => journeyTabsRaw as JourneyTabEntry[], []);
    const [activeTab, setActiveTab] = useState<JourneyTab>('finish');

    const handleTabChange = (value: string) => setActiveTab(value as JourneyTab);

    return (
        <section className="w-full">
            <div className="relative w-full overflow-hidden rounded-[32px] bg-[#FFFDF5]">
                <div className="relative z-10 mx-auto flex w-full max-w-[1440px] flex-col lg:flex-row">
                    {/* LEFT VISUAL */}
                    <div className="relative w-full lg:w-[55%]">
                        <div className="relative h-[360px] sm:h-[460px] lg:h-[780px]">
                            {/* flames: move LEFT + DOWN */}
                            <img
                                src="/flames.png"
                                alt=""
                                className={[
                                    'pointer-events-none select-none absolute',
                                    // mobile shift
                                    'left-[-60px] bottom-[-20px] w-[130%] max-w-none',
                                    // desktop shift (more left + more down)
                                    'lg:left-[-140px] lg:bottom-[-70px] lg:w-[135%]',
                                ].join(' ')}
                                draggable={false}
                            />

                            {/* Katniss: move LEFT + DOWN */}
                            <img
                                src="/Katniss.png"
                                alt="Katniss Silhouette"
                                className={[
                                    'pointer-events-none select-none absolute w-auto',
                                    // mobile shift
                                    'left-[-30px] bottom-[-10px] h-full',
                                    // desktop shift (more left + more down)
                                    'lg:left-[-90px] lg:bottom-[-40px]',
                                ].join(' ')}
                                style={{ maxWidth: 'none' }}
                                draggable={false}
                            />
                        </div>
                    </div>

                    {/* RIGHT CONTENT */}
                    <div className="flex w-full flex-col px-4 pb-10 pt-8 sm:px-8 sm:pt-10 lg:w-[45%] lg:items-end lg:justify-center lg:px-0 lg:pb-0 lg:pt-0">
                        {/* Shift everything RIGHT on desktop */}
                        <div className="w-full lg:max-w-[606px] lg:pr-[150px]">
                            {/* JOURNEY header: TEXT LEFT of SVG, and move right */}
                            <div className="mb-6 flex items-center justify-center gap-4 lg:mb-10 lg:justify-end">
                                <div
                                    className="text-[#D01414]"
                                    style={{
                                        fontFamily: 'Orbitron, ui-sans-serif, system-ui',
                                        fontSize: 40,
                                        letterSpacing: '0.32em',
                                        lineHeight: '28px',
                                        textTransform: 'uppercase',
                                    }}
                                >
                                    JOURNEY
                                </div>

                                <img
                                    src="/mockingjay-red.svg"
                                    alt=""
                                    className="h-[34px] w-auto sm:h-[40px] lg:h-[44px]"
                                    draggable={false}
                                />
                            </div>

                            <Tabs value={activeTab} onValueChange={handleTabChange} className="w-full">
                                {/* Triggers */}
                                <TabsList className="grid w-full grid-cols-2 gap-3 bg-transparent p-0 sm:flex sm:flex-row sm:gap-4 lg:gap-[26px]">
                                    {/* START */}
                                    <TabsTrigger
                                        value="start"
                                        className={[
                                            triggerBase,
                                            'w-full sm:w-[132px]',
                                            'border-2 border-[#D01414]',
                                            // inactive
                                            'data-[state=inactive]:bg-[#E74018] data-[state=inactive]:text-[#FFFDF5]',
                                            // active: button white
                                            'data-[state=active]:bg-[#FFFDF5] data-[state=active]:text-[#D01414]',
                                        ].join(' ')}
                                        style={triggerTextStyle}
                                    >
                                        START
                                    </TabsTrigger>

                                    {/* GATHER */}
                                    <TabsTrigger
                                        value="gather"
                                        className={[
                                            triggerBase,
                                            'w-full sm:w-[132px]',
                                            // inactive colored
                                            'data-[state=inactive]:bg-[#E74018] data-[state=inactive]:text-[#FFFDF5]',
                                            // active white
                                            'data-[state=active]:bg-[#FFFDF5] data-[state=active]:text-[#D01414] border-2 border-[#D01414]',
                                        ].join(' ')}
                                        style={triggerTextStyle}
                                    >
                                        GATHER
                                    </TabsTrigger>

                                    {/* HACK */}
                                    <TabsTrigger
                                        value="hack"
                                        className={[
                                            triggerBase,
                                            'w-full sm:w-[132px]',
                                            'data-[state=inactive]:bg-[#E43717] data-[state=inactive]:text-[#FFFDF5]',
                                            'data-[state=active]:bg-[#FFFDF5] data-[state=active]:text-[#D01414] border-2 border-[#D01414]',
                                        ].join(' ')}
                                        style={triggerTextStyle}
                                    >
                                        HACK
                                    </TabsTrigger>

                                    {/* FINISH */}
                                    <TabsTrigger
                                        value="finish"
                                        className={[
                                            triggerBase,
                                            'w-full sm:w-[132px]',
                                            'data-[state=inactive]:bg-[#F88320] data-[state=inactive]:text-[#FFFDF5]',
                                            'data-[state=active]:bg-[#FFFDF5] data-[state=active]:text-[#D01414] border-2 border-[#D01414]',
                                        ].join(' ')}
                                        style={triggerTextStyle}
                                    >
                                        FINISH
                                    </TabsTrigger>
                                </TabsList>

                                {/* Contents */}
                                {tabs.map((t) => (
                                    <TabsContent key={t.value} value={t.value} className="m-0 p-0">
                                        <Card
                                            className="relative mt-6 overflow-hidden border-0"
                                            style={{
                                                width: '100%',
                                                maxWidth: 606,
                                                minHeight: 334,
                                                borderRadius: 18,
                                                boxShadow: '0px 10px 18px rgba(0,0,0,0.20)',
                                                background:
                                                    'linear-gradient(90deg, #DE2515 0%, #F05F1B 55%, #FAA82A 100%)',
                                            }}
                                        >
                                            <div
                                                className="absolute inset-0"
                                                style={{
                                                    background:
                                                        'linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.28) 100%)',
                                                }}
                                            />

                                            <CardHeader className="relative z-10 px-6 pt-[22px]">
                                                <CardTitle
                                                    style={{
                                                        fontFamily: 'Orbitron, ui-sans-serif, system-ui',
                                                        fontSize: 24,
                                                        lineHeight: '28px',
                                                        letterSpacing: '0.10em',
                                                        color: '#FFFDF5',
                                                        textTransform: 'uppercase',
                                                    }}
                                                >
                                                    {t.title}
                                                </CardTitle>

                                                <div
                                                    style={{
                                                        marginTop: 12,
                                                        height: 1,
                                                        width: '100%',
                                                        backgroundColor: 'rgba(255, 253, 245, 0.70)',
                                                    }}
                                                />
                                            </CardHeader>

                                            <CardContent className="relative z-10 px-6 pb-6 pt-0">
                                                <CardDescription
                                                    style={{
                                                        whiteSpace: 'pre-line',
                                                        fontFamily: 'oxanium, ui-sans-serif, system-ui',
                                                        fontSize: 14,
                                                        lineHeight: '19px',
                                                        color: '#FFFDF5',
                                                    }}
                                                >
                                                    {t.body}
                                                </CardDescription>
                                            </CardContent>
                                        </Card>
                                    </TabsContent>
                                ))}
                            </Tabs>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
};
