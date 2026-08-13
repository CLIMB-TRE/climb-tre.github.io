# synthSCAPE Downstream Analyses Specification

A **downstream analysis** is a record of a pipeline run carried out on data already
held in Onyx. It is a distinct object type from a project record: an analysis
describes *how* a result was produced (pipeline, version, command, methods) and
*what* it produced (result, metrics, report, outputs), and links back to the
project records it was produced from and to any upstream analyses it was derived
from.

Analyses are identified by an `analysis_id` of the form `A-XXXXXXXXXX`, assigned
automatically by Onyx on submission.

The **Submission Specification** below lists the fields that can be provided when
creating or updating an analysis. The **Read Specification** lists all fields
visible when retrieving an analysis, including those assigned by Onyx.

