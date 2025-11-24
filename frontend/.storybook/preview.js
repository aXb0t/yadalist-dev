import '../dist/yadalist-ui.css'

/** @type { import('@storybook/html').Preview } */
const preview = {
  parameters: {
    actions: { argTypesRegex: '^on[A-Z].*' },
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
    backgrounds: {
      default: 'nord',
      values: [
        {
          name: 'nord',
          value: '#ECEFF4',
        },
        {
          name: 'dark',
          value: '#2E3440',
        },
        {
          name: 'white',
          value: '#FFFFFF',
        },
      ],
    },
  },
}

export default preview
