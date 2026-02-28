import { useMemo, useState } from 'react';
import { Tabs, TabsContent } from '@/components/ui/tabs';
import './JourneySection.css';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

import journeyTabsRaw from './StaticContent/journeyTabs.json';
import { JourneyTabs, JourneyTabEntry } from './JourneyTabs';

type JourneyTab = 'start' | 'gather' | 'hack' | 'finish';

type JourneyTabContent = JourneyTabEntry & {
    title: string;
    body: string;
};

export const JourneySection = () => {
    const tabs = useMemo(() => journeyTabsRaw as JourneyTabContent[], []);
    const [activeTab, setActiveTab] = useState<JourneyTab>('finish');
    const handleTabChange = (value: string) => setActiveTab(value as JourneyTab);

    return (
        <section className="w-full" id="journey">
            <div className="relative w-full overflow-hidden rounded-[32px] bg-[#FFFDF5]">
                <div className="relative w-full sm:h-[clamp(560px,80vh,780px)]">
                    {/* VISUAL LAYER (hidden on phones) */}
                    {/* Key fix: constrain visuals to a LEFT container so they can't spill into content on iPad */}
                    <div
                        className="hidden sm:block absolute inset-y-0 left-0 pointer-events-none select-none overflow-hidden
                          w-[55%] md:w-[50%] lg:w-[45%] xl:w-[42%]"
                    >
                        <img
                            src="/journeyShooter.png"
                            alt="Journey visual"
                            className="absolute inset-0 w-full h-full object-cover object-center"
                            draggable={false}
                        />
                    </div>

                    {/* CONTENT LAYER */}
                    <div className="relative z-10 mx-auto h-full w-full max-w-[1440px]">
                        <div className="h-full w-full px-4 py-10 sm:py-0 sm:px-6 md:px-4 lg:px-4 xl:px-6 flex flex-col justify-center">
                            {/* iPad fix: make content block slightly smaller on lg so it won't collide */}
                            <div className="w-full ml-auto max-w-[680px] lg:max-w-[620px] xl:max-w-[700px]">
                                {/* Header:
                    MOBILE centered (unchanged), SM+ right (unchanged) */}
                                <div className="mb-6 sm:mb-8 flex items-center gap-4 justify-center sm:justify-end">
                                    <div
                                        className="text-[#D01414] whitespace-nowrap"
                                        style={{
                                            fontFamily: 'Orbitron, ui-sans-serif, system-ui',
                                            fontSize: 'clamp(26px, 3.0vw, 40px)',
                                            letterSpacing: 'clamp(0.18em, 0.6vw, 0.32em)',
                                            lineHeight: '1.1',
                                            textTransform: 'uppercase',
                                        }}
                                    >
                                        JOURNEY
                                    </div>
                                    <img
                                        src="/mockingjay-red.svg"
                                        alt=""
                                        className="h-[28px] sm:h-[34px] md:h-[40px] xl:h-[44px] w-auto"
                                        draggable={false}
                                    />
                                </div>

                                <Tabs value={activeTab} onValueChange={handleTabChange} className="w-full">
                                    <div className="mb-6">
                                        <JourneyTabs
                                            activeTab={activeTab}
                                            entries={tabs.map(({ value, label }) => ({ value, label }))}
                                        />
                                    </div>

                                    {tabs.map((t) => (
                                        <TabsContent
                                            key={t.value}
                                            value={t.value}
                                            className="m-0 p-0 journey-tab-content"
                                        >
                                            <Card
                                                className="relative overflow-hidden border-0 w-full"
                                                style={{
                                                    // iPad: allow a bit shorter card so it fits nicer under tabs
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
                                                            fontSize: 28,
                                                            lineHeight: '34px',
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
                                                            fontSize: 16,
                                                            lineHeight: '24px',
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

                    {/* MOBILE RULES UNCHANGED:
              - visuals are hidden on mobile (sm:block)
              - header centered on mobile
              - tabs are 2x2 on mobile */}
                </div>
            </div>
        </section>
    );
};
