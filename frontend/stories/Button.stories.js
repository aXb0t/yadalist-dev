export default {
  title: 'Components/Button',
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: { type: 'select' },
      options: ['primary', 'secondary', 'success', 'danger'],
      description: 'Button style variant',
    },
    label: {
      control: 'text',
      description: 'Button text',
    },
    type: {
      control: { type: 'select' },
      options: ['button', 'submit', 'reset'],
      description: 'Button type attribute',
    },
  },
}

const Template = ({ variant, label, type = 'button' }) => {
  return `
    <button type="${type}" class="btn btn--${variant}">
      ${label}
    </button>
  `
}

export const Primary = Template.bind({})
Primary.args = {
  variant: 'primary',
  label: 'Primary Button',
}

export const Secondary = Template.bind({})
Secondary.args = {
  variant: 'secondary',
  label: 'Secondary Button',
}

export const Success = Template.bind({})
Success.args = {
  variant: 'success',
  label: 'Success Button',
}

export const Danger = Template.bind({})
Danger.args = {
  variant: 'danger',
  label: 'Danger Button',
}

export const AllVariants = () => `
  <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
    <button class="btn btn--primary">Primary</button>
    <button class="btn btn--secondary">Secondary</button>
    <button class="btn btn--success">Success</button>
    <button class="btn btn--danger">Danger</button>
  </div>
`
