# SciX Reference Matching Workflow Tools
Tools to help connect modern reference processing architecture to Classic back office workflows
## Usage and logic
This environent uses the typical `run.py` approach. Command line parameters (described below) determine the results generated.
### Saving citing/cited pairs of bibcodes
For interoperability with the Classic reference processing workflow, a file TSV file needs to be generated with the bibcode of the citing publication in the first column and the bibcode of the cited work in the second column (for those cases where the cited work was successfully matched with an existing record). This is done as follows

```
python run.py -r/--resolved [-f/--file <optional alternative output file>]
```
The default location is stored in the configuration. The default command (above) saves all resolved references that do NOT have either arXiv or AUTHOR as source. To store arXiv references, do
```
python run.py -r/--resolved [-f/--file <optional alternative output file>] --rs arXiv
```
and for author-submitted references do
```
python run.py -r/--resolved [-f/--file <optional alternative output file>] --rs AUTHOR
```
(actually, the filtering on source is done case-insensitively).
### Show files: time frame
When troubleshooting it can be helpful to find files that were processed in a specific time frame; either the time frame in which they were processed or the time frame in which the source files were updated. The pattern for this is as follows

```
python run.py -d/--date <date type> [-sd/--start_date <start date> -ed/--end_date <end date>
```
Without a time frame specificied, the script will take the past 31 days as default. The value to be specified with the required parameter is either `processed` or `updated`. Dates are expected in the numerical format `YYYY-MM-DD`. This command returns a list of file names, together with the date on which the source file was modified and the date on which the file was processed.
### Show files: citing work
To display a list of files that contain reference data cited by a specific publication, use the pattern

```
python run.py -s/--citing <bibcode of citing work>
```
This command returns a list of file names, together with the date on which the source file was modified and the date on which the file was processed.
### Show files: cited work
To display a list of files that contain reference data matched to an existing record, use the pattern
```
python run.py -t/--cited <bibcode of cited work>
```
This command returns a list of file names, together with the date on which the source file was modified and the date on which the file was processed.
### Reference data with specific pattern
In some cases we like to be able to generate a list of references (from the raw reference data) that contain a specific text string. This can be done using the pattern

```
python run.py -x/--text <ASCII string>
```
This will result in a case-insensitive search of the text provided. Currently no regular expressions are supported.
### Comparison with Classic workflow
The reference pipeline, when executed with the appropriate parameter, generates results from a comparison with the Classic workflow. The following command generates results from this comparison

```
python run.py -c/--check <status>
```
The value to be supplied on the command line is one of the following
| Label | Classic Score | Service Score | Comments                                                   |
|-------|---------------|---------------|------------------------------------------------------------|
| UNVER | 5             | 0             | Classic found unverified bibcode and service did not match |
| NEWU  | 5             | 1             | Classic found unverified bibcode and service found match   |
| MATCH | 1             | 1             | Both Classic and service agreed on match                   |
| DIFF  | 1             | 1             | Classic and service found different matches                |
| MISS  | 1             | 0             | Classic found match and service did not match              |
| NEW   | 0             | 1             | Classic unmatched and service found match                  |
| NONE  | 0             | 0             | Both Classic and service did not find match                |

The cases `DIFF` and `MISS` are the most interesting for troubleshooting (the Classic workflow found a match and service is in disagreement).
