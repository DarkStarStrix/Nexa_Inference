import { useState, useEffect } from 'react';
import { Layout } from '../components/Layout';
import axios from 'axios';

interface ModelVersion {
  [key: string]: string[];
}

interface HealthStatus {
  status: string;
  version: string;
  model_status: {
    [key: string]: boolean;
  };
}

export default function Dashboard() {
  const [models, setModels] = useState<ModelVersion>({});
  const [selectedModel, setSelectedModel] = useState('');
  const [selectedVersion, setSelectedVersion] = useState('');
  const [inputData, setInputData] = useState('');
  const [result, setResult] = useState<any>(null);
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchModels();
    checkHealth();
  }, []);

  const fetchModels = async () => {
    try {
      const response = await axios.get('http://localhost:8000/models');
      setModels(response.data);
    } catch (err) {
      setError('Failed to fetch models');
      console.error(err);
    }
  };

  const checkHealth = async () => {
    try {
      const response = await axios.get('http://localhost:8000/health');
      setHealth(response.data);
    } catch (err) {
      setError('Failed to check system health');
      console.error(err);
    }
  };

  const handlePredict = async () => {
    setLoading(true);
    setError('');
    try {
      let modelType = '';
      if (selectedModel.includes('Bio')) modelType = 'bio';
      else if (selectedModel.includes('Astro')) modelType = 'astro';
      else if (selectedModel.includes('Mat')) modelType = 'materials';

      const response = await axios.post(`http://localhost:8000/predict/${modelType}`, {
        model_name: selectedModel,
        version: selectedVersion,
        data: JSON.parse(inputData)
      });
      setResult(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Prediction failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-8">HelixSynth Dashboard</h1>

        {/* Health Status */}
        <div className="mb-8 p-4 bg-gray-100 rounded-lg">
          <h2 className="text-xl font-semibold mb-4">System Status</h2>
          {health && (
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p>Status: <span className={health.status === 'healthy' ? 'text-green-600' : 'text-red-600'}>
                  {health.status}
                </span></p>
                <p>Version: {health.version}</p>
              </div>
              <div>
                <h3 className="font-medium mb-2">Model Status:</h3>
                {Object.entries(health.model_status).map(([model, status]) => (
                  <p key={model}>{model}: <span className={status ? 'text-green-600' : 'text-red-600'}>
                    {status ? 'Available' : 'Unavailable'}
                  </span></p>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Model Selection */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold mb-4">Model Selection</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <select
              className="form-select w-full"
              value={selectedModel}
              onChange={(e) => setSelectedModel(e.target.value)}
            >
              <option value="">Select Model</option>
              {Object.keys(models).map((model) => (
                <option key={model} value={model}>{model}</option>
              ))}
            </select>

            <select
              className="form-select w-full"
              value={selectedVersion}
              onChange={(e) => setSelectedVersion(e.target.value)}
              disabled={!selectedModel}
            >
              <option value="">Select Version</option>
              {selectedModel && models[selectedModel]?.map((version) => (
                <option key={version} value={version}>{version}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Input Data */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold mb-4">Input Data</h2>
          <textarea
            className="w-full h-48 p-2 border rounded"
            value={inputData}
            onChange={(e) => setInputData(e.target.value)}
            placeholder="Enter input data in JSON format..."
          />
        </div>

        {/* Action Buttons */}
        <div className="mb-8">
          <button
            className="bg-blue-600 text-white px-6 py-2 rounded disabled:bg-gray-400"
            onClick={handlePredict}
            disabled={!selectedModel || !inputData || loading}
          >
            {loading ? 'Processing...' : 'Run Inference'}
          </button>
        </div>

        {/* Error Display */}
        {error && (
          <div className="mb-8 p-4 bg-red-100 text-red-700 rounded">
            {error}
          </div>
        )}

        {/* Results Display */}
        {result && (
          <div className="mb-8 p-4 bg-green-100 rounded">
            <h2 className="text-xl font-semibold mb-4">Results</h2>
            <pre className="whitespace-pre-wrap">
              {JSON.stringify(result, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </Layout>
  );
}

