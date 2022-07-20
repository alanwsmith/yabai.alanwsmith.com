import HeadTag from '../components/HeadTag'
import CodeBlock from '../components/CodeBlock'
// import Image from 'next/image'
// import yabai_layout_script_example from '../images/yabai_layout_script_example.gif'
// import yabai_resize_example from '../images/yabai_resize_example.gif'

export default function HomePage() {
  const holding = `

      `

  return (
    <>
      <HeadTag
        description="Automatic layout scripts for the Yabai tiling window manager for Mac"
        image="https://yabai.alanwsmith.com/og-images/main.png"
        title="The Yabai Scripts Of Alan"
        type="website"
        url="https://yabai.alanwsmith.com/"
      />

      <h1>Yabai Automatic Layout Scripts</h1>

      <p>NOTE: This page is still a work in progress</p>

      <p>
        I&apos;m using the{' '}
        <a href="https://github.com/koekeishiya/yabai">Yabai</a> tiling window
        manager on my mac. Having windows automatically position themselves is a
        suprisingly large quality of life improvement.{' '}
      </p>
      <p>
        The one thing that bugged me is that it can be difficult to get windows
        to go where you want them to for anything but the most basic layout. So,
        I wrote some scripts to help out with that.
      </p>

      <p>It looks like this:</p>

      <img
        src="/webp-files/yabai_layout_script_example.webp"
        alt="Application windows being put on a desktop and automatically resized to fit in a way where they are all visible"
      />

      <p>I will add more details later, but the scripts are <a href="https://github.com/alanwsmith/dotfiles.alanwsmith.com/tree/main/dotfiles/yabai/resize-scripts">here</a> if you want to poke around with them</p>

    </>
  )
}
