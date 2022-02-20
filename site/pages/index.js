import HeadTag from '../components/HeadTag'
import CodeBlock from '../components/CodeBlock'
import Image from 'next/image'
import yabai_layout_script_example from '../images/yabai_layout_script_example.webp'
import yabai_resize_example from '../images/yabai_resize_example.webp'

export default function HomePage() {
  const exampleCode = `
const some_var = 'a value'
const some_object = { key: 'value' }
`

  const asdf = `
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
        I'm using the <a href="https://github.com/koekeishiya/yabai">Yabai</a>{' '}
        tiling window manager on my mac. Having windows automatically position
        themselves is a suprisingly large quality of life improvement.{' '}
      </p>
      <p>
        The one thing that bugged me is that it can be difficult to get windows
        to go where you want them to for anything but the most basic layout. So,
        I wrote some scripts to help out with that.
      </p>

      <p>It looks like this:</p>

      <div className="pb-6">
        <Image src={yabai_layout_script_example} />
      </div>

      <h2>TL;DR - Setup And Run</h2>

      <p>To get up and running fast, do this:</p>

      <ul>
        <li>
          Create a self signed cert as{' '}
          <a href="https://github.com/koekeishiya/yabai/wiki/Installing-yabai-%28from-HEAD%29">
            described here
          </a>
        </li>
        <li>
          Run:{' '}
          <CodeBlock
            src={`brew install koekeishiya/formulae/yabai --HEAD
codesign -fs 'yabai-cert' $(which yabai)`}
            language="bash"
          />
        </li>
        <li>
          Do Not Run These <br />
          (unless you read through the docs and understand the security changes
          you&apos;d have to make)
          <CodeBlock
            src={`
sudo yabai --install-sa
sudo yabai --load-sa
`}
            language="bash"
          />
        </li>
        <li>
          Start Yabai with:
          <CodeBlock src="brew services start yabai" language="bash" />
        </li>
        <li>
          Open however many spaces you&apos;re going to need with{' '}
          <a href="https://support.apple.com/en-us/HT204100">Mission Control</a>
        </li>
        <li>
          Download{' '}
          <a href="https://github.com/alanwsmith/yabai.alanwsmith.com/blob/main/site/scripts/yabai_resize_example.py">
            this script
          </a>
          , tweak the layout commands at the bottom, and run it with:
          <CodeBlock src="python3 yabai_resize_example.py" language="bash" />
        </li>
      </ul>

      <h2>Moving Windows</h2>

      <p>
        After the windows are are in place, you can drag them around and
        everything resizes automaticaly. It's like magic.
      </p>

      <div className="pb-6">
        <Image src={yabai_resize_example} />
      </div>

      <h2>Yabai Installation Details</h2>

      <p>
        I installed Yabai with <a href="https://brew.sh/">Homebrew</a>.
      </p>

      <p>
        I installed Yabai from the HEAD branch since I'm using an M1 Mac.
        (I&apos;m not sure if that&apos;s required but it seemed like a good
        idea.) Using the HEAD branch requires creating a self-signed
        certificate. Directions for that and the install{' '}
        <a href="https://github.com/koekeishiya/yabai/wiki/Installing-yabai-%28from-HEAD%29">
          are here
        </a>
        . Basically, once you get the cert setup, you run:
      </p>

      <CodeBlock
        src={`
brew install koekeishiya/formulae/yabai --HEAD
codesign -fs 'yabai-cert' $(which yabai)
`}
        language="bash"
      />
      <p>And then start Yabai with:</p>

      <CodeBlock src={`brew services start yabai`} language="bash" />

      <p>
        Note that you do not have to install the scripting additions (i.e. `sudo
        yabai --install-sa`) for my scripts to work. I haven&apos;t installed
        them becuase as of the time of this writing, they don&apos;t work on M1
        macs. Secondarily, part of the scripting additions require turning of
        some system level security stuff that I prefer to leave on.
      </p>

      <h2>Downloading And Running The Scripts</h2>
      <p>
        You can download the{' '}
        <a href="https://github.com/alanwsmith/yabai.alanwsmith.com/blob/main/site/scripts/yabai_resize_example.py">
          example script here.
        </a>
      </p>

      <p>
        It&apos;s written in python3 and make calls to the yabai command line{' '}
        <a href="https://github.com/koekeishiya/yabai/wiki/Commands#message-passing-interface">
          message passing interface
        </a>
        . I use python3 from homebrew, but I think there's a system python3
        installed on macs so you should be able to run the scripts without any
        other installs like:
      </p>

      <CodeBlock src={`python3 yabai_resize_example.py`} language="bash" />

      <h2>The Gory Details</h2>

      <ul>
        <li>
          You'll need to have already created your spaces prior to running the
          script
        </li>
        <li>
          The script will attempt to open apps if they aren&apos;t already open.
          It waits a while but will time out if the app doesn&apos;t open in a
          reasonable time. That timeout is adjustable in the
          `.ensure_app_is_open()` funciton.
        </li>

        <li>
          There&apos;s some delays inserted between certain actions. It&apos;
          covers everything in my testing, but different environments may have
          different results. If the script times out, adjust the time with
          `am.time_padding = 0.3` (or longer) on a line right after the `am =
          AppMover()` line.
        </li>

        <li>
          The `am.stage_apps()` call moves all windows to the last availabe
          space to prep them for moving to their final locaitons. This is
          necessary because things don't work right if an app is already on a
          window you tell it to move to.
        </li>
        <li>
          The spces can be spread across multiple monitors. The listed Desktop
          number in Mission Control is cohesive across them.
        </li>

        <li>
          If you have two windows open for a single app (e.g. two Chrome
          windows), only one of them will be adjusted. Adding a feature to deal
          with multiple windows is possible but not something I need at this
          point.
        </li>

        <li>
          To do a baisc movement of an app to a window, use:
          <CodeBlock
            src="am.move_app_to_space('App Name', #)"
            language="python"
          />
          where 'App Name' is the name of your app and `#` is the space number
          to move to. For example:
          <CodeBlock
            src="am.move_app_to_space('Discord', 6)"
            language="python"
          />
        </li>

        <li>
          The other command to move a window to a space is
          `am.insert_from_anchor()` It looks like this:
          <pre>
            <code>
              am.insert_from_anchor('iTerm2', 'west', 'Google Chrome')
            </code>
          </pre>
        </li>

        <li>
          It places the second app (e.g. 'Google Chrome') next to the first app
          (e.g. 'iTerm1') based on the requested direction (e.g. 'west')
        </li>

        <li>
          It&apos;s also possible to put one app behind another (and then
          cmd+tab or flip between them with an app switcher). This is done with:
          <CodeBlock src={`yabai_layout_script_example`} language={`bash`} />
        </li>

        <li>
          The last positioning part is the `am.expand_DIRECTION()` calls. They
          example the requested window in the request direction to the requested
          amount.
        </li>

        <li>
          The name of the app isn't always what shows up in the menua bar. The
          way to find them is to open the app and the then run this to find the
          app name that Yabai sees:
          <pre>
            <code>yabai -m query --windows</code>
          </pre>
          One symptom of not having the correct name is that Yabai will try to
          start the app, but it will time out.
        </li>

        <li>
          I the script doesn't complete a run, you'll sometimes see a red
          overlay on one of the app windows where the next app was about to
          move. I clear this by dragging another app window out it then fiddling
          with the script to figure out what went wrong.
        </li>
        <li>
          Look at the .yabrc file for how to setup apps to not be controlled by
          yabai so they always float (e.g. I let the finder always be floating)
        </li>
        <li>
          Some apps have minimum dimensions. If you try to place them in smaller
          areas they stick out and sometimes mess with other windows
        </li>
        <li>
          You always want to end the script with a `.fouce_app()` call. Without
          that, sometimes the focus stays on an app in a difference space and
          when you type it goes to that and you can&apos;t see it
        </li>
        <li>
          Sometimes swithing to apps in Yabai doesn&apos;t work properly. For
          example, if you have Finder on a space that&apos;s not in focus you
          may not be able to CMD+Tab to it or bring it up from Spotlight or an
          app switcher.
        </li>
        <li>
          The python process is not aware of the homebrew path yabai is sitting
          on. At the time of this writing, that path is
          `/opt/homebrew/bin/yabai`. If that&apos;s not where you yabai is, you
          can change the path by calling `am.yabai_path =
          '/opt/homebrew/bin/yabai'` right after the `am = AppMover()`.
        </li>
      </ul>
    </>
  )
}
