import React from 'react';
import { motion } from 'framer-motion';
import { CheckCircle2, Circle, Loader2 } from 'lucide-react';

const AnalysisProgress = ({ currentStep, steps, isAnalyzing }) => {
  const normalForms = [
    { id: 'upload', name: 'File Upload', description: 'Excel file uploaded successfully' },
    { id: '1nf', name: '1NF Analysis', description: 'Checking for atomic values and repeating groups' },
    { id: '2nf', name: '2NF Analysis', description: 'Detecting partial dependencies' },
    { id: '3nf', name: '3NF Analysis', description: 'Identifying transitive dependencies' },
    { id: 'bcnf', name: 'BCNF Analysis', description: 'Verifying determinant constraints' },
    { id: '4nf', name: '4NF Analysis', description: 'Checking multi-valued dependencies' },
    { id: '5nf', name: '5NF Analysis', description: 'Analyzing join dependencies' },
    { id: 'generate', name: 'Generate Outputs', description: 'Creating report, SQL script, and Excel file' },
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
          Normalization Analysis Progress
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
                    <span className="badge-success">Complete</span>
                  </div>
                )}
                {status === 'active' && (
                  <div className="flex-shrink-0">
                    <span className="badge-info">Processing...</span>
                  </div>
                )}
              </motion.div>
            );
          })}
        </div>
        
        {/* Progress bar */}
        <div className="mt-6">
          <div className="flex justify-between text-sm text-gray-600 mb-2">
            <span>Overall Progress</span>
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
