import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Database, Sparkles, ArrowRight, FileText, FileSpreadsheet } from 'lucide-react';
import FileUpload from '../components/FileUpload';
import AnalysisProgress from '../components/AnalysisProgress';
import ResultsPanel from '../components/ResultsPanel';
import { uploadFile, analyzeFile } from '../services/api';

const HomePage = () => {
  const [currentPhase, setCurrentPhase] = useState('upload'); // upload, analyzing, results
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileId, setFileId] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [currentStep, setCurrentStep] = useState(0);
  const [error, setError] = useState(null);

  const handleFileSelect = (file) => {
    setSelectedFile(file);
    setError(null);
  };

  const handleStartAnalysis = async () => {
    if (!selectedFile) return;

    try {
      setCurrentPhase('analyzing');
      setCurrentStep(0);
      setError(null);

      // Upload file
      setCurrentStep(1);
      const uploadResponse = await uploadFile(selectedFile, (progress) => {
        console.log('Upload progress:', progress);
      });

      setFileId(uploadResponse.file_id);
      setCurrentStep(2);

      // Start analysis
      const analysisResponse = await analyzeFile(uploadResponse.file_id);
      
      // Simulate progress through steps
      for (let i = 2; i <= 7; i++) {
        await new Promise(resolve => setTimeout(resolve, 500));
        setCurrentStep(i);
      }

      setAnalysisResult(analysisResponse);
      setCurrentStep(8);
      
      // Move to results
      setTimeout(() => {
        setCurrentPhase('results');
      }, 1000);

    } catch (err) {
      console.error('Analysis error:', err);
      setError(err.response?.data?.error || err.message || 'Une erreur est survenue lors de l\'analyse');
      setCurrentPhase('upload');
    }
  };

  const handleReset = () => {
    setCurrentPhase('upload');
    setSelectedFile(null);
    setFileId(null);
    setAnalysisResult(null);
    setCurrentStep(0);
    setError(null);
  };

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <div className="flex justify-center mb-4">
            <div className="p-4 bg-gradient-to-br from-primary-500 to-indigo-600 rounded-2xl shadow-xl">
              <Database className="w-12 h-12 text-white" />
            </div>
          </div>
          
          <h1 className="text-5xl font-bold mb-4">
            <span className="text-gradient">Normalisation de Base de Données</span>
            <br />
            <span className="text-gray-800">Outil d'Analyse</span>
          </h1>
          
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Téléchargez votre fichier Excel et obtenez une analyse complète de normalisation avec
            des rapports académiques, des scripts MySQL et des données normalisées
          </p>
          
          <div className="flex justify-center items-center space-x-2 mt-6">
            <Sparkles className="w-5 h-5 text-yellow-500" />
            <span className="text-sm font-medium text-gray-700">
              Propulsé par la détection de dépendances via IA
            </span>
          </div>
        </motion.div>

        {/* Error Display */}
        {error && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="max-w-2xl mx-auto mb-6 p-4 bg-red-50 border-2 border-red-200 rounded-lg"
          >
            <p className="text-red-800 font-medium">{error}</p>
            <button
              onClick={handleReset}
              className="mt-2 text-red-600 hover:text-red-800 font-medium text-sm underline"
            >
              Réessayer
            </button>
          </motion.div>
        )}

        {/* Main Content */}
        <AnimatePresence mode="wait">
          {currentPhase === 'upload' && (
            <motion.div
              key="upload-phase"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="space-y-8"
            >
              <FileUpload onFileSelect={handleFileSelect} />
              
              {selectedFile && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="text-center"
                >
                  <button
                    onClick={handleStartAnalysis}
                    className="btn-primary inline-flex items-center space-x-2 text-lg px-8 py-4"
                  >
                    <span>Lancer l'Analyse</span>
                    <ArrowRight className="w-5 h-5" />
                  </button>
                </motion.div>
              )}
            </motion.div>
          )}

          {currentPhase === 'analyzing' && (
            <motion.div
              key="analyzing-phase"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <AnalysisProgress currentStep={currentStep} isAnalyzing={true} />
            </motion.div>
          )}

          {currentPhase === 'results' && (
            <motion.div
              key="results-phase"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="space-y-6"
            >
              <ResultsPanel analysisResult={analysisResult} />
              
              <div className="text-center">
                <button
                  onClick={handleReset}
                  className="btn-secondary inline-flex items-center space-x-2"
                >
                  <span>Analyser un autre fichier</span>
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Features Section */}
        {currentPhase === 'upload' && !selectedFile && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-6"
          >
            <div className="card text-center">
              <div className="p-3 bg-blue-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <FileText className="w-8 h-8 text-blue-600" />
              </div>
              <h3 className="font-bold text-lg text-gray-800 mb-2">Rapport Académique</h3>
              <p className="text-gray-600 text-sm">
                Rapport standard universitaire avec contexte théorique et analyse étape par étape
              </p>
            </div>

            <div className="card text-center">
              <div className="p-3 bg-purple-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <Database className="w-8 h-8 text-purple-600" />
              </div>
              <h3 className="font-bold text-lg text-gray-800 mb-2">Script MySQL</h3>
              <p className="text-gray-600 text-sm">
                SQL prêt pour la production avec meilleures pratiques, contraintes et commentaires complets
              </p>
            </div>

            <div className="card text-center">
              <div className="p-3 bg-green-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <FileSpreadsheet className="w-8 h-8 text-green-600" />
              </div>
              <h3 className="font-bold text-lg text-gray-800 mb-2">Excel Normalisé</h3>
              <p className="text-gray-600 text-sm">
                Données normalisées avec métadonnées, dictionnaire de données et diagrammes relationnels
              </p>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
};

export default HomePage;
