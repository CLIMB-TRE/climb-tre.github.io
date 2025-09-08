# PATH-SAFE Uploader Specification

## Files to be provided

* A FASTQ 1 file containing the forward sequencing reads.
* A FASTQ 2 file containing the reverse sequencing reads.
* A CSV file containing the metadata associated with sequencing the sample.

## File naming convention

The base filenames should be of the form

```
pathsafe.[run_index].[run_id].[extension]
```

where:

* `[run_index]` is an identifier that is unique within a sequencing run, e.g. a sequencing barcode identifier, or a 96-well plate co-ordinate.
* `[run_id]` is the name of the sequencing run as given by the supplier's sequencing instrument (not an internal identifier assigned by the supplier).
* `[extension]` is the file extension indicating the file type.

## File name extensions

The extensions (`[extension]`) should be:

* `1.fastq.gz` for the forward FASTQ file.
* `2.fastq.gz` for the reverse FASTQ file.
* `csv` for the CSV metadata file.

## Valid characters

The `[run_index]`, `[run_id]` and `[extension]` must contain only:

* Letters (`A-Z`, `a-z`).
* Numbers (`0-9`).
* Hyphens (`-`).
* Underscores (`_`).

## Metadata specification

### CSV Template

A CSV template for uploaders can be downloaded here: [pathsafe-template.csv](pathsafe-template.csv){:download=pathsafe-template.csv}
