#!/usr/bin/env python3
"""
Process All Creatio Academy Videos
Comprehensive processing script with optimized settings for the complete video library
"""

import os
import sys
import subprocess
import logging
from pathlib import Path
from datetime import datetime

def setup_logging():
    """Setup comprehensive logging"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"full_processing_{timestamp}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

def run_command(cmd, logger):
    """Run command and log output"""
    logger.info(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        logger.info("Command completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {e}")
        logger.error(f"Error output: {e.stderr}")
        return False

def main():
    logger = setup_logging()
    
    logger.info("=" * 80)
    logger.info("CREATIO ACADEMY VIDEO PROCESSING - FULL BATCH")
    logger.info("=" * 80)
    
    # Configuration
    base_dir = Path(__file__).parent
    video_dirs = [
        "downloads",
        ".",  # Current directory for any other videos
    ]
    
    output_dir = "creatio_academy_transcriptions"
    whisper_model = "base"  # Good balance of speed and accuracy
    
    logger.info(f"Base directory: {base_dir}")
    logger.info(f"Output directory: {output_dir}")
    logger.info(f"Whisper model: {whisper_model}")
    
    # Activate virtual environment
    venv_python = base_dir / "venv" / "bin" / "python"
    if not venv_python.exists():
        logger.error("Virtual environment not found. Please run setup first.")
        return False
    
    total_processed = 0
    total_failed = 0
    
    # Process each video directory
    for video_dir in video_dirs:
        video_path = base_dir / video_dir
        
        if not video_path.exists():
            logger.warning(f"Video directory not found: {video_path}")
            continue
        
        logger.info(f"\n{'='*60}")
        logger.info(f"PROCESSING DIRECTORY: {video_path}")
        logger.info(f"{'='*60}")
        
        # First, do a dry run to see what we have
        logger.info("Performing dry run to count files...")
        dry_run_cmd = [
            str(venv_python), "batch_transcribe.py", str(video_path),
            "--model", whisper_model,
            "--output", output_dir,
            "--dry-run"
        ]
        
        if not run_command(dry_run_cmd, logger):
            logger.error(f"Dry run failed for {video_path}")
            continue
        
        # Process the directory with enhanced summaries
        logger.info("Starting full processing with enhanced summaries...")
        process_cmd = [
            str(venv_python), "batch_transcribe.py", str(video_path),
            "--model", whisper_model,
            "--output", output_dir,
            "--enhance",
            "--verbose"
        ]
        
        if run_command(process_cmd, logger):
            logger.info(f"Successfully processed {video_path}")
            total_processed += 1
        else:
            logger.error(f"Failed to process {video_path}")
            total_failed += 1
    
    # Generate final report
    logger.info("\n" + "="*80)
    logger.info("PROCESSING COMPLETE - FINAL SUMMARY")
    logger.info("="*80)
    
    logger.info(f"Directories processed: {total_processed}")
    logger.info(f"Directories failed: {total_failed}")
    
    # Check output statistics
    output_path = base_dir / output_dir
    if output_path.exists():
        transcript_count = len(list((output_path / "transcripts").glob("*.txt")))
        metadata_count = len(list((output_path / "metadata").glob("*.yaml")))
        summary_count = len(list((output_path / "summaries").glob("*.json")))
        enhanced_count = len(list((output_path / "summaries").glob("*_enhanced_summary.json")))
        
        logger.info(f"\nOutput Statistics:")
        logger.info(f"  - Transcripts: {transcript_count}")
        logger.info(f"  - Metadata files: {metadata_count}")
        logger.info(f"  - Basic summaries: {summary_count}")
        logger.info(f"  - Enhanced summaries: {enhanced_count}")
        logger.info(f"  - Output directory: {output_path.absolute()}")
    
    # Provide next steps
    logger.info(f"\nNext Steps:")
    logger.info(f"1. Review processing logs for any errors")
    logger.info(f"2. Check output files in: {output_path.absolute()}")
    logger.info(f"3. Verify transcription quality for important videos")
    logger.info(f"4. Consider reprocessing failed videos individually")
    logger.info(f"5. Use structured metadata for search and organization")
    
    logger.info(f"\nProcessing completed at: {datetime.now()}")
    
    return total_failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
