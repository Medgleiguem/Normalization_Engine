import React from 'react';
import { motion } from 'framer-motion';
import { Download, FileText, Database, FileSpreadsheet, CheckCircle, TrendingUp } from 'lucide-react';
import { getDownloadUrl } from '../services/api';

const ResultsPanel = ({ analysisResult }) => {
  if (!analysisResult) return null;

  const {
    analysis_id,
    original_table,
    original_nf,
    final_nf,
    steps_count,
    tables_count,
    violations_count,
    steps
  } = analysisResult;

  const handleDownload = (type) => {
    const url = getDownloadUrl(analysis_id, type);
    window.open(url, '_blank');
  };

  return (
    <div className="w-full max-w-6xl mx-auto space-y-6">
      {/* Success Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="card-gradient text-center"
      >
        <div className="flex justify-center mb-4">
          <div className="p-4 bg-accent-100 rounded-full">
            <CheckCircle className="w-16 h-16 text-accent-600" />
          </div>
        </div>
        <h2 className="text-3xl font-bold text-gray-800 mb-2">
          Analyse Terminée !
        </h2>
        <p className="text-lg text-gray-600">
          Votre base de données a été normalisée avec succès
        </p>
      </motion.div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="card"
        >
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-blue-100 rounded-lg">
              <TrendingUp className="w-6 h-6 text-blue-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Normalisation</p>
              <p className="text-xl font-bold text-gray-800">{original_nf} → {final_nf}</p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="card"
        >
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-purple-100 rounded-lg">
              <Database className="w-6 h-6 text-purple-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Tables Créées</p>
              <p className="text-xl font-bold text-gray-800">{tables_count}</p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="card"
        >
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-green-100 rounded-lg">
              <CheckCircle className="w-6 h-6 text-green-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Étapes Appliquées</p>
              <p className="text-xl font-bold text-gray-800">{steps_count}</p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="card"
        >
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-red-100 rounded-lg">
              <FileText className="w-6 h-6 text-red-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Violations Corrigées</p>
              <p className="text-xl font-bold text-gray-800">{violations_count}</p>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Download Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="card-gradient"
      >
        <h3 className="text-2xl font-bold text-gray-800 mb-6">Télécharger les Résultats</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button
            onClick={() => handleDownload('report')}
            className="group p-6 bg-white hover:bg-primary-50 border-2 border-gray-200 hover:border-primary-400 rounded-xl transition-all duration-300 hover:shadow-lg"
          >
            <div className="flex flex-col items-center text-center space-y-3">
              <div className="p-4 bg-blue-100 group-hover:bg-blue-200 rounded-full transition-colors">
                <FileText className="w-8 h-8 text-blue-600" />
              </div>
              <div>
                <h4 className="font-semibold text-lg text-gray-800">Rapport Académique</h4>
                <p className="text-sm text-gray-600 mt-1">
                  Rapport d'analyse complet (DOCX)
                </p>
              </div>
              <div className="flex items-center space-x-2 text-primary-600 font-medium">
                <Download className="w-4 h-4" />
                <span>Télécharger</span>
              </div>
            </div>
          </button>

          <button
            onClick={() => handleDownload('sql')}
            className="group p-6 bg-white hover:bg-primary-50 border-2 border-gray-200 hover:border-primary-400 rounded-xl transition-all duration-300 hover:shadow-lg"
          >
            <div className="flex flex-col items-center text-center space-y-3">
              <div className="p-4 bg-purple-100 group-hover:bg-purple-200 rounded-full transition-colors">
                <Database className="w-8 h-8 text-purple-600" />
              </div>
              <div>
                <h4 className="font-semibold text-lg text-gray-800">Script MySQL</h4>
                <p className="text-sm text-gray-600 mt-1">
                  Script de création de base de données (SQL)
                </p>
              </div>
              <div className="flex items-center space-x-2 text-primary-600 font-medium">
                <Download className="w-4 h-4" />
                <span>Télécharger</span>
              </div>
            </div>
          </button>

          <button
            onClick={() => handleDownload('excel')}
            className="group p-6 bg-white hover:bg-primary-50 border-2 border-gray-200 hover:border-primary-400 rounded-xl transition-all duration-300 hover:shadow-lg"
          >
            <div className="flex flex-col items-center text-center space-y-3">
              <div className="p-4 bg-green-100 group-hover:bg-green-200 rounded-full transition-colors">
                <FileSpreadsheet className="w-8 h-8 text-green-600" />
              </div>
              <div>
                <h4 className="font-semibold text-lg text-gray-800">Excel Normalisé</h4>
                <p className="text-sm text-gray-600 mt-1">
                  Tables de données normalisées (XLSX)
                </p>
              </div>
              <div className="flex items-center space-x-2 text-primary-600 font-medium">
                <Download className="w-4 h-4" />
                <span>Télécharger</span>
              </div>
            </div>
          </button>
        </div>
      </motion.div>

      {/* Normalization Steps */}
      {steps && steps.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="card"
        >
          <h3 className="text-2xl font-bold text-gray-800 mb-6">Étapes de Normalisation</h3>
          
          <div className="space-y-4">
            {steps.map((step, index) => (
              <div
                key={index}
                className="p-4 bg-gray-50 rounded-lg border border-gray-200"
              >
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-semibold text-lg text-gray-800">
                    Étape {index + 1}: {step.from_nf} → {step.to_nf}
                  </h4>
                  <span className="badge-warning">
                    {step.violations} violation{step.violations !== 1 ? 's' : ''}
                  </span>
                </div>
                <p className="text-gray-600 text-sm">
                  {step.explanation}
                </p>
              </div>
            ))}
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default ResultsPanel;
