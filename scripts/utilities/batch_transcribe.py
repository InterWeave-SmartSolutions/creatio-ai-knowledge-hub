#!/usr/bin/env python3
"""
Batch Video Transcription Script
Process multiple videos with different options and configurations
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from transcription_processor import TranscriptionProcessor
from llm_summarizer import enhance_existing_summaries

def setup_logging(verbose: bool = False):
    """Setup logging configuration"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('batch_transcription.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def main():
    parser = argparse.ArgumentParser(
        description="Batch process videos for transcription and metadata",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process current directory with default settings
  python batch_transcribe.py .
  
  # Process with larger Whisper model for better accuracy
  python batch_transcribe.py ./downloads --model large
  
  # Process only first 3 files for testing
  python batch_transcribe.py ./downloads --max-files 3
  
  # Process with enhanced LLM summaries
  python batch_transcribe.py ./downloads --enhance
  
  # Process specific directory with custom output
  python batch_transcribe.py ./videos --output ./processed_transcripts
        """
    )
    
    parser.add_argument(
        "input_directory", 
        help="Directory containing video files to process"
    )
    
    parser.add_argument(
        "--model", 
        default="base",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model size (default: base). Larger models are more accurate but slower."
    )
    
    parser.add_argument(
        "--output", 
        default="transcriptions",
        help="Output directory for transcriptions and metadata (default: transcriptions)"
    )
    
    parser.add_argument(
        "--max-files", 
        type=int,
        help="Maximum number of files to process (useful for testing)"
    )
    
    parser.add_argument(
        "--enhance", 
        action="store_true",
        help="Generate enhanced summaries using LLM analysis"
    )
    
    parser.add_argument(
        "--force", 
        action="store_true",
        help="Force reprocessing of already processed files"
    )
    
    parser.add_argument(
        "--verbose", 
        action="store_true",
        help="Enable verbose logging"
    )
    
    parser.add_argument(
        "--dry-run", 
        action="store_true",
        help="Show what would be processed without actually processing"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    # Validate input directory
    input_path = Path(args.input_directory)
    if not input_path.exists():
        logger.error(f"Input directory does not exist: {input_path}")
        sys.exit(1)
    
    if not input_path.is_dir():
        logger.error(f"Input path is not a directory: {input_path}")
        sys.exit(1)
    
    # Create output directory
    output_path = Path(args.output)
    output_path.mkdir(exist_ok=True)
    
    logger.info(f"Starting batch transcription processing")
    logger.info(f"Input directory: {input_path.absolute()}")
    logger.info(f"Output directory: {output_path.absolute()}")
    logger.info(f"Whisper model: {args.model}")
    logger.info(f"Max files: {args.max_files or 'unlimited'}")
    logger.info(f"Enhanced summaries: {'Yes' if args.enhance else 'No'}")
    
    try:
        # Initialize processor
        processor = TranscriptionProcessor(
            whisper_model=args.model, 
            output_dir=str(output_path)
        )
        
        # Find video files
        video_files = processor.find_video_files(str(input_path))
        
        if not video_files:
            logger.warning("No video files found in the specified directory")
            return
        
        if args.max_files:
            video_files = video_files[:args.max_files]
            logger.info(f"Limited to first {args.max_files} files")
        
        # Show what will be processed
        logger.info(f"Found {len(video_files)} video files to process:")
        for i, video_file in enumerate(video_files, 1):
            size_mb = video_file.stat().st_size / (1024 * 1024)
            logger.info(f"  {i}. {video_file.name} ({size_mb:.1f} MB)")
        
        if args.dry_run:
            logger.info("Dry run mode - no files will be processed")
            return
        
        # Process files
        if args.force:
            # Remove existing metadata files to force reprocessing
            metadata_dir = output_path / "metadata"
            if metadata_dir.exists():
                for metadata_file in metadata_dir.glob("*.yaml"):
                    logger.info(f"Removing existing metadata: {metadata_file}")
                    metadata_file.unlink()
        
        # Process videos
        processor.process_directory(str(input_path), max_files=args.max_files)
        
        # Generate enhanced summaries if requested
        if args.enhance:
            logger.info("Generating enhanced summaries with LLM analysis...")
            enhance_existing_summaries(str(output_path))
        
        # Generate final report
        logger.info("=" * 60)
        logger.info("BATCH PROCESSING COMPLETE")
        logger.info("=" * 60)
        
        # Count output files
        output_counts = {
            "transcripts": len(list((output_path / "transcripts").glob("*.txt"))),
            "metadata": len(list((output_path / "metadata").glob("*.yaml"))),
            "summaries": len(list((output_path / "summaries").glob("*.json"))),
            "enhanced": len(list((output_path / "summaries").glob("*_enhanced_summary.json"))) if args.enhance else 0,
        }
        
        logger.info(f"Generated files:")
        logger.info(f"  - Transcripts: {output_counts['transcripts']}")
        logger.info(f"  - Metadata files: {output_counts['metadata']}")
        logger.info(f"  - Basic summaries: {output_counts['summaries']}")
        if args.enhance:
            logger.info(f"  - Enhanced summaries: {output_counts['enhanced']}")
        
        logger.info(f"All files saved to: {output_path.absolute()}")
        logger.info("Processing completed successfully!")
        
    except KeyboardInterrupt:
        logger.info("Processing interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error during processing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
