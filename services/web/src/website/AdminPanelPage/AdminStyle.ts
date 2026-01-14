export const Styles = {
    colors: {
        darkNavy: '#020F1B',
        deepBlue: '#18305F',
        hubCyan: '#00B2FF',
        hubCyanHover: '#0096D6',
        textDimmed: 'text-blue-200/60',
        textMuted: 'text-white/20',
    },

    backgrounds: {
        primaryGradient: 'bg-[linear-gradient(145deg,_#020F1B_0%,_#0B1E3B_50%,_#18305F_100%)]',
        previewBox:
            'bg-white/[0.02] border-white/10 border-2 border-dashed hover:border-white/20 transition-all duration-300',
        footerDark: 'bg-black/40 border-t border-white/5 backdrop-blur-md',
    },

    glass: {
        card: 'bg-white/[0.03] backdrop-blur-xl border border-white/10 shadow-2xl overflow-hidden',
        cardHover: 'hover:border-white/20 hover:bg-white/10 transition-all duration-300',
        ghostButton: 'text-white/70 hover:text-white hover:bg-white/10 transition-all duration-200',
        input: 'bg-white/[0.05] border-white/10 text-white focus:border-[#00B2FF]/50 focus:ring-2 focus:ring-[#00B2FF]/20 transition-all',
    },

    text: {
        title: 'text-white font-bold tracking-tight',
        subtitle: 'text-blue-200/50 mt-2 leading-relaxed',
        label: 'text-[11px] font-bold text-blue-200/40 uppercase tracking-[0.2em]',
    },

    actions: {
        primaryButton:
            'text-white font-bold shadow-[0_0_20px_rgba(0,178,255,0.3)] hover:shadow-[0_0_25px_rgba(0,178,255,0.5)] transition-all hover:opacity-90 active:scale-[0.98]',
        secondaryButton: 'text-black bg-white border-white hover:bg-gray-200 transition-colors',
    },

    forms: {
        fieldContainer:
            'flex-1 space-y-6 [&_label]:text-white [&_input]:text-black [&_input]:bg-white [&_textarea]:text-black [&_textarea]:bg-white',
    },
} as const;
