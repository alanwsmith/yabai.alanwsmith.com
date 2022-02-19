import Link from 'next/link'

export default function LayoutMain({ children }) {
  return (
    <>
      <nav className="mt-4 mx-auto pt-2 px-6 max-w-prose">
        <div className="border-b border-gray-700">
          <Link href="/">
            <a className="text-gray-500">Home</a>
          </Link>
        </div>
      </nav>
      <main className="pb-16 mx-auto container pt-3 px-6 max-w-prose">
        {children}
      </main>
    </>
  )
}
