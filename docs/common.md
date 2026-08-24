# Project specification structure

## Overview

All projects on CLIMB-TRE are specified in the same way.

## Files to be provided

These are the files that must be uploaded (usually some sequencing reads and a metadata file).
Submissions without the correct number of files provided will be considered incomplete and will not be processed.

## File naming convention

This is the convention to which the provided file names must adhere.

Each of the files to be provided will use the same basename followed by specified extensions (e.g. for data versus metadata). 
The basename for each file is usually several fields separated by a fixed number of stops/periods (`.`).

The set of valid characters is usually limited to letters, numbers, hyphens (`-`) and underscores (`_`) but this will be specified.
Filenames containing forbidden characters or extensions will not be processed.

## File processing requirements

### FASTQ

* Must be gzipped.
* Must adhere to the FASTQ format.

### CSV

* Must be a plain text file with comma-delimited data.
* Must contain two rows: the first will contain the column names and the second will contain the data.
* Must have column names that match the specification exactly.
* Must not have missing data for required fields.
* Must not have invalid data (e.g. `"N/A"`) to circumvent missing data checks.
* Must not contain metadata that contradicts the file name.
* Must use the latest version of the metadata specification.

## Metadata specification

The metadata for each project is specified in tables detailing required fields (which must not be empty) and optional fields (which can be left empty).

## Project upload buckets

Files should be uploaded to S3 buckets hosted at the [`s3.climb.ac.uk`](https://s3.climb.ac.uk) endpoint. 

The bucket names are a combination of:

* Project (e.g. `mscape`).
* Your site code (issued to you when your site is onboarded).
* Platform (e.g. `illumina`).
* A flag that indicates a test (`test`) or production (`prod`) submission.

All files must be placed in the root directory of the submission buckets.
Any S3 URI containing a directory will be ignored.