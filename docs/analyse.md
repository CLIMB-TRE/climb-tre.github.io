# Analysing data

## Overview

Once data and metadata have been ingested into the Onyx database, you
can query it using the Onyx client, which provides a command line interface (CLI)
and Python API.  This short example
demonstrates a few principal functions.  More are described in the
[`onyx-client` documentation](https://climb-tre.github.io/onyx-client/).

This guide also assumes that you're using a Notebook Server on CLIMB,
so that once installed, the Onyx client will automatically be configured.

## Onyx client basics

First, let's install the Onyx client, which is available through the
[conda-forge package](https://anaconda.org/conda-forge/climb-onyx-client)
`climb-onyx-client` and can thus be installed
with `conda`.  As advised in the [CLIMB docs on installing
software](https://docs.climb.ac.uk/notebook-servers/installing-software-with-conda/),
you should install the client in a new Conda environment.
I'll name my environment `onyx` and install `climb-onyx-client`, as well as `ipykernel` (so that the client is available in my Jupyter Notebooks).
```
jovyan:~$ conda create -n onyx ipykernel climb-onyx-client
```
Let's activate this environment.
```
jovyan:~$ conda activate onyx
```
On Bryn's Notebook Servers, the client will automatically be configured.
We will now have access to both the Python API and a command-line client.
Let's walk through some of the commands available to us.
In each case you can choose between the Python API or the command-line interface (CLI).

### Initial setup

=== "CLI"
	No additional setup is required if you are running the CLI in a CLIMB
	notebook. You can try running the command-line client with

	```console
	(onyx) jovyan:~$ onyx
	```
	to see some of the options and commands available to you.

=== "Python"
	If you are using onyx in Python, then you need to import the required modules and configure a client.
	```python
	import os
	from onyx import OnyxConfig, OnyxEnv, OnyxClient

	config = OnyxConfig(
	    domain=os.environ[OnyxEnv.DOMAIN],
	    token=os.environ[OnyxEnv.TOKEN],
	)

	client = OnyxClient(config=config)
	```

	!!! note

	    In all the Python API examples, arguments will be
		explicitly passed as keyword arguments e.g. `arg=value`,
		however, in all cases shown on this page, the argument names 
		can be omitted.

### Profile

You can view information about your profile (username, site, and email) with

=== "CLI"

	```console
	(onyx) jovyan:~$ onyx profile
	```

=== "Python"

	```python
	client.profile()
	```

### Projects

You can view the projects you have access to with

=== "CLI"

	```console
	(onyx) jovyan:~$ onyx projects
	```

=== "Python"

	```python
	client.projects()
	```

## Querying data

As an example task, we'll see if we can find any sequencing data performed
for ZymoBIOMICS sources.  These are designed with
[a particular specification](https://files.zymoresearch.com/protocols/_d6300_zymobiomics_microbial_community_standard.pdf)
of DNA from eight bacteria and two yeasts.
We will search the `mscape` project, but bear in mind you may not
have access to that particular project.

To see every entry in the entire database for a particular project we can do

=== "CLI"

	```console
	(onyx) jovyan:~$ onyx filter mscape
	```

=== "Python"

	```python
	# client.filter returns a generator that we can iterate over
	entires = client.filter(project="mscape")
	```

On its own, this command queries the database with *no* filters, and
could return thousands of entries.

### Fields

We can see what fields exist in a particular database with

=== "CLI"

	```console
	(onyx) jovyan:~$ onyx fields mscape
	```

=== "Python"

	```python
	client.fields(project="mscape")
	```

### Filtering

We can filter the returned records to just select the entries in the
database that we are interested in. For this example we'll see if we
can find any sequencing data performed for ZymoBIOMICS sources.  These
are designed with [a particular
specification](https://files.zymoresearch.com/protocols/_d6300_zymobiomics_microbial_community_standard.pdf)
of DNA from eight bacteria and two yeasts.

To select these samples, we can ask that the `control_type_details`
equals `zymo-mc_D6300`.

=== "CLI"

	```console
	(onyx) jovyan:~$ onyx filter mscape --field control_type_details=zymo-mc_D6300
	```

=== "Python"

	```python
	# client.filter returns a generator that we can iterate over
    entries = client.filter(project="mscape", fields={"control_type_details": "zymo-mc_D6300"})
	```

This returns a small number of entries that we can more easily work
with. Note that this returns every field for each record that is
found, which can be much more information than we need. We can select
specific fields to include using e.g.

=== "CLI"

	```console
	(onyx) jovyan:~$ onyx filter mscape --field control_type_details=zymo-mc_D6300 --include climb_id,biosample_id,taxon_reports
	```

=== "Python"

	```python
	query = {"control_type_details": "zymo-mc_D6300"}
	fields_to_include = ["climb_id", "biosample_id" , "taxon_reports"]
	# client.filter returns a generator that we can iterate over
    entries = client.filter("mscape", fields=query, include=fields_to_include)
	```

### Taxonomic information

By default, the filter command will not return taxonomic
information. To access that information for an individual record use the `get` command.

=== "CLI"

	```console
	(onyx) jovyan:~$ onyx get mscape <CLIMB_ID>
	```

=== "Python"

	```python
	record = client.get(project="mscape", climb_id=<CLIMB_ID>)
	```
where `<CLIMB_ID>` is replaced with the CLIMB ID of the record you
want to retrieve.
This will you give you all the information about a particular record
including binned reads and all classifier calls.

## Tips

### `jq`

If you are using the CLI, you may find [`jq`](https://jqlang.org)
useful. `jq` can be installed into your conda environment

```console
(onyx) jovyan:~$ conda install jq
```
You can then pipe the output of your onyx queries
e.g. `onyx filter ...` into `jq` using the pipe operator `|`.
This will colourise the output and may make reading the data easier.
```console
(onyx) jovyan:~$ onyx filter mscape --field control_type_details=zymo-mc_D6300 | jq
```
`jq` has many powerful features, including filtering, selecting, and formatting data.


### Python context manager

If you are using the Python client, and performing more than one query to
the onyx database in a single code block e.g. in a `for` loop. Then we
recommend you use the `OnyxClient` as a context manager.

```python
# ...
# Setup omitted
# ...
client = OnyxClient(config=config)

# Perform several onyx operations in this block
with client:
	# Get the first entry in the database for the mscape project
    first_entry = next(client.filter(project="mscape"))
	
	# Get the CLIMB ID of the entry
    climb_id = first_entry["climb_id"]
	
	# Get the full record for this CLIMB ID using the `get` method
    full_record = client.get(project="mscape", climb_id=climb_id)
	
	# Count the number of taxa_files
    n_taxa_files = len(full_record["taxa_files"])
    print(f"CLIMB_ID: {climb_id} has {n_taxa_files} taxa files")
```

This is more efficient that not using the context manager as the
client will re-use the same session for all requests, rather than
creating a new session for each request. For more information, see:
<https://requests.readthedocs.io/en/master/user/advanced/#session-objects`>

## Next steps

Complete documentation of Onyx for both the CLI and Python API can be
found [here](https://CLIMB-TRE.github.io/onyx-client/).
