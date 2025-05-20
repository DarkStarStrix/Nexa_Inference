import Link from 'next/link';
import { Layout } from '../components/Layout';

export default function Home() {
  return (
    <Layout>
      <div className="relative bg-white overflow-hidden">
        <div className="max-w-7xl mx-auto">
          <div className="relative z-10 pb-8 bg-white sm:pb-16 md:pb-20 lg:max-w-2xl lg:w-full lg:pb-28 xl:pb-32">
            <main className="mt-10 mx-auto max-w-7xl px-4 sm:mt-12 sm:px-6 md:mt-16 lg:mt-20 lg:px-8 xl:mt-28">
              <div className="sm:text-center lg:text-left">
                <h1 className="text-4xl tracking-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
                  <span className="block xl:inline">Advanced Scientific</span>{' '}
                  <span className="block text-blue-600 xl:inline">Inference Engine</span>
                </h1>
                <p className="mt-3 text-base text-gray-500 sm:mt-5 sm:text-lg sm:max-w-xl sm:mx-auto md:mt-5 md:text-xl lg:mx-0">
                  Accelerate your research with our state-of-the-art machine learning models for biology, astrophysics, and materials science.
                </p>
                <div className="mt-5 sm:mt-8 sm:flex sm:justify-center lg:justify-start">
                  <div className="rounded-md shadow">
                    <Link
                      href="/dashboard"
                      className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 md:py-4 md:text-lg md:px-10"
                    >
                      Get Started
                    </Link>
                  </div>
                  <div className="mt-3 sm:mt-0 sm:ml-3">
                    <a
                      href="https://github.com/yourusername/HelixSynth"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-blue-700 bg-blue-100 hover:bg-blue-200 md:py-4 md:text-lg md:px-10"
                    >
                      View on GitHub
                    </a>
                  </div>
                </div>
              </div>
            </main>
          </div>
        </div>
        <div className="lg:absolute lg:inset-y-0 lg:right-0 lg:w-1/2">
          <div className="h-56 w-full bg-blue-100 sm:h-72 md:h-96 lg:w-full lg:h-full">
            {/* Add relevant scientific visualization or hero image here */}
          </div>
        </div>
      </div>

      {/* Feature Section */}
      <div className="py-12 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="lg:text-center">
            <h2 className="text-base text-blue-600 font-semibold tracking-wide uppercase">Features</h2>
            <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
              Advanced Scientific Computing
            </p>
          </div>

          <div className="mt-10">
            <div className="space-y-10 md:space-y-0 md:grid md:grid-cols-3 md:gap-x-8 md:gap-y-10">
              {/* Biology Feature */}
              <div className="relative">
                <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-blue-500 text-white">
                  🧬
                </div>
                <p className="ml-16 text-lg leading-6 font-medium text-gray-900">Biology Models</p>
                <p className="mt-2 ml-16 text-base text-gray-500">
                  Advanced protein structure prediction and genomic analysis tools.
                </p>
              </div>

              {/* Astrophysics Feature */}
              <div className="relative">
                <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-blue-500 text-white">
                  🌌
                </div>
                <p className="ml-16 text-lg leading-6 font-medium text-gray-900">Astrophysics Models</p>
                <p className="mt-2 ml-16 text-base text-gray-500">
                  Stellar classification and cosmological parameter estimation.
                </p>
              </div>

              {/* Materials Science Feature */}
              <div className="relative">
                <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-blue-500 text-white">
                  ⚛️
                </div>
                <p className="ml-16 text-lg leading-6 font-medium text-gray-900">Materials Science</p>
                <p className="mt-2 ml-16 text-base text-gray-500">
                  Material property prediction and structure analysis.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
