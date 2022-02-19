import React from 'react'
import Highlight, { defaultProps } from 'prism-react-renderer'
import nightOwl from 'prism-react-renderer/themes/nightOwl'
import dracula from 'prism-react-renderer/themes/dracula'

const exampleCode = `
const example = 'thing'
const more = 'here'
`

export default function CodeBlockWithLineNumbers() {
  // TODO: Might need to adjust these keys so they are different
  // across different code blocks on the same page? Not really sure
  // how keys work that way
  return (
    <Highlight
      {...defaultProps}
      theme={nightOwl}
      code={exampleCode.trim()}
      language="jsx"
    >
      {({ className, style, tokens, getLineProps, getTokenProps }) => (
        <pre className={`${className} code_block`} style={style}>
          {tokens.map((line, i) => (
            <div
              key={i}
              {...getLineProps({ line, key: i })}
              className="token-line code_line"
            >
              <span
                className={
                  i === 0
                    ? `code_line_number code_line_number_first`
                    : i === tokens.length - 1
                    ? `code_line_number code_line_number_last`
                    : `code_line_number`
                }
              >
                {i + 1}
              </span>
              <span className={`code_line_content`}>
                {line.map((token, key) => (
                  <span key={key} {...getTokenProps({ token, key })} />
                ))}
              </span>
            </div>
          ))}
        </pre>
      )}
    </Highlight>
  )
}

export function CodeBlock() {
  /* eslint-disable */
  return (
    <Highlight
      theme={nightOwl}
      {...defaultProps}
      code={exampleCode}
      language="jsx"
    >
      {({ className, style, tokens, getLineProps, getTokenProps }) => (
        <pre className={className} style={style}>
          {tokens.map((line, i) => (
            <div {...getLineProps({ line, key: i })}>
              {line.map((token, key) => (
                <span {...getTokenProps({ token, key })} />
              ))}
            </div>
          ))}
        </pre>
      )}
    </Highlight>
  )
  /* eslint-enable */
}
