multi_shot_primer = {}
multi_shot_key = {}
multi_shot_comment = {}
multi_shot_comment_end = {}
multi_shot_primer["DOCSTYLE"] = '''
SAMPLE 1
CODE:
void getInput(string names[], int ages[], const int SIZE) {
    // for each student
    for (int i = 0; i < SIZE; i++) {
        // prompt and store the name of the current student
        cout << "Enter the name for student #" << i + 1 << ": ";
        getline(cin, names[i]);

        // prompt and store for the age of the current student
        cout << "Enter the age for student #" << i + 1 << ": ";
        cin >> ages[i];

        // need to ignore the newline for the next iteration
        cin.ignore();
    }
}
CODE_END

COMMENT:
/*******************************************************************************
* 
*   Use a for loop to prompt the user for the name/age of each student. Store
*   the information in the appropriate array.
*
* Inputs:
*   names - a string array for storing the students' names
*   ages  - an integer array for storing the students' ages
*   SIZE  - a constant integer that represents the size of the two arrays
*******************************************************************************/
COMMENT_END

SAMPLE 2
CODE:
::is_sorted_backward(it_index itx_first, it_index itx_last)
{
    size_t nblock = size_t(itx_last - itx_first);
    range_it rng = get_group_range(*itx_first, nblock);

    size_t nelem = rng.size();
    size_t min_process = (std::max)(BLOCK_SIZE, (nelem >> 3));

    size_t nsorted2 = bsc::number_stable_sorted_backward(rng.first, rng.last,
                                                         min_process, cmp);
    if (nsorted2 == nelem) return true;
    if (nsorted2 == 0 ) return false;
    Iter_t itaux = rng.last - nsorted2;
    size_t nsorted1 = nelem - nsorted2;

    if (nsorted1 <= (BLOCK_SIZE << 1))
    {
        flat_stable_sort(rng.first, itaux, cmp, ptr_circ);
        bscu::insert_sorted_backward(rng.first, itaux, rng.last, cmp,
                                     ptr_circ->get_buffer());
    }
    else
    {   // Adjust the size of nsorted2 for to be a number of blocks
        size_t nblock1 = (nsorted1 + BLOCK_SIZE - 1) >> Power2;
        size_t nsorted1_adjust = (nblock1 << Power2);
        flat_stable_sort(rng.first, rng.first + nsorted1_adjust, cmp,
                         ptr_circ);
        merge_range_pos(itx_first, itx_first + nblock1, itx_last);
    };
    return true;
};
CODE_END

COMMENT:
/*******************************************************************************
* 
*   This function checks if a range of elements is sorted in a descending order.
*   It uses the number_stable_sorted_backward function to determine the number
*   of sorted elements in the range, and then uses the flat_stable_sort and
*   insert_sorted_backward functions to sort the remaining elements.
*
* Inputs:
*   itx_first - an iterator pointing to the first element in the range
*   itx_last  - an iterator pointing to the last element in the range
*
* Outputs:
*   bool - true if the range is sorted in a descending order, false otherwise
*******************************************************************************/
COMMENT_END

SAMPLE 3
CODE:

'''
multi_shot_key["DOCSTYLE"] = '''SAMPLE 3
CODE:''' 

multi_shot_comment["DOCSTYLE"] = '''
CODE_END

COMMENT:'''

multi_shot_comment_end["DOCSTYLE"] = '''COMMENT_END''' 



multi_shot_primer["DOCSTRING.AI"] = '''
SAMPLE 1
CODE:
void getInput(string names[], int ages[], const int SIZE) {
    // for each student
    for (int i = 0; i < SIZE; i++) {
        // prompt and store the name of the current student
        cout << "Enter the name for student #" << i + 1 << ": ";
        getline(cin, names[i]);

        // prompt and store for the age of the current student
        cout << "Enter the age for student #" << i + 1 << ": ";
        cin >> ages[i];

        // need to ignore the newline for the next iteration
        cin.ignore();
    }
}
CODE_END

COMMENT:
// This is a function called `getInput` that takes in three parameters: an array of strings called `names`, an array of integers called `ages`, and a constant integer called `SIZE`.
COMMENT_END

SAMPLE 2
CODE:
::is_sorted_backward(it_index itx_first, it_index itx_last)
{
    size_t nblock = size_t(itx_last - itx_first);
    range_it rng = get_group_range(*itx_first, nblock);

    size_t nelem = rng.size();
    size_t min_process = (std::max)(BLOCK_SIZE, (nelem >> 3));

    size_t nsorted2 = bsc::number_stable_sorted_backward(rng.first, rng.last,
                                                         min_process, cmp);
    if (nsorted2 == nelem) return true;
    if (nsorted2 == 0 ) return false;
    Iter_t itaux = rng.last - nsorted2;
    size_t nsorted1 = nelem - nsorted2;

    if (nsorted1 <= (BLOCK_SIZE << 1))
    {
        flat_stable_sort(rng.first, itaux, cmp, ptr_circ);
        bscu::insert_sorted_backward(rng.first, itaux, rng.last, cmp,
                                     ptr_circ->get_buffer());
    }
    else
    {   // Adjust the size of nsorted2 for to be a number of blocks
        size_t nblock1 = (nsorted1 + BLOCK_SIZE - 1) >> Power2;
        size_t nsorted1_adjust = (nblock1 << Power2);
        flat_stable_sort(rng.first, rng.first + nsorted1_adjust, cmp,
                         ptr_circ);
        merge_range_pos(itx_first, itx_first + nblock1, itx_last);
    };
    return true;
};
CODE_END

COMMENT:
// This is a function called `is_sorted_backward` that takes in two iterators `itx_first` and `itx_last` representing a range of elements and checks if the range is sorted in non-increasing order.
COMMENT_END

SAMPLE 3
CODE:

'''
multi_shot_key["DOCSTRING.AI"] = '''SAMPLE 3
CODE:''' 

multi_shot_comment["DOCSTRING.AI"] = '''
CODE_END

COMMENT:'''

multi_shot_comment_end["DOCSTRING.AI"] = '''COMMENT_END''' 


multi_shot_primer["NOSHOT"] = '''
CODE:

'''
multi_shot_key["NOSHOT"] = '''
CODE:''' 

multi_shot_comment["NOSHOT"] = '''
CODE_END

COMMENT:'''

multi_shot_comment_end["NOSHOT"] = '''COMMENT_END''' 