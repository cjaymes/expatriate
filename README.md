# pyscap
Python implementation of a Security Content Automation Protocol compatible Configuration, Vulnerability, Patch and Inventory Scanner

Requires Python 3.5 or greater. See the requirements.txt file for addition required packages that can be installed using:

    pip install -r requirements.txt

Usage
=====

    pyscap.py
        [--help or -h]
        [--version or -V]
        [--verbose or -v]
        [--output [OUTPUT] or -o [OUTPUT]]
        [--inventory INVENTORY [INVENTORY ...]]
        [--host HOST [HOST ...]]
        --list-hosts
        | --parse CONTENT [CONTENT ...]
        | --detect
        | --collect --content CONTENT [--content CONTENT [...]]
        | --benchmark
            --content CONTENT [--content CONTENT [...]]
            [--data_stream DATA_STREAM]
            [--checklist CHECKLIST]
            [--profile PROFILE]
            [--pretty]

Options
-------

* --help

    Prints a help message.

* --version

    Prints the version of pyscap.

* --verbose

    Prints greater detail to the log/stderr. Multiple -v flags can be used to increase the level of detail.

* --output

    Configures the location where output is sent for the various operations. Stdout can be specified with - and is also the default output location.

* --inventory

    Specifies the location of an (ini formatted) inventory file. Pyscap by default tries to load ~/.pyscap/inventory.ini unless one is specified. See the inventory_sample.ini file for an example of the file and settings that can be used. Currently, only local and ssh connections are supported.

* --host

    Specifies a host to target. Except for the special host specification 'localhost', which just forks a shell on the current host, these should be defined in an inventory file and referenced by this option.

Operations
----------

* --list-hosts

    List the hosts that would be targeted. Utility operation that will eventually be deprecated.

* --parse
    Parse the specified file. Utility operation that will eventually be deprecated.

* --detect
    Do basic detection on the specified host(s)

* --collect
    Collect system characteristics about the specified host(s)

    * --content
        Specifies the content to use for system characteristic collection

* --benchmark

    Benchmarks a host against a checklist (unless there's only one).

    * --content

        Specifies the content to use for benchmarking.

    * --data_stream

        If a data stream collection is used, the data_stream must also be specified (required unless there's only one).

    * --checklist

        Used to specify checklist (required unless there's only one).

    * --profile

        Used to specify profile (required unless there's only one).

    * --pretty

        Beautify the output generated to make it easier to read by human eyes.
