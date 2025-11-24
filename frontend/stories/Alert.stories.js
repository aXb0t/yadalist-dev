export default {
  title: 'Components/Alert',
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: { type: 'select' },
      options: ['success', 'error', 'info', 'warning'],
      description: 'Alert type',
    },
    message: {
      control: 'text',
      description: 'Alert message',
    },
  },
}

const Template = ({ variant, message }) => {
  return `
    <div class="alert alert--${variant}">
      ${message}
    </div>
  `
}

export const Success = Template.bind({})
Success.args = {
  variant: 'success',
  message: 'Your changes have been saved successfully!',
}

export const Error = Template.bind({})
Error.args = {
  variant: 'error',
  message: 'There was an error processing your request.',
}

export const Info = Template.bind({})
Info.args = {
  variant: 'info',
  message: 'Please verify your email address to continue.',
}

export const Warning = Template.bind({})
Warning.args = {
  variant: 'warning',
  message: 'Your session will expire in 5 minutes.',
}

export const AllVariants = () => `
  <div style="display: flex; flex-direction: column; gap: 1rem;">
    <div class="alert alert--success">
      Successfully logged in! Welcome back.
    </div>
    <div class="alert alert--error">
      Invalid username or password. Please try again.
    </div>
    <div class="alert alert--info">
      A password reset link has been sent to your email.
    </div>
    <div class="alert alert--warning">
      Your password will expire in 7 days. Please update it.
    </div>
  </div>
`

export const AlertList = () => `
  <ul class="alert-list">
    <li class="alert alert--success">Profile updated successfully</li>
    <li class="alert alert--info">Please check your email to verify changes</li>
  </ul>
`
