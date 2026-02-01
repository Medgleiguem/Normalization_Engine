#!/usr/bin/env node

/**
 * Professional Database Normalization Report Generator using docx-js
 * Generates university-standard academic reports with proper formatting
 */

const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        HeadingLevel, AlignmentType, BorderStyle, WidthType, ShadingType,
        PageBreak, LevelFormat } = require('docx');
const fs = require('fs');

// Read analysis result from stdin or file
function readAnalysisData() {
    const args = process.argv.slice(2);
    if (args.length < 1) {
        console.error('Usage: node report_generator.js <analysis_json_file> <output_docx>');
        process.exit(1);
    }
    
    const dataFile = args[0];
    const outputFile = args[1] || 'normalization_report.docx';
    
    const data = JSON.parse(fs.readFileSync(dataFile, 'utf8'));
    return { data, outputFile };
}

// Generate the complete report
function generateReport(analysisResult) {
    const doc = new Document({
        styles: {
            default: {
                document: {
                    run: { font: "Arial", size: 24 } // 12pt
                }
            },
            paragraphStyles: [
                {
                    id: "Heading1",
                    name: "Heading 1",
                    basedOn: "Normal",
                    next: "Normal",
                    quickFormat: true,
                    run: { size: 32, bold: true, font: "Arial", color: "003366" },
                    paragraph: { spacing: { before: 480, after: 240 }, outlineLevel: 0 }
                },
                {
                    id: "Heading2",
                    name: "Heading 2",
                    basedOn: "Normal",
                    next: "Normal",
                    quickFormat: true,
                    run: { size: 28, bold: true, font: "Arial", color: "003366" },
                    paragraph: { spacing: { before: 360, after: 180 }, outlineLevel: 1 }
                },
                {
                    id: "Heading3",
                    name: "Heading 3",
                    basedOn: "Normal",
                    next: "Normal",
                    quickFormat: true,
                    run: { size: 26, bold: true, font: "Arial", color: "003366" },
                    paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 2 }
                }
            ]
        },
        numbering: {
            config: [
                {
                    reference: "bullets",
                    levels: [{
                        level: 0,
                        format: LevelFormat.BULLET,
                        text: "•",
                        alignment: AlignmentType.LEFT,
                        style: { paragraph: { indent: { left: 720, hanging: 360 } } }
                    }]
                },
                {
                    reference: "numbers",
                    levels: [{
                        level: 0,
                        format: LevelFormat.DECIMAL,
                        text: "%1.",
                        alignment: AlignmentType.LEFT,
                        style: { paragraph: { indent: { left: 720, hanging: 360 } } }
                    }]
                }
            ]
        },
        sections: [{
            properties: {
                page: {
                    size: { width: 12240, height: 15840 }, // US Letter
                    margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
                }
            },
            children: [
                // Title Page
                ...generateTitlePage(analysisResult),
                new Paragraph({ children: [new PageBreak()] }),
                
                // Executive Summary
                ...generateExecutiveSummary(analysisResult),
                new Paragraph({ children: [new PageBreak()] }),
                
                // Original Table Analysis
                ...generateOriginalTableAnalysis(analysisResult),
                new Paragraph({ children: [new PageBreak()] }),
                
                // Normalization Process
                ...generateNormalizationProcess(analysisResult),
                new Paragraph({ children: [new PageBreak()] }),
                
                // Final Schema
                ...generateFinalSchema(analysisResult),
                new Paragraph({ children: [new PageBreak()] }),
                
                // Theoretical Background
                ...generateTheoreticalBackground(),
                new Paragraph({ children: [new PageBreak()] }),
                
                // Conclusion
                ...generateConclusion(analysisResult),
                new Paragraph({ children: [new PageBreak()] }),
                
                // References
                ...generateReferences()
            ]
        }]
    });
    
    return doc;
}

function generateTitlePage(analysisResult) {
    const today = new Date().toLocaleDateString('en-US', { 
        year: 'numeric', month: 'long', day: 'numeric' 
    });
    
    return [
        new Paragraph({
            heading: HeadingLevel.HEADING_1,
            alignment: AlignmentType.CENTER,
            spacing: { before: 2880, after: 480 },
            children: [new TextRun("Database Normalization Analysis Report")]
        }),
        new Paragraph({
            alignment: AlignmentType.CENTER,
            spacing: { after: 960 },
            children: [new TextRun({
                text: `Analysis of: ${analysisResult.original_table}`,
                bold: true,
                size: 28
            })]
        }),
        new Paragraph({
            alignment: AlignmentType.CENTER,
            spacing: { after: 240 },
            children: [new TextRun(`Generated: ${today}`)]
        }),
        new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [new TextRun(`Analysis ID: ${analysisResult.analysis_id || 'N/A'}`)]
        }),
        new Paragraph({
            alignment: AlignmentType.CENTER,
            spacing: { before: 480 },
            children: [new TextRun({
                text: `Final Normal Form Achieved: ${analysisResult.final_nf}`,
                bold: true,
                size: 26,
                color: "22C55E"
            })]
        })
    ];
}

function generateExecutiveSummary(analysisResult) {
    return [
        new Paragraph({
            heading: HeadingLevel.HEADING_1,
            children: [new TextRun("Executive Summary")]
        }),
        new Paragraph({
            spacing: { after: 240 },
            children: [new TextRun(
                `This report presents a comprehensive analysis of the database normalization process ` +
                `applied to the '${analysisResult.original_table}' dataset. The analysis identified ` +
                `the original table's compliance with normal forms and systematically applied normalization ` +
                `techniques to achieve ${analysisResult.final_nf}.`
            )]
        }),
        new Paragraph({
            spacing: { before: 240, after: 120 },
            children: [new TextRun({ text: "Key Findings:", bold: true })]
        }),
        new Paragraph({
            numbering: { reference: "bullets", level: 0 },
            children: [new TextRun(`Original Normal Form: ${analysisResult.original_nf}`)]
        }),
        new Paragraph({
            numbering: { reference: "bullets", level: 0 },
            children: [new TextRun(`Target Normal Form: ${analysisResult.final_nf}`)]
        }),
        new Paragraph({
            numbering: { reference: "bullets", level: 0 },
            children: [new TextRun(`Normalization Steps Applied: ${analysisResult.steps_count}`)]
        }),
        new Paragraph({
            numbering: { reference: "bullets", level: 0 },
            children: [new TextRun(`Final Number of Tables: ${analysisResult.tables_count}`)]
        }),
        new Paragraph({
            numbering: { reference: "bullets", level: 0 },
            children: [new TextRun(`Total Violations Resolved: ${analysisResult.violations_count}`)]
        }),
        new Paragraph({
            spacing: { before: 240 },
            children: [new TextRun(
                "The normalization process successfully eliminated data redundancy, improved data integrity, " +
                "and optimized the database structure for efficient querying and maintenance."
            )]
        })
    ];
}

function generateOriginalTableAnalysis(analysisResult) {
    const paragraphs = [
        new Paragraph({
            heading: HeadingLevel.HEADING_1,
            children: [new TextRun("Original Table Analysis")]
        }),
        new Paragraph({
            heading: HeadingLevel.HEADING_2,
            children: [new TextRun("Table Structure")]
        }),
        new Paragraph({
            children: [new TextRun(`Table Name: ${analysisResult.original_table}`)]
        }),
        new Paragraph({
            children: [new TextRun(`Current Normal Form: ${analysisResult.original_nf}`)]
        })
    ];
    
    return paragraphs;
}

function generateNormalizationProcess(analysisResult) {
    const paragraphs = [
        new Paragraph({
            heading: HeadingLevel.HEADING_1,
            children: [new TextRun("Normalization Process")]
        }),
        new Paragraph({
            spacing: { after: 240 },
            children: [new TextRun(
                "The following sections detail each normalization step applied to achieve the target normal form."
            )]
        })
    ];
    
    // Add each step
    if (analysisResult.steps && analysisResult.steps.length > 0) {
        analysisResult.steps.forEach((step, index) => {
            paragraphs.push(
                new Paragraph({
                    heading: HeadingLevel.HEADING_2,
                    children: [new TextRun(`Step ${index + 1}: ${step.from_nf} → ${step.to_nf}`)]
                }),
                new Paragraph({
                    spacing: { after: 120 },
                    children: [new TextRun(step.explanation || "No explanation provided.")]
                }),
                new Paragraph({
                    spacing: { before: 120 },
                    children: [new TextRun({
                        text: `Violations Found: ${step.violations || 0}`,
                        bold: true
                    })]
                })
            );
        });
    } else {
        paragraphs.push(
            new Paragraph({
                children: [new TextRun("No normalization steps were required. Table already in optimal form.")]
            })
        );
    }
    
    return paragraphs;
}

function generateFinalSchema(analysisResult) {
    return [
        new Paragraph({
            heading: HeadingLevel.HEADING_1,
            children: [new TextRun("Final Normalized Schema")]
        }),
        new Paragraph({
            spacing: { after: 240 },
            children: [new TextRun(
                `The normalization process resulted in ${analysisResult.tables_count} table(s) that comply ` +
                `with ${analysisResult.final_nf}.`
            )]
        })
    ];
}

function generateTheoreticalBackground() {
    return [
        new Paragraph({
            heading: HeadingLevel.HEADING_1,
            children: [new TextRun("Theoretical Background")]
        }),
        new Paragraph({
            spacing: { after: 240 },
            children: [new TextRun(
                "Database normalization is a systematic approach to organizing data in a relational database " +
                "to reduce redundancy and improve data integrity. The process involves decomposing tables into " +
                "smaller, well-structured tables without losing information."
            )]
        }),
        new Paragraph({
            heading: HeadingLevel.HEADING_2,
            children: [new TextRun("Normal Forms")]
        }),
        new Paragraph({
            heading: HeadingLevel.HEADING_3,
            children: [new TextRun("First Normal Form (1NF)")]
        }),
        new Paragraph({
            numbering: { reference: "bullets", level: 0 },
            children: [new TextRun("All column values must be atomic (indivisible)")]
        }),
        new Paragraph({
            numbering: { reference: "bullets", level: 0 },
            children: [new TextRun("No repeating groups or arrays")]
        }),
        new Paragraph({
            numbering: { reference: "bullets", level: 0 },
            children: [new TextRun("Each column contains values of a single type")]
        }),
        new Paragraph({
            heading: HeadingLevel.HEADING_3,
            spacing: { before: 240 },
            children: [new TextRun("Second Normal Form (2NF)")]
        }),
        new Paragraph({
            numbering: { reference: "bullets", level: 0 },
            children: [new TextRun("Must satisfy 1NF")]
        }),
        new Paragraph({
            numbering: { reference: "bullets", level: 0 },
            children: [new TextRun("No partial dependencies (all non-key attributes must depend on the entire primary key)")]
        }),
        new Paragraph({
            heading: HeadingLevel.HEADING_3,
            spacing: { before: 240 },
            children: [new TextRun("Third Normal Form (3NF)")]
        }),
        new Paragraph({
            numbering: { reference: "bullets", level: 0 },
            children: [new TextRun("Must satisfy 2NF")]
        }),
        new Paragraph({
            numbering: { reference: "bullets", level: 0 },
            children: [new TextRun("No transitive dependencies (non-key attributes must not depend on other non-key attributes)")]
        }),
        new Paragraph({
            spacing: { before: 360, after: 120 },
            children: [new TextRun({ text: "Benefits of Normalization:", bold: true })]
        }),
        new Paragraph({
            numbering: { reference: "bullets", level: 0 },
            children: [new TextRun("Eliminates data redundancy")]
        }),
        new Paragraph({
            numbering: { reference: "bullets", level: 0 },
            children: [new TextRun("Improves data integrity and consistency")]
        }),
        new Paragraph({
            numbering: { reference: "bullets", level: 0 },
            children: [new TextRun("Reduces update, insertion, and deletion anomalies")]
        }),
        new Paragraph({
            numbering: { reference: "bullets", level: 0 },
            children: [new TextRun("Optimizes storage efficiency")]
        }),
        new Paragraph({
            numbering: { reference: "bullets", level: 0 },
            children: [new TextRun("Enhances query performance")]
        })
    ];
}

function generateConclusion(analysisResult) {
    return [
        new Paragraph({
            heading: HeadingLevel.HEADING_1,
            children: [new TextRun("Conclusion")]
        }),
        new Paragraph({
            children: [new TextRun(
                `This analysis successfully normalized the '${analysisResult.original_table}' dataset from ` +
                `${analysisResult.original_nf} to ${analysisResult.final_nf}. The process identified and ` +
                `resolved ${analysisResult.violations_count} normalization violations, resulting in a ` +
                `well-structured database schema comprising ${analysisResult.tables_count} table(s).`
            )]
        }),
        new Paragraph({
            spacing: { before: 240, after: 120 },
            children: [new TextRun({ text: "The normalized schema provides:", bold: true })]
        }),
        new Paragraph({
            numbering: { reference: "bullets", level: 0 },
            children: [new TextRun("Enhanced data integrity through elimination of redundancy")]
        }),
        new Paragraph({
            numbering: { reference: "bullets", level: 0 },
            children: [new TextRun("Improved query performance via optimized table structures")]
        }),
        new Paragraph({
            numbering: { reference: "bullets", level: 0 },
            children: [new TextRun("Reduced storage requirements")]
        }),
        new Paragraph({
            numbering: { reference: "bullets", level: 0 },
            children: [new TextRun("Simplified maintenance and updates")]
        }),
        new Paragraph({
            numbering: { reference: "bullets", level: 0 },
            children: [new TextRun("Compliance with database design best practices")]
        }),
        new Paragraph({
            spacing: { before: 240 },
            children: [new TextRun(
                "The accompanying MySQL script implements this normalized schema with proper constraints, " +
                "indexes, and documentation, ready for deployment in a production environment."
            )]
        })
    ];
}

function generateReferences() {
    const references = [
        'Codd, E. F. (1970). "A Relational Model of Data for Large Shared Data Banks". Communications of the ACM.',
        'Date, C. J. (2003). "An Introduction to Database Systems" (8th ed.). Addison-Wesley.',
        'Elmasri, R., & Navathe, S. B. (2015). "Fundamentals of Database Systems" (7th ed.). Pearson.',
        'Kent, W. (1983). "A Simple Guide to Five Normal Forms in Relational Database Theory". Communications of the ACM.',
        'Silberschatz, A., Korth, H. F., & Sudarshan, S. (2019). "Database System Concepts" (7th ed.). McGraw-Hill.'
    ];
    
    const paragraphs = [
        new Paragraph({
            heading: HeadingLevel.HEADING_1,
            children: [new TextRun("References")]
        })
    ];
    
    references.forEach((ref, index) => {
        paragraphs.push(
            new Paragraph({
                spacing: { after: 120 },
                children: [new TextRun(`[${index + 1}] ${ref}`)]
            })
        );
    });
    
    return paragraphs;
}

// Main execution
async function main() {
    try {
        const { data, outputFile } = readAnalysisData();
        console.log('Generating report...');
        
        const doc = generateReport(data);
        const buffer = await Packer.toBuffer(doc);
        
        fs.writeFileSync(outputFile, buffer);
        console.log(`Report generated successfully: ${outputFile}`);
        
        // Output success JSON for Python to parse
        console.log(JSON.stringify({ success: true, output: outputFile }));
    } catch (error) {
        console.error('Error generating report:', error);
        console.error(JSON.stringify({ success: false, error: error.message }));
        process.exit(1);
    }
}

if (require.main === module) {
    main();
}

module.exports = { generateReport };
