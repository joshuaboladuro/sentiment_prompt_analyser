import { SentimentApp } from "@/components/SentimentApp";

export default function Page() {
  return (
    <main className="min-h-screen w-full flex flex-col items-center justify-center px-4 py-12">
      <div className="w-full max-w-2xl">
        <header className="text-center mb-10">
          <h1 className="text-4xl sm:text-5xl font-bold tracking-tight text-zinc-900 dark:text-zinc-50">
            Sentiment Analyser
          </h1>
          <p className="mt-3 text-zinc-500 dark:text-zinc-400 text-lg">
            Type anything. Get an instant read on the mood.
          </p>
        </header>

        <SentimentApp />

        <footer className="mt-12 text-center text-xs text-zinc-400">
          Built by{" "}
          <a
            href="https://github.com/joshuaboladuro"
            target="_blank"
            rel="noreferrer"
            className="underline hover:text-zinc-600 dark:hover:text-zinc-300"
          >
            Joshua Boladuro
          </a>
        </footer>
      </div>
    </main>
  );
}
