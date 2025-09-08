---
layout: docpost
title: mSCAPE DIPI Changelog
date_published: 2025-03-06 11:30:00 +0000
date_modified:  2025-05-08 13:12:00 +0000
author: rmcolq
maintainer: rmcolq
logo: assets/dipi-patch.png
logo_alt: CLIMB-TRE mSCAPE DIPI Mission Patch
---

# mSCAPE Changelog

All notable changes to CLIMB-TRE mSCAPE APIs, data or interchange formats that have impact to users or other pipelines should be documented in this file.
Changes described here may only be a subset of all changes to a project as this log concerns itself only with changes that impact how data is provided or consumed by users or other pipelines.

The following DIPI projects are routinely using this CHANGELOG:

* `Scylla` -- ingest analysis pipeline
* `Roz` -- ingest management
* `Onyx` -- metadata database
* `Onyx-client` -- API for interacting with metadata database

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

Issues can be reported to the [mSCAPE DIPI group](https://github.com/CLIMB-TRE/mscape-dipi-group).

***

## 2025-08-05
### Onyx
#### Added
* Added `spike_in` option `bacillus_ms2phage`.

## 2025-07-02
### Onyx
#### Added
* Added `total_bases` field, for recording the number of bases in the input FASTQ file(s), before any filtering.
* Added `taxa_files.total_bases` field, for recording the number of bases extracted for a taxa (assignable for each taxa within the `taxa_files` of a record).

## 2025-05-08
### Scylla
Released version 2.0.0. Given the number of changes, they are grouped by category rather than Added/Changed etc. 

#### HCID changes
* Add `min_coverage` parameter to HCID JSON
* Update references in HCID JSON and reference file
* Update thresholds for HCID detection
* Drop requirement for classified reads at taxon/parent level for HCID to be detected (mapping sufficient)
* Output reads corresponding to HCIDs which have flagged a warning (NEW OUTPUT in `qc/<taxid>.reads.fq`)
* Output read stats for HCID reads to the warning JSON (`mapped_mean_quality` and `mapped_mean_length`)
* Add coverage information for HCID found showing how many bases have coverage at each level - in HCID JSON

#### Extract taxa changes
* Reworked code to interact with kraken reports and assignment files during extract steps. Found a bug where some of the counts in the summary had previously been double counted (where both a S and S1 or S2 level taxa were extracted)
* Extract reads at different levels for different domains as specified by config (`F` for Viruses, `G` for everything else)
* Only extract reads at the specific level, not sublevels (e.g. S not S1 or S2)
* Add `total_len` calculated both for input and extracted output files in the summary JSON (NEW OUTPUT `qc/total_length.json`)
* Make extraction percentages domain-specific (e.g. 1% of bacterial reads rather than 1% of classified reads) to fix zepto example
* To extract a taxon, needs to pass count threshold OR the percentage threshold (previously both) and increase the count threshold for bacteria to 500

#### Workflow changes
* Add workflow to reclassify the viral+unclassified fraction with a second database
* In the process, the parameters associated with kraken databases have been restructured. Replace `--k2_host` with `--kraken_database.default.host`, `--k2_port` with `--kraken_database.default.port`, `--database` with `--kraken_database.default.path` and `database_set` is now `kraken_database.default.name`. This allows a second dictionary of kraken parameters for `kraken_database.virus` to be defined if/when necessary.
* Add code to merge kraken assignment files, giving preference to second assignment file
* Add code to update kraken report, giving list of changes made to assignments 
* Add a QC script to check the input file where a single fastq file is provided, so that it can warn if there are duplicate headers. This was seen in some example data and would cause big problems for the viral reclassification step when run, as read names need to be unique. If it finds duplicate/unexpectedly interleaved files, tries to correct them but then exists. The user can try rerunning with the fixed files. I considered silently handling but this approach seemed dangerous.
* Add messaging if paired reads provided and `--paired` not.
* Add a workflow to run modules (use `--module <name>`) and remove workflow definitions from within these modules
* Add a warning for incorrect Phred parsing as this is thought to be a resolved issue

#### Nextflow changes
* set `docker.userEmulation   = true`

#### Other changes
* Add to README more helpful
* Review all local test commands and make sure they run as expected.

## 2025-03-31
### Onyx
#### Added
* Added `nuth` (Newcastle upon Tyne Hospitals NHS Foundation Trust) as an option in the mSCAPE `site` field. 

## 2025-03-06
### All
* Start of changelog
