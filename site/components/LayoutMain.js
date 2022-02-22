import Link from 'next/link'

export default function LayoutMain({ children }) {
  return (
    <>
      <nav className="mt-6 mx-auto max-w-4xl">
        <div className="border-b border-gray-700">
          <Link href="/">
            <a className="text-gray-500">Home</a>
          </Link>
        </div>
      </nav>
      <main className="pb-16 mx-auto pt-4 max-w-4xl text-lg pr-28">
        {children}
      </main>
    </>
  )
}
