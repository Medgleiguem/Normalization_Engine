import React, { useState, useCallback } from 'react';
import { Upload, FileSpreadsheet, X, AlertCircle } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const FileUpload = ({ onFileSelect, onUploadComplete }) => {
  const [isDragging, setIsDragging] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [error, setError] = useState(null);
  const [isUploading, setIsUploading] = useState(false);

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setIsDragging(false);
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFileSelection(files[0]);
    }
  }, []);

  const handleFileInput = (e) => {
    const files = e.target.files;
    if (files.length > 0) {
      handleFileSelection(files[0]);
    }
  };

  const handleFileSelection = (file) => {
    setError(null);
    
    // Validate file type
    const validTypes = ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel'];
    const validExtensions = ['.xlsx', '.xls'];
    const fileExtension = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
    
    if (!validTypes.includes(file.type) && !validExtensions.includes(fileExtension)) {
      setError('Veuillez télécharger un fichier Excel valide (.xlsx ou .xls)');
      return;
    }
    
    // Validate file size (max 16MB)
    if (file.size > 16 * 1024 * 1024) {
      setError('La taille du fichier doit être inférieure à 16 Mo');
      return;
    }
    
    setSelectedFile(file);
    if (onFileSelect) {
      onFileSelect(file);
    }
  };

  const handleRemoveFile = () => {
    setSelectedFile(null);
    setUploadProgress(0);
    setError(null);
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Octets';
    const k = 1024;
    const sizes = ['Octets', 'Ko', 'Mo'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      <AnimatePresence mode="wait">
        {!selectedFile ? (
          <motion.div
            key="upload-zone"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className={`
              relative border-3 border-dashed rounded-2xl p-12 text-center transition-all duration-300
              ${isDragging 
                ? 'border-primary-500 bg-primary-50 scale-105' 
                : 'border-gray-300 bg-white hover:border-primary-400 hover:bg-gray-50'
              }
            `}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
          >
            <input
              type="file"
              id="file-upload"
              className="hidden"
              accept=".xlsx,.xls"
              onChange={handleFileInput}
            />
            
            <motion.div
              animate={{ y: isDragging ? -10 : 0 }}
              transition={{ type: 'spring', stiffness: 300 }}
            >
              <Upload className={`w-16 h-16 mx-auto mb-4 ${isDragging ? 'text-primary-600' : 'text-gray-400'}`} />
            </motion.div>
            
            <h3 className="text-2xl font-bold text-gray-800 mb-2">
              {isDragging ? 'Déposez votre fichier ici' : 'Télécharger un fichier Excel'}
            </h3>
            
            <p className="text-gray-600 mb-6">
              Glissez et déposez votre fichier Excel ici, ou cliquez pour parcourir
            </p>
            
            <label htmlFor="file-upload" className="btn-primary cursor-pointer inline-block">
              Choisir un fichier
            </label>
            
            <p className="text-sm text-gray-500 mt-4">
              Formats supportés: .xlsx, .xls (Taille max: 16 Mo)
            </p>
          </motion.div>
        ) : (
          <motion.div
            key="file-selected"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            className="card"
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center space-x-4">
                <div className="p-3 bg-accent-100 rounded-lg">
                  <FileSpreadsheet className="w-8 h-8 text-accent-600" />
                </div>
                <div>
                  <h4 className="font-semibold text-lg text-gray-800">{selectedFile.name}</h4>
                  <p className="text-sm text-gray-600">{formatFileSize(selectedFile.size)}</p>
                </div>
              </div>
              
              <button
                onClick={handleRemoveFile}
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                disabled={isUploading}
              >
                <X className="w-5 h-5 text-gray-600" />
              </button>
            </div>
            
            {uploadProgress > 0 && uploadProgress < 100 && (
              <div className="mb-4">
                <div className="flex justify-between text-sm text-gray-600 mb-2">
                  <span>Téléchargement...</span>
                  <span>{uploadProgress}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
                  <motion.div
                    className="h-full bg-gradient-to-r from-primary-500 to-primary-600"
                    initial={{ width: 0 }}
                    animate={{ width: `${uploadProgress}%` }}
                    transition={{ duration: 0.3 }}
                  />
                </div>
              </div>
            )}
            
            {uploadProgress === 100 && (
              <div className="flex items-center space-x-2 text-accent-600 mb-4">
                <div className="w-5 h-5 rounded-full bg-accent-600 flex items-center justify-center">
                  <svg className="w-3 h-3 text-white" fill="none" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" viewBox="0 0 24 24" stroke="currentColor">
                    <path d="M5 13l4 4L19 7"></path>
                  </svg>
                </div>
                <span className="font-medium">Téléchargement terminé!</span>
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
      
      {error && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start space-x-3"
        >
          <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
          <p className="text-red-800">{error}</p>
        </motion.div>
      )}
    </div>
  );
};

export default FileUpload;
