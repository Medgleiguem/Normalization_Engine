import React from 'react';
import { motion } from 'framer-motion';
import { CheckCircle2, Circle, Loader2 } from 'lucide-react';

const AnalysisProgress = ({ currentStep, steps, isAnalyzing }) => {
  const normalForms = [
    { id: 'upload', name: 'Téléchargement du fichier', description: 'Fichier Excel téléchargé avec succès' },
    { id: '1nf', name: 'Analyse 1NF', description: 'Vérification des valeurs atomiques et groupes répétitifs' },
    { id: '2nf', name: 'Analyse 2NF', description: 'Détection des dépendances partielles' },
    { id: '3nf', name: 'Analyse 3NF', description: 'Identification des dépendances transitives' },
    { id: 'bcnf', name: 'Analyse BCNF', description: 'Vérification des contraintes des déterminants' },
    { id: '4nf', name: 'Analyse 4NF', description: 'Vérification des dépendances multivaluées' },
    { id: '5nf', name: 'Analyse 5NF', description: 'Analyse des dépendances de jointure' },
    { id: 'generate', name: 'Génération des résultats', description: 'Création du rapport, script SQL et fichier Excel' },
  ];

  const getStepStatus = (index) => {
    if (index < currentStep) return 'completed';
    if (index === currentStep) return 'active';
    return 'pending';
  };

  return (
    <div className="w-full max-w-3xl mx-auto">
      <div className="card-gradient">
        <h3 className="text-2xl font-bold text-gray-800 mb-6 text-center">
          Progression de l'Analyse de Normalisation
        </h3>
        
        <div className="space-y-4">
          {normalForms.map((step, index) => {
            const status = getStepStatus(index);
            
            return (
              <motion.div
                key={step.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className={`
                  flex items-start space-x-4 p-4 rounded-xl transition-all duration-300
                  ${status === 'active' ? 'bg-primary-50 border-2 border-primary-300' : ''}
                  ${status === 'completed' ? 'bg-accent-50 border border-accent-200' : ''}
                  ${status === 'pending' ? 'bg-gray-50 border border-gray-200' : ''}
                `}
              >
                <div className="flex-shrink-0 mt-1">
                  {status === 'completed' && (
                    <CheckCircle2 className="w-6 h-6 text-accent-600" />
                  )}
                  {status === 'active' && (
                    <Loader2 className="w-6 h-6 text-primary-600 animate-spin" />
                  )}
                  {status === 'pending' && (
                    <Circle className="w-6 h-6 text-gray-400" />
                  )}
                </div>
                
                <div className="flex-1">
                  <h4 className={`
                    font-semibold text-lg
                    ${status === 'active' ? 'text-primary-700' : ''}
                    ${status === 'completed' ? 'text-accent-700' : ''}
                    ${status === 'pending' ? 'text-gray-500' : ''}
                  `}>
                    {step.name}
                  </h4>
                  <p className={`
                    text-sm mt-1
                    ${status === 'active' ? 'text-primary-600' : ''}
                    ${status === 'completed' ? 'text-accent-600' : ''}
                    ${status === 'pending' ? 'text-gray-400' : ''}
                  `}>
                    {step.description}
                  </p>
                </div>
                
                {status === 'completed' && (
                  <div className="flex-shrink-0">
                    <span className="badge-success">Terminé</span>
                  </div>
                )}
                {status === 'active' && (
                  <div className="flex-shrink-0">
                    <span className="badge-info">En cours...</span>
                  </div>
                )}
              </motion.div>
            );
          })}
        </div>
        
        {/* Progress bar */}
        <div className="mt-6">
          <div className="flex justify-between text-sm text-gray-600 mb-2">
            <span>Progression globale</span>
            <span>{Math.round((currentStep / normalForms.length) * 100)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
            <motion.div
              className="h-full bg-gradient-to-r from-primary-500 via-primary-600 to-accent-500"
              initial={{ width: 0 }}
              animate={{ width: `${(currentStep / normalForms.length) * 100}%` }}
              transition={{ duration: 0.5 }}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalysisProgress;
