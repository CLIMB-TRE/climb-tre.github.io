# synthSCAPE Uploader Specification

## Files to be provided

For _paired-end Illumina_ sequencing data, suppliers must provide:

- A FASTQ 1 file containing the forward sequencing reads.
- A FASTQ 2 file containing the reverse sequencing reads.
- A CSV file containing the metadata associated with sequencing the sample.

For _single-end Illumina_ sequencing data, suppliers must provide:

- A FASTQ file containing the sequencing reads.
- A CSV file containing the metadata associated with sequencing the sample.

For _ONT_ sequencing data, suppliers must provide:

- A FASTQ file containing the sequencing reads.
- A CSV file containing the metadata associated with sequencing the sample.

Sequencing data must be dehumanised prior to submission. The ingest pipeline
will reject sequencing data where the number of assigned human reads exceeds the
human read rejection threshold.

## File naming convention

The base filenames should be of the form

```
synthscape.[run_index].[run_id].[extension]
```

where:

- `[run_index]` is an identifier that is unique within a sequencing run, e.g. a sequencing barcode identifier, or a 96-well plate co-ordinate.
- `[run_id]` is the name of the sequencing run as given by the supplier's sequencing instrument (not an internal identifier assigned by the supplier).
- `[extension]` is the file extension indicating the file type.

## File name extensions

For _paired-end Illumina_ sequencing data, the extensions (`[extension]`) should be:

- `1.fastq.gz` for the forward FASTQ file.
- `2.fastq.gz` for the reverse FASTQ file.
- `csv` for the CSV metadata file.

For _single-end Illumina_ sequencing data, the extensions (`[extension]`) should be:

- `fastq.gz` for the forward FASTQ file.
- `csv` for the CSV metadata file.

For _ONT_ sequencing data, the extensions (`[extension]`) should be:

- `fastq.gz` for the forward FASTQ file.
- `csv` for the CSV metadata file.

## Valid characters

The `[run_index]`, `[run_id]` and `[extension]` must contain only:

- Letters (`A-Z`, `a-z`).
- Numbers (`0-9`).
- Hyphens (`-`).
- Underscores (`_`).

## Buckets

Bucket names follow the general convention:

```
synthscape-[sequencing_org]-[platform]-[test_flag]
```

## Metadata specification

### CSV Template

A CSV template for uploaders can be downloaded here: [synthscape-template.csv](synthscape-template.csv){:download=synthscape-template.csv}
