
import './index.css'

function App() {
  return (
    <div className="min-h-screen bg-slate-900 flex flex-col items-center justify-center text-white">
      <div className="p-8 bg-slate-800 rounded-2xl border border-slate-700 shadow-2xl text-center max-w-sm">
        <h1 className="text-3xl font-extrabold text-blue-400">Day 1 is Live!</h1>
        <p className="mt-3 text-slate-400">
          Tailwind v4 is configured and working perfectly in TypeScript.
        </p>
        <button className="mt-6 px-6 py-2 bg-blue-500 hover:bg-blue-600 active:scale-95 transition-transform rounded-lg font-medium">
          Let's Build
        </button>
      </div>
    </div>
  )
}

export default App
