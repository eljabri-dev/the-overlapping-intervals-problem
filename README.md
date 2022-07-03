This is an implemetation of the overlapping intervals problem.
The MergeOverlappingIntervals class can deal with small in-memory inputs as well as storage file large inputs.

	1- To test the in-memory use case, the programm generates a list of lists that can be
	   used as input to the main class method merge_overlapping_intevals.

	2- For large input simulation we generate a large text file (1 million lines) that 
	   gets not loaded at once to memory.Instead we read it line by line and split it into
	   sorted and merged subparts. This resulted subparts are stored in seperate files under 
	   the sorted_parts directory. The subparts files content is then passed to 
	   the merge function of the python standard library that is capable of merging multiple
	   sorted inputs into a single sorted output and returns an iterator over 
	   the sorted values. This process continues until we reached the final result.

The input is checked for correctness in both cases before it gets processed. Any list item that does not fulfill
the intervals requirements gets discarded.

For more details, please read the code comments.

## Usage
  
This implementation uses the python standard library only, so if you have any python 3 version installed on your computer you can run the Program as follows:

Under Microsoft:

```sh

$ python merging_overlapping_intervals.py

```

Under Linux:

```sh

$ python3 merging_overlapping_intervals.py

```

### Prerequisites

Any python 3 version.

  
## Repository Layout

  

*  `final_result/` – contains the test results of the storage files large inputs.

*  `sorted_parts/` - contains the merged and sorted subparts files of the large input files.

*  `temp/` - contains the temporory results of the merging and sorting.
