"""
    This is an implemetation of the overlapping intervals problem.
    The MergeOverlappingIntervals class can deal with small in-memory inputs as well as storage file large inputs

    1- To test the in-memory use case, the programm generates a list of lists that can be used as input to the 
    method merge_overlapping_intevals.
    2- For large input simulation we generate a large text file (1 million lines) that gets not loaded at once to memory. 
    Instead we read it line by line and split it into sorted and merged subparts. This resulted subparts are stored in 
    seperate files under the sorted_parts directory. The subparts files content is then passed to the merge function of 
    the python standard library that is capable of merging multiple sorted inputs into a single sorted output 
    and returns an iterator over the sorted values.
    This process continues until we reached the final result.

    The input is checked for correctness in both cases before it gets processed. Any list item that does not fulfill
    the intervals requirements gets discarded.

    The time complexity for the sorting is O(n*log(n)) and the merging is linear O(n)
    with n is equal to length of the input

    About the test correctness:

        General Rule: All the outputs of all the Testcases must be sorted,
                      otherwise we can never be sure that the result is correct. 

        1- TestCase: intervals without errors and without non overlapping:
            The output of this test must be one interval containing as first element,
            the first element of the passed list of intervals and its last element must be the last element of the
            last interval of the passed list (Our Output fulfills this criteria)

        2- TestCase: 2- intervals with errors and without non overlapping:
            Because errors gets discarded by the program, the output must
            stay the same as the first TestCase (Our Output fulfills this criteria)

        3- TesCase: 3- intervals with errors and with non overlapping
            we introduce a non overlapping element and the end of every intervals list.
            The number of generated non overlapping intervals must be equal to the numbers of intervals lists plus one
            in-memory test: one list of intervals as input -> two intervals as output
            storage-file test: one thousand lists of intervals as input -> one thousand and one intervals as output
            (Our Output fulfills this criteria)
    ----------------------------------------------------------------------------------------------------------------
    Author: Amine M. El Jabri
"""

import os
import heapq
import shutil
import random


class MergeOverlappingIntervals:

    def __init__(self):
        """starts the program and runs the tests"""
        print("------------------------------------------------------------------------")
        print("IN-MEMORY TEST:\n")
        self.in_memory_input_test(10)
        print("------------------------------------------------------------------------")

        print("------------------------------------------------------------------------")
        print("STORAGE FILE TEST:")
        print("\n1- intervals without errors and without non overlapping")
        self.preapare_test_environnement()
        self.result_file = ""
        self.overlap = False
        self.output_temp_size = []
        self.output_temp = 0
        self.intervals_file_generator()
        sorted_files = self.file_split("input.txt")
        self.join_sorted_files(sorted_files)
        while self.overlap:
            self.merge_temp_output_file()
        shutil.copy(self.result_file, "final_result/test1_result.txt")
        print("To view the result, open: final_result/test1_result.txt")

        print("\n2- intervals with errors and without non overlapping")
        self.preapare_test_environnement(False)
        self.result_file = ""
        self.overlap = False
        self.output_temp_size = []
        self.output_temp = 0
        self.intervals_file_generator(True)
        sorted_files = self.file_split("input.txt")
        self.join_sorted_files(sorted_files)
        while self.overlap:
            self.merge_temp_output_file()
        shutil.copy(self.result_file, "final_result/test2_result.txt")
        print("To view the result, open: final_result/test2_result.txt")

        print("\n3- intervals with errors and without non overlapping")
        self.preapare_test_environnement(False)
        self.result_file = ""
        self.overlap = False
        self.output_temp_size = []
        self.output_temp = 0
        self.intervals_file_generator(True,True)
        sorted_files = self.file_split("input.txt")
        self.join_sorted_files(sorted_files)
        while self.overlap:
            self.merge_temp_output_file()
        shutil.copy(self.result_file, "final_result/test3_result.txt")
        print("To view the result, open: final_result/test3_result.txt")
        print("------------------------------------------------------------------------")
        



    def merge_overlapping_intevals(self,intervals):
        """
            Takes a list of intervals, and sort it based on the first element of the intervals.
            The overlapping intervals of the sorted list gets then merged
        """
        result = []
        intervals = self.enforce_correctness(intervals)
        if intervals:
            intervals.sort(key=lambda x: x[0])
            for interval in intervals:
                if (len(result) == 0) or (result[-1][1] < interval[0]):
                    result.append(interval)
                else:
                    result[-1][1] = max(result[-1][1], interval[1])
                    self.overlap = True
        return result



    def enforce_correctness(self,intervals):
        """
            Checks if the intervals inside a list are correct,
            an interval must be composed of two integers where the first one
            is smaller than the second one.
            We do not check for overflows, because integers in python can be
            arbitrary long
        """
        correct_intervals = []
        for interval in intervals:
            if len(interval) == 2:
                compare = True  
                for idx,i in enumerate(interval):
                    try:
                        interval[idx] = int(i)
                    except:
                        compare = False
                if compare:
                    if interval[0] < interval[1]:
                        correct_intervals.append(interval)
        return correct_intervals


    def error_interval(self,error_num):
        """
            Returns a faulty interval, based on the passed error number
        """
        if error_num == 0:
            return []
        elif error_num == 1:
            return [1,2,3]
        elif error_num == 2:
            return ["a",3]
        elif error_num == 3:
            return ["a","c"]
        else:
            return [18,9]


    def intervals_generator(self,intervals_count, starting_point,
        introduce_erros=False, introduce_non_overlaps=False):
        """
            Returns a list of intervals based on the invervals count and the 
            starting point (the first number of the first interval)
            Optionaly we can generates lists that contains non ovelapping or
            erroneous intervals
        """
        intervals = []
        itr_start = 0
        prv_itr_end = 0
        if intervals_count < 2:
            intervals_count = 2
        if starting_point != 0:
            itr_start = starting_point       
        for i in range(intervals_count):
            if prv_itr_end > 0:
                itr_start = prv_itr_end - 1
            if i == 2 and introduce_erros:
                intervals.append(self.error_interval(random.randint(0, 4)))
            itr_end = itr_start + 7
            intervals.append([itr_start, itr_end])
            prv_itr_end = itr_end        
            if i == (intervals_count -1) and introduce_non_overlaps:
                itr_start = prv_itr_end + 1
                itr_end = itr_start + 7
                intervals.append([itr_start, itr_end])
        return intervals


    def in_memory_input_test(self,intervals_count):
        """
            Starts 3 tests:
                1- intervals without errors and without non overlapping
                2- intervals with errors and without non overlapping
                3- intervals with errors and without non overlapping
        """
        print("INPUT: ",self.intervals_generator(intervals_count,0))
        print("------------------------------------------------------------------------")
        print("OUTPUT: ",
            self.merge_overlapping_intevals(self.intervals_generator(intervals_count,0)),"\n\n")
        print("INPUT: ",self.intervals_generator(intervals_count,1,True))
        print("------------------------------------------------------------------------")
        print("OUTPUT: ",
            self.merge_overlapping_intevals(self.intervals_generator(intervals_count,0,True)),"\n\n")
        print("INPUT: ",self.intervals_generator(intervals_count,1,True,True))
        print("------------------------------------------------------------------------")
        print("OUTPUT: ",
            self.merge_overlapping_intevals(self.intervals_generator(intervals_count,0,True,True)),"\n\n")



    def preapare_test_environnement(self,initialisation=True):
        """Removes all the files inside the folder, that will be used by the test"""
        dirs = ["temp","sorted_parts","final_result"]
        if not initialisation:
            dirs = ["temp","sorted_parts"]
        for dir in dirs:
            for files in os.listdir(dir):
                path = os.path.join(dir, files)
                try:
                    shutil.rmtree(path)
                except OSError:
                    os.remove(path)


    def intervals_file_generator(self,introduce_erros=False, introduce_non_overlaps=False):
        """Creates a file with 1 million intervals"""
        intervals = self.intervals_generator(1000,0,introduce_erros,introduce_non_overlaps)
        intervals = self.enforce_correctness(intervals)
        it_file = open('input.txt','w')
        for i in range(1000):
            if i != 0:
                starting_point = intervals[-1][-1] - 1
                intervals = self.intervals_generator(1000,starting_point,introduce_erros,introduce_non_overlaps)
            for interval in intervals:
                try:
                    line = str(interval[0])+","+str(interval[1])+"\n"
                    it_file.write(line)
                except:
                    pass
        it_file.close()


    def file_split(self,input_file):
        """
            Splits a big file into sorted and overlap merged subparts.
            Returns the names of the files where the subparts are stored
        """
        self.overlap == False
        sorted_files = []
        file_part = []
        part_idx = 0
        with open(input_file) as file:
            for line in file:
                file_part.append(line.rstrip().split(","))
                if len(file_part) == 1000:
                    file_part = self.merge_overlapping_intevals(file_part)
                    file_part_name = 'sorted_parts/'+str(part_idx)+'.txt'
                    sorted_files.append(file_part_name)
                    if part_idx == 0:
                        with open(file_part_name, 'w') as fp:
                            for interval in file_part:
                                line = str(interval[0])+","+str(interval[1])+"\n"
                                fp.write(line)
                        fp.close()
                    else:
                        with open(file_part_name, 'w') as fp:
                            for interval in file_part:
                                line = str(interval[0])+","+str(interval[1])+"\n"
                                fp.write(line)
                        fp.close()
                    part_idx = part_idx + 1
                    file_part = []
            else:
                file_part = self.merge_overlapping_intevals(file_part)
                file_part_name = 'sorted_parts/'+str(part_idx)+'.txt'
                sorted_files.append(file_part_name)
                if part_idx == 0:
                    with open(file_part_name, 'w') as fp:
                        for interval in file_part:
                            line = str(interval[0])+","+str(interval[1])+"\n"
                            fp.write(line)
                    fp.close()
                else:
                    with open(file_part_name, 'w') as fp:
                        for interval in file_part:
                            line = str(interval[0])+","+str(interval[1])+"\n"
                            fp.write(line)
                    fp.close()
        file.close()
        self.output_temp = self.output_temp + 1
        return sorted_files


    def file_to_list(self, file_name):
        """Returns the contents of a file as a list"""
        flist = []
        with open(file_name) as file:
            for line in file:
                try:
                    interval = line.rstrip().split(",")
                    flist.append([int(interval[0]),int(interval[1])])
                except:
                    pass
        file.close()
        return flist


    def join_sorted_files(self,sorted_files):
        """
            Joins the sorted and overlap merged subparts files with the merge function of 
            the python standard library that is capable of merging multiple sorted inputs into a single sorted output 
            and returns an iterator over the sorted values
            (The iterator enable us a memory friendly access to so far processed data).
            we loop over the iterator line by line and generate a temporory file that contains the so far reached
            result.
        """
        all_sorted_files_as_lists = [self.file_to_list(sf) for sf in sorted_files]
        sorted_temp_outp_list = list(heapq.merge(*all_sorted_files_as_lists))
        file_name = 'temp/'+str(self.output_temp)+'.txt'
        with open(file_name, 'w') as temp_outfile:
            for interval in sorted_temp_outp_list:
                line = str(interval[0])+","+str(interval[1])+"\n"
                temp_outfile.write(line)
        temp_outfile.close()
        self.output_temp_size.append(os.path.getsize(file_name))
        print("the temp output file",str(self.output_temp),"size is: ",os.path.getsize(file_name))


    def merge_temp_output_file(self):
        """
            makes sure that the process of splitting, sorting and merging is repeated
            until we reached the final result.
            we reach the final result if the size of temporory result files remains
            unchanged.
        """

        file_name = 'temp/'+str(self.output_temp)+'.txt'
        sorted_files = self.file_split(file_name)
        self.join_sorted_files(sorted_files)

        if len(self.output_temp_size) > 4:
            if len(set(self.output_temp_size[-3:])) == 1:
                self.overlap = False
                self.result_file = file_name


MergeOverlappingIntervals()