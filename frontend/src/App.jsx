import React from 'react';
import CreativeForm from './components/CreativeForm';

function App() {
  return (
    <div className="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-extrabold text-gray-900 sm:text-5xl sm:tracking-tight lg:text-6xl">
            Auto-Creative Engine
          </h1>
          <p className="mt-5 max-w-xl mx-auto text-xl text-gray-500">
            Generate high-quality ad creatives in seconds using AI.
          </p>
        </div>
        <CreativeForm />
      </div>
    </div>
  );
}

export default App;
