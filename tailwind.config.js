module.exports = {
    content: ["./src/**/*.{html,js}"],
    theme: {
        extend: {
            colors: {
                // Customize colors here
                primary: '#1a202c',
                secondary: '#2d3748',
                accent: '#38b2ac',
            },
            fontFamily: {
                sans: ['Inter', 'sans-serif'],
            },
        },
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
        require('@tailwindcss/line-clamp'),
        require('daisyui'),
    ],
    daisyui: {
        themes: ["nord", "light", "dark"],
    },
};
