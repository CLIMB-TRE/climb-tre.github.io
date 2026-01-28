# HPRU GRE TB Uploader Specification

## Files to be provided

Suppliers must provide:

* A VCF file containing the variant calls for the consensus sequence.
* A FASTA file containing the consensus sequence in FASTA format.
* A CSV file containing the metadata associated with sequencing the sample.


## File naming convention

The base filenames should be of the form

```
hprugretb.[run_index].[run_id].[extension]
```

where:

* `[run_index]` is an identifier that is unique within a sequencing run, e.g. a sequencing barcode identifier, or a 96-well plate co-ordinate.
* `[run_id]` is the name of the sequencing run as given by the supplier's sequencing instrument (not an internal identifier assigned by the supplier).
* `[extension]` is the file extension indicating the file type.

**ALL** files must be uploaded to the root of the bucket, meaning that subdirectories cannot be used. Any file inside of a subdirectory of a bucket **will** be ignored.

## File name extensions

The extensions (`[extension]`) should be:

* `vcf` for the VCF file.
* `fasta` for the FASTA file.
* `csv` for the CSV metadata file.

## Platforms

As only consensus sequences are used in this project the sequencing platform is less relevant so there is only one "platform", `noplatform`.

## Valid characters

The `[run_index]`, `[run_id]` and `[extension]` must contain only:

* Letters (`A-Z`, `a-z`).
* Numbers (`0-9`).
* Hyphens (`-`).
* Underscores (`_`).

## Buckets

Bucket names follow the general convention:

```
hprugretb-[sequencing_org]-noplatform-[test_flag]
```

If you upload your data to an incorrect bucket, it will not be processed or in the worst case may be processed incorrectly, **it is your responsibility to ensure that your data is uploaded correctly!**

## Metadata specification

### CSV Template

A CSV template for uploaders can be downloaded here: [hprugretb-template.csv](hprugretb-template.csv){:download=hprugretb-template.csv}
