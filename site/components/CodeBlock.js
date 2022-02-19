import React from 'react'
import Highlight, { defaultProps } from 'prism-react-renderer'
import nightOwl from 'prism-react-renderer/themes/nightOwl'

export default function CodeBlock({ src, language }) {
  return (
    <Highlight
      {...defaultProps}
      theme={nightOwl}
      code={src.trim()}
      language={language}
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
              ></span>
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
